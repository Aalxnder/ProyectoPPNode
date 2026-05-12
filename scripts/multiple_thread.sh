#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THREAD_COUNTS=(1 2 4 8)

start_server() {
  local locks_value="$1"
  echo "Iniciando servidor (locks=${locks_value})..."
  node "${ROOT_DIR}/server.js" -locks "${locks_value}" &
  SERVER_PID=$!
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
  local threads="$1"
  echo "Ejecutando ataque con ${threads} hilos..."
  if command -v python3 >/dev/null 2>&1; then
    python3 "${ROOT_DIR}/raceConditionNode.py" --hilos "${threads}"
  else
    python "${ROOT_DIR}/raceConditionNode.py" --hilos "${threads}"
  fi
}

cleanup() {
  stop_server
}

trap cleanup EXIT

echo "[1/2] Iniciando servidor SIN locks..."
start_server 0

for t in "${THREAD_COUNTS[@]}"; do
  echo
  echo "Ejecutando ataque (SIN locks) con ${t} hilos..."
  run_attack "${t}"
done

stop_server
sleep 1

echo "[2/2] Iniciando servidor CON locks..."
start_server 1

for t in "${THREAD_COUNTS[@]}"; do
  echo
  echo "Ejecutando ataque (CON locks) con ${t} hilos..."
  run_attack "${t}"
done

stop_server

echo "Listo."
