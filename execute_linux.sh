#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

start_server() {
  local locks_value="$1"
  echo "Iniciando servidor (locks=${locks_value})..."
  node "${ROOT_DIR}/server.js" -locks "${locks_value}" &
  SERVER_PID=$!

  # Give the server time to bind the port.
  sleep 2
}

stop_server() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "Deteniendo servidor (PID=${SERVER_PID})..."
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
  SERVER_PID=""
}

run_attack() {
  echo "Ejecutando ataque..."
  if command -v python3 >/dev/null 2>&1; then
    python3 "${ROOT_DIR}/raceConditionNode.py"
  else
    python "${ROOT_DIR}/raceConditionNode.py"
  fi
}

cleanup() {
  stop_server
}

trap cleanup EXIT

echo "[1/4] Iniciando servidor SIN locks..."
start_server 0

echo "[2/4] Ejecutando ataque (SIN locks)..."
run_attack

stop_server
sleep 1

echo "[3/4] Iniciando servidor CON locks..."
start_server 1

echo "[4/4] Ejecutando ataque (CON locks)..."
run_attack

stop_server

echo "Listo."

