#!/usr/bin/env python3
"""
07_rag_con_ia.py — Ejercicio 7: RAG + IA
=========================================

El RAG básico (ejercicio 6) devuelve "cachos crudos". Aquí esos fragmentos se
pasan a un modelo de lenguaje (LLM) para que redacte una respuesta natural,
humana y comprensible, usando solo el contexto recuperado.

Modelo de IA: Ollama en local (igual que el repositorio original, que usaba
llama3.1:8b). Si Ollama no está corriendo, se muestra una respuesta de respaldo
hecha con los chunks, indicándolo claramente.

Para usar IA real:
    1. Instala Ollama:  https://ollama.com
    2. Descarga el modelo:  ollama pull llama3.1:8b
    3. Asegúrate de que el servicio está activo (ollama serve)

Uso:
    python3 07_rag_con_ia.py
    python3 07_rag_con_ia.py --pregunta "..." --modelo llama3.1:8b
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nucleo.rag import MotorRAG, ollama_disponible  # noqa: E402


def cargar_corpus() -> str:
    ruta = os.path.join(os.path.dirname(__file__), "datos", "corpus.txt")
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def main() -> None:
    ap = argparse.ArgumentParser(description="RAG + IA con Ollama")
    ap.add_argument("--pregunta", help="Pregunta a realizar")
    ap.add_argument("--modelo", default="llama3.1:8b", help="Modelo de Ollama")
    ap.add_argument("--k", type=int, default=4, help="Nº de chunks de contexto")
    args = ap.parse_args()

    print("=" * 64)
    print("  EJERCICIO 7 — RAG + IA (chunks -> LLM -> respuesta natural)")
    print("=" * 64)

    disponible = ollama_disponible()
    print(f"  Ollama detectado: {'SÍ' if disponible else 'NO (modo respaldo)'}")
    if disponible:
        print(f"  Modelo: {args.modelo}")

    rag = MotorRAG(nombre_coleccion="rag_ia")
    print(f"  Embedding: {rag.nombre_embedding}")
    n = rag.indexar_texto(cargar_corpus(), fuente="corpus")
    print(f"  Indexado: {n} chunks")

    preguntas = (
        [args.pregunta]
        if args.pregunta
        else [
            "¿Qué diferencia hay entre un proceso y un hilo?",
            "¿Cómo se almacena una contraseña de forma segura?",
        ]
    )

    for pregunta in preguntas:
        print("\n" + "=" * 64)
        print(f"  PREGUNTA: {pregunta}")
        print("=" * 64)

        r = rag.consultar_con_ia(pregunta, k=args.k, modelo=args.modelo)

        print(f"\n  --- Contexto recuperado ({len(r.chunks)} chunks) ---")
        for i, c in enumerate(r.chunks, 1):
            print(f"  [{i}] {c[:80]}...")

        print(f"\n  --- Respuesta generada (fuente: {r.fuente_ia}) ---\n")
        for linea in r.respuesta_ia.splitlines():
            print(f"  {linea}")

    print("\n" + "=" * 64)


if __name__ == "__main__":
    main()
