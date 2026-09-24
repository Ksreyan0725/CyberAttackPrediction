# ===== Build stage: compile Go error-bus for Linux =====
FROM golang:1.22-alpine AS go-builder

WORKDIR /build
COPY CyberAttackPrediction/error-bus/go.mod ./
COPY CyberAttackPrediction/error-bus/main.go ./
RUN go build -o /error-bus .

# ===== Build stage: compile TypeScript app modules =====
FROM node:20-slim AS ts-builder

WORKDIR /t
COPY CyberAttackPrediction/static/ts/package.json CyberAttackPrediction/static/ts/tsconfig.json ./
RUN npm install --no-audit --no-fund
COPY CyberAttackPrediction/static/ts/*.ts ./
RUN npm run build

# ===== Build stage: compile Rust guest-engine for Linux =====
FROM rust:1.79-slim AS rust-builder

WORKDIR /build
COPY CyberAttackPrediction/rust_auth/Cargo.toml CyberAttackPrediction/rust_auth/Cargo.lock* ./
COPY CyberAttackPrediction/rust_auth/src ./src
RUN cargo build --release

# ===== Final stage: Python app with compiled binaries =====
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies (supervisord, curl for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY CyberAttackPrediction/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy the app source first
COPY CyberAttackPrediction /app/CyberAttackPrediction

# Overlay compiled Linux binaries on top
# error-bus goes to /usr/local/bin so it never collides with the
# source directory /app/CyberAttackPrediction/error-bus/
COPY --from=go-builder /error-bus /usr/local/bin/error-bus
COPY --from=rust-builder /build/target/release/rust_auth /app/CyberAttackPrediction/rust_auth/target/release/rust_auth

# Overlay compiled frontend assets (TypeScript modules -> static/js)
COPY --from=ts-builder /js /app/CyberAttackPrediction/static/js

# Supervisor config to run Flask + Go error-bus together
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create logs directory
RUN mkdir -p /app/CyberAttackPrediction/logs

EXPOSE 8080

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
