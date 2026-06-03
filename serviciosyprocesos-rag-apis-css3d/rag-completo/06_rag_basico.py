#!/usr/bin/env python3
"""
06_rag_basico.py — Ejercicio 6: RAG básico
===========================================

Demuestra el ciclo completo de un RAG SIN IA:
  1. Cargar un texto grande
  2. Trocearlo en chunks
  3. Calcular embeddings y guardarlos en ChromaDB
  4. Hacer preguntas y recuperar los chunks más similares semánticamente

El resultado son los "cachos crudos" (raw chunks). El ejercicio 7 los mejora
pasándolos por una IA.

Uso:
    python3 06_rag_basico.py
    python3 06_rag_basico.py --pregunta "tu pregunta aquí"
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nucleo.rag import MotorRAG  # noqa: E402


def cargar_corpus() -> str:
    ruta = os.path.join(os.path.dirname(__file__), "datos", "corpus.txt")
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            return f.read()
    return "No se encontró datos/corpus.txt"


def main() -> None:
    ap = argparse.ArgumentParser(description="RAG básico con ChromaDB")
    ap.add_argument("--pregunta", help="Pregunta a realizar")
    ap.add_argument("--k", type=int, default=3, help="Nº de chunks a recuperar")
    args = ap.parse_args()

    print("=" * 64)
    print("  EJERCICIO 6 — RAG BÁSICO (ChromaDB + embeddings)")
    print("=" * 64)

    rag = MotorRAG(nombre_coleccion="rag_basico")
    print(f"  Embedding: {rag.nombre_embedding}")

    texto = cargar_corpus()
    n = rag.indexar_texto(texto, fuente="corpus")
    print(f"  Texto indexado en {n} chunks. Total en BD: {rag.total_chunks()}")

    preguntas = (
        [args.pregunta]
        if args.pregunta
        else [
            "¿Qué es la programación multihilo?",
            "¿Cómo se comunican los procesos en red?",
            "¿Para qué sirve el cifrado autenticado?",
        ]
    )

    for pregunta in preguntas:
        print("\n" + "-" * 64)
        print(f"  PREGUNTA: {pregunta}")
        print("-" * 64)
        r = rag.consultar(pregunta, k=args.k)
        if not r.chunks:
            print("  (sin resultados)")
            continue
        for i, (chunk, dist) in enumerate(zip(r.chunks, r.distancias), 1):
            print(f"\n  [{i}] similitud (distancia={dist:.3f}):")
            print(f"      {chunk}")

    print("\n" + "=" * 64)
    print("  Estos son los 'cachos crudos'. El ejercicio 7 los redacta con IA.")
    print("=" * 64)


if __name__ == "__main__":
    main()
