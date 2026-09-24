package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

// ─── Configuration ───
// NOTE: must NOT read PORT — Render sets PORT to the public web port
// (gunicorn's). The sidecar listens on its own private port instead.
const (
	MaxEvents        = 5000
	HeartbeatInterval = 3 * time.Second
)

// Port is resolved at init time (not a const — getEnv is a runtime call).
var Port = getEnv("ERROR_BUS_PORT", "9090")

func getEnv(key, defaultVal string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return defaultVal
}

// ─── Event Structure ───
type Event struct {
	Timestamp string                 `json:"timestamp"`
	Level     string                 `json:"level"`     // info, warning, error
	Code      string                 `json:"code"`      // e.g., VALIDATION_ERROR, OOM
	Message   string                 `json:"message"`   // human-readable
	Details   interface{}            `json:"details,omitempty"`
	Route     string                 `json:"route,omitempty"`
	Method    string                 `json:"method,omitempty"`
	Status    int                    `json:"status,omitempty"`
	DurationMs int                   `json:"duration_ms,omitempty"`
	RequestID string                 `json:"request_id,omitempty"`
}

// ─── In-Memory Ring Buffer ───
type EventStore struct {
	mu      sync.RWMutex
	events  []Event
	maxSize int
}

func NewEventStore(maxSize int) *EventStore {
	return &EventStore{
		events:  make([]Event, 0, maxSize),
		maxSize: maxSize,
	}
}

func (s *EventStore) Add(e Event) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.events = append(s.events, e)
	if len(s.events) > s.maxSize {
		s.events = s.events[len(s.events)-s.maxSize:]
	}
}

func (s *EventStore) Get(limit, offset int, level, code, route, search string) []Event {
	s.mu.RLock()
	defer s.mu.RUnlock()
	
	result := make([]Event, 0)
	for i := len(s.events) - 1; i >= 0; i-- {
		e := s.events[i]
		if level != "" && e.Level != level { continue }
		if code != "" && e.Code != code { continue }
		if route != "" && e.Route != route { continue }
		if search != "" {
			s := search
			found := false
			if len(e.Message) > 0 && containsIgnoreCase(e.Message, s) { found = true }
			if !found {
				b, _ := json.Marshal(e.Details)
				if containsIgnoreCase(string(b), s) { found = true }
			}
			if !found { continue }
		}
		result = append(result, e)
	}
	
	// Apply pagination
	start := 0
	if offset > 0 && offset < len(result) {
		start = offset
	}
	end := len(result)
	if limit > 0 && start+limit < end {
		end = start + limit
	}
	if start > len(result) {
		return []Event{}
	}
	return result[start:min(end, len(result))]
}

func min(a, b int) int {
	if a < b { return a }
	return b
}

func containsIgnoreCase(s, substr string) bool {
	sLower := ""
	for _, r := range s {
		if r >= 'A' && r <= 'Z' {
			sLower += string(r + 32)
		} else {
			sLower += string(r)
		}
	}
	subLower := ""
	for _, r := range substr {
		if r >= 'A' && r <= 'Z' {
			subLower += string(r + 32)
		} else {
			subLower += string(r)
		}
	}
	return len(sLower) >= len(subLower) && (sLower == substr || len(sLower) > len(substr) && (sLower[:len(substr)] == subLower || sLower[len(sLower)-len(substr):] == subLower || containsSubstring(sLower, subLower)))
}

func containsSubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// ─── HTTP Handlers ───
type Server struct {
	store *EventStore
}

func NewServer() *Server {
	return &Server{store: NewEventStore(5000)}
}

func (s *Server) HealthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "ok",
		"service": "error-bus",
		"time":    time.Now().UTC().Format(time.RFC3339),
	})
}

func (s *Server) EventHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	var e Event
	if err := json.NewDecoder(r.Body).Decode(&e); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}
	if e.Timestamp == "" {
		e.Timestamp = time.Now().UTC().Format(time.RFC3339)
	}
	s.store.Add(e)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "accepted"})
}

func (s *Server) EventsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	
	q := r.URL.Query()
	limit := 100
	if l := q.Get("limit"); l != "" {
		fmt.Sscanf(l, "%d", &limit)
	}
	offset := 0
	if o := q.Get("offset"); o != "" {
		fmt.Sscanf(o, "%d", &offset)
	}
	level := q.Get("level")
	code := q.Get("code")
	
	events := s.store.Get(limit, offset, level, code, q.Get("route"), q.Get("search"))
	s.store.mu.RLock()
	total := len(s.store.events)
	s.store.mu.RUnlock()
	json.NewEncoder(w).Encode(map[string]interface{}{
		"events": events,
		"total":  total,
		"limit":  limit,
		"offset": offset,
	})
}

func (s *Server) StreamHandler(w http.ResponseWriter, r *http.Request) {
	// SSE endpoint for real-time log streaming
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	
	// Send initial events
	s.store.mu.RLock()
	for _, e := range s.store.events {
		fmt.Fprintf(w, "data: %s\n\n", mustMarshal(e))
	}
	s.store.mu.RUnlock()
	flusher.Flush()
	
	// Keep connection alive, send new events as they arrive
	// (Simplified: in production use a pub/sub channel)
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	for range ticker.C {
		fmt.Fprintf(w, ": keep-alive\n\n")
		flusher.Flush()
	}
}

func mustMarshal(v interface{}) string {
	b, _ := json.Marshal(v)
	return string(b)
}

func main() {
	s := NewServer()
	mux := http.NewServeMux()
	
	mux.HandleFunc("/health", s.HealthHandler)
	mux.HandleFunc("/event", s.EventHandler)
	mux.HandleFunc("/events", s.EventsHandler)
	mux.HandleFunc("/stream", s.StreamHandler)
	
	addr := ":" + Port
	log.Printf("[error-bus] Starting on %s", addr)
	log.Fatal(http.ListenAndServe(addr, mux))
}