#!/usr/bin/env bash
set -euo pipefail

# -------------------- CONFIGURABILI --------------------
POSTGRES_USER="${POSTGRES_USER:-drivingsocial}"
POSTGRES_DB="${POSTGRES_DB:-drivingsocial}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-strongpassword123}"
POSTGRES_PORT=5432

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"
FRONTEND_HOST="${FRONTEND_HOST:-0.0.0.0}"
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"

DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"

# ----------------- INSTALLAZIONE BASE ------------------
echo "🟢 Aggiornamento e installazione pacchetti base..."
apt-get update -y
apt-get install -y curl git sudo

if ! command -v docker &> /dev/null; then
  echo "🟢 Installazione Docker..."
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER
fi

if ! command -v docker-compose &> /dev/null; then
  sudo apt-get install -y docker-compose
fi

# ------------------ INIZIALIZZA IL PROGETTO ------------------
if [ ! -d ".git" ]; then
  # (esempio: se vuoi clonare un repo iniziale, oppure partire da qui)
  echo "⚠️  Progetto non inizializzato: usa 'git init' e commita i tuoi file."
else
  echo "🟢 Progetto già inizializzato in questa directory."
fi

# ------------------ SETUP BACKEND .ENV ------------------
if [ ! -f backend/.env ]; then
  echo "🟢 Creo backend/.env..."
  cp backend/.env.example backend/.env
  echo "DATABASE_URL=${DATABASE_URL}" >> backend/.env
  echo "SECRET_KEY=${SECRET_KEY:-verysecurekey}" >> backend/.env
fi

# ------------------ AVVIO DOCKER COMPOSE ------------------
echo "🟢 Avvio Docker Compose in background..."
docker compose up --build -d

echo "✅ Driving Social avviato ✅"
echo "🌐 Frontend: http://${FRONTEND_HOST}:${FRONTEND_PORT}"
echo "🛠️  Backend: http://${BACKEND_HOST}:${BACKEND_PORT}"
