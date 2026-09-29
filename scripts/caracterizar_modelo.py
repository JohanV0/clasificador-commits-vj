#!/usr/bin/env python3
"""Caracteriza el modelo Ollama local: latencias y calidad."""
import json
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:270m"
PROMPT = "Responde solo con una palabra: hola"
N = 5

def llamar_modelo():
    payload = json.dumps({
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    dt = (time.perf_counter() - t0) * 1000
    return dt, data.get("response", "").strip()

def main():
    latencias = []
    print(f"Caracterizando {MODEL} con {N} ejecuciones...\n")
    for i in range(1, N + 1):
        ms, respuesta = llamar_modelo()
        latencias.append(ms)
        print(f"Ejecucion {i}: {ms:.0f} ms  ->  {respuesta!r}")

    prom = sum(latencias) / len(latencias)
    print(f"\nLatencia promedio: {prom:.1f} ms")
    print(f"Latencia minima:   {min(latencias):.1f} ms")
    print(f"Latencia maxima:   {max(latencias):.1f} ms")

if __name__ == "__main__":
    main()
