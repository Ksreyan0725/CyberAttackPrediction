/* CyberShield Service Worker - hand-maintained source (plain JS). */
"use strict";
/**
 * CyberShield Service Worker — TypeScript source.
 * Build: `npm run build` in static/ts/ emits ../sw.js (the served file).
 * Do not hand-edit ../sw.js — edit this file instead.
 *
 * What it caches:
 *   1. Temporary same-origin GET /api/* JSON (data only, 5-min TTL, 50 max).
 *   2. Same-origin images (stale-while-revalidate, 7-day TTL, 60 max).
 * What it NEVER caches: HTML documents, CSS, JS, fonts, CDN files,
 *   POST/PUT/DELETE. App code always loads fresh from the server, and the
 *   browser's own HTTP cache keeps working underneath untouched.
 */
/// <reference lib="webworker" />
const SW = self;
const DATA_CACHE = "cybershield-data-v1";
const IMG_CACHE = "cybershield-img-v1";
const MAX_DATA_ENTRIES = 50;
const DATA_TTL_MS = 5 * 60 * 1000; // 5 minutes — temporary by design
const MAX_IMG_ENTRIES = 60;
const IMG_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days — images rarely change
SW.addEventListener("install", () => {
    // No precache on purpose: zero app files are stored.
    SW.skipWaiting();
});
SW.addEventListener("activate", (event) => {
    event.waitUntil(caches.keys()
        .then((names) => Promise.all(names.map((n) => (n === DATA_CACHE || n === IMG_CACHE ? null : caches.delete(n)))))
        .then(() => SW.clients.claim()));
});
// ---------------------------------------------------------------------------
// Theme choice memory (one word only — no page content, no user data).
// ---------------------------------------------------------------------------
let savedTheme = null;
SW.addEventListener("message", (event) => {
    if (event.origin && event.origin !== location.origin) return;
    const data = (event.data || {});
    if (data.type === "THEME_SET" &&
        (data.theme === "light" || data.theme === "dark" || data.theme === "auto")) {
        savedTheme = data.theme;
        const src = event.source;
        SW.clients
            .matchAll({ type: "window", includeUncontrolled: true })
            .then((clients) => {
            clients.forEach((c) => {
                if (src && c.id === src.id)
                    return; // sender already applied it
                c.postMessage({ type: "THEME_APPLY", theme: savedTheme });
            });
        })
            .catch(() => { });
    }
    else if (data.type === "THEME_GET" && event.source) {
        event.source.postMessage({ type: "THEME_VALUE", theme: savedTheme });
    }
});
// ---------------------------------------------------------------------------
// Request classifiers
// ---------------------------------------------------------------------------
function sameOrigin(url) {
    return url.origin === SW.location.origin;
}
function isDataRequest(request) {
    if (request.method !== "GET")
        return false;
    let url;
    try {
        url = new URL(request.url);
    }
    catch {
        return false;
    }
    return sameOrigin(url) && url.pathname.startsWith("/api/");
}
const IMG_EXT = /\.(png|jpe?g|gif|webp|ico|svg|bmp|avif)(\?.*)?$/i;
function isImageRequest(request) {
    if (request.method !== "GET")
        return false;
    let url;
    try {
        url = new URL(request.url);
    }
    catch {
        return false;
    }
    if (!sameOrigin(url))
        return false; // never third-party
    if (request.destination === "image")
        return true;
    return IMG_EXT.test(url.pathname);
}
// ---------------------------------------------------------------------------
// Cache helpers
// ---------------------------------------------------------------------------
function stampedCopy(res) {
    const headers = new Headers(res.headers);
    headers.set("X-SW-Cached-At", String(Date.now()));
    return new Response(res.body, {
        status: res.status,
        statusText: res.statusText,
        headers,
    });
}
function trimCache(cache, max) {
    return cache.keys().then((keys) => {
        if (keys.length <= max)
            return null;
        // Keys are insertion-ordered: drop the oldest surplus.
        return Promise.all(keys.slice(0, keys.length - max).map((k) => cache.delete(k)));
    });
}
function freshEnough(cached, ttl) {
    const at = parseInt(cached.headers.get("X-SW-Cached-At") || "0", 10);
    return !!at && Date.now() - at <= ttl;
}
function offlineJson() {
    return new Response(JSON.stringify({ ok: false, code: "OFFLINE", message: "Offline — no cached data available." }), { status: 503, headers: { "Content-Type": "application/json", "X-SW-Fallback": "offline" } });
}
// ---------------------------------------------------------------------------
// Strategies
// ---------------------------------------------------------------------------
function handleData(request) {
    return fetch(request).then((res) => {
        const ct = res.headers.get("content-type") || "";
        if (res.ok && ct.indexOf("application/json") !== -1) {
            caches.open(DATA_CACHE).then((cache) => {
                cache.put(request, stampedCopy(res)).then(() => trimCache(cache, MAX_DATA_ENTRIES));
            }).catch(() => { });
        }
        return res;
    }).catch(() => caches.open(DATA_CACHE).then((cache) => cache.match(request).then((cached) => {
        if (!cached || !freshEnough(cached, DATA_TTL_MS)) {
            if (cached)
                cache.delete(request).catch(() => { });
            return offlineJson();
        }
        const headers = new Headers(cached.headers);
        headers.set("X-SW-Stale", "true");
        return new Response(cached.body, {
            status: cached.status,
            statusText: cached.statusText,
            headers,
        });
    })).catch(offlineJson));
}
function handleImage(request) {
    // Stale-while-revalidate: instant paint from cache, silent refresh behind.
    // The browser's HTTP cache still applies underneath — no conflict, since
    // the SW cache is a separate layer keyed by request URL.
    return caches.open(IMG_CACHE).then((cache) => cache.match(request).then((cached) => {
        const refresh = fetch(request).then((res) => {
            const ct = res.headers.get("content-type") || "";
            if (res.ok && (res.type === "basic" || res.type === "default") && ct.indexOf("image/") === 0) {
                cache.put(request, stampedCopy(res)).then(() => trimCache(cache, MAX_IMG_ENTRIES));
            }
            return res;
        }).catch(() => null);
        if (cached && freshEnough(cached, IMG_TTL_MS)) {
            refresh.catch(() => { });
            return cached;
        }
        // No usable copy: wait for network, fall back to stale copy if any.
        return refresh.then((res) => {
            if (res)
                return res;
            if (cached)
                return cached;
            throw new Error("offline");
        }).catch(() => new Response(null, { status: 504, statusText: "Gateway Timeout" }));
    }));
}
SW.addEventListener("fetch", (event) => {
    const request = event.request;
    if (isDataRequest(request)) {
        event.respondWith(handleData(request));
    }
    else if (isImageRequest(request)) {
        event.respondWith(handleImage(request));
    }
    // Everything else (HTML, CSS, JS, fonts, uploads, POSTs): pass through.
});
