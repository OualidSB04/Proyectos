#!/usr/bin/env python3
"""
08_rag_flask.py — Ejercicio 8: RAG empaquetado (interfaz Flask)
================================================================

Una interfaz web para que cualquier usuario, sin saber programar, pueda:
  1. Pegar o subir su propio texto
  2. "Entrenar" su RAG (trocear + embeddings + guardar en ChromaDB)
  3. Hacer preguntas y obtener respuestas (con IA si Ollama está disponible)

Empaqueta el motor del ejercicio 6 y 7 detrás de una API REST + página web.

Uso:
    pip install flask
    python3 08_rag_flask.py
    Abrir: http://127.0.0.1:5000

Endpoints de la API:
    POST /api/entrenar   {"texto": "...", "fuente": "..."}  -> indexa el texto
    POST /api/preguntar  {"pregunta": "...", "ia": true}    -> recupera + (IA)
    POST /api/reiniciar                                     -> vacía la BD
    GET  /api/estado                                        -> nº de chunks, etc.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, request, jsonify, render_template
except ImportError:
    print("Falta Flask. Instala con:  pip install flask")
    sys.exit(1)

from nucleo.rag import MotorRAG, ollama_disponible  # noqa: E402

app = Flask(__name__, template_folder="plantillas", static_folder="static")

# Motor RAG persistente (guarda la BD en disco entre reinicios)
RUTA_BD = os.path.join(os.path.dirname(__file__), "datos", "chroma_db")
motor = MotorRAG(
    nombre_coleccion="rag_usuario",
    ruta_persistencia=RUTA_BD,
)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/api/estado")
def estado():
    return jsonify(
        {
            "chunks": motor.total_chunks(),
            "embedding": motor.nombre_embedding,
            "ollama": ollama_disponible(),
        }
    )


@app.route("/api/entrenar", methods=["POST"])
def entrenar():
    datos = request.get_json(silent=True) or {}
    texto = (datos.get("texto") or "").strip()
    fuente = (datos.get("fuente") or "usuario").strip()
    tam = int(datos.get("tam", 400))
    solape = int(datos.get("solape", 80))

    if not texto:
        return jsonify({"error": "El texto está vacío"}), 400
    if len(texto) < 50:
        return jsonify({"error": "El texto es demasiado corto (mín. 50 caracteres)"}), 400

    n = motor.indexar_texto(texto, fuente=fuente, tam=tam, solape=solape)
    return jsonify(
        {
            "ok": True,
            "chunks_añadidos": n,
            "total_chunks": motor.total_chunks(),
            "embedding": motor.nombre_embedding,
        }
    ), 201


@app.route("/api/preguntar", methods=["POST"])
def preguntar():
    datos = request.get_json(silent=True) or {}
    pregunta = (datos.get("pregunta") or "").strip()
    usar_ia = bool(datos.get("ia", True))
    k = int(datos.get("k", 4))
    modelo = datos.get("modelo", "llama3.1:8b")

    if not pregunta:
        return jsonify({"error": "La pregunta está vacía"}), 400
    if motor.total_chunks() == 0:
        return jsonify({"error": "Primero entrena el RAG con algún texto"}), 400

    if usar_ia:
        r = motor.consultar_con_ia(pregunta, k=k, modelo=modelo)
    else:
        r = motor.consultar(pregunta, k=k)

    return jsonify(
        {
            "pregunta": r.pregunta,
            "chunks": r.chunks,
            "distancias": [round(d, 4) for d in r.distancias],
            "respuesta_ia": r.respuesta_ia,
            "fuente_ia": r.fuente_ia,
        }
    )


@app.route("/api/reiniciar", methods=["POST"])
def reiniciar():
    motor.vaciar()
    return jsonify({"ok": True, "total_chunks": 0})


if __name__ == "__main__":
    print("=" * 60)
    print("  EJERCICIO 8 — RAG EMPAQUETADO (Flask)")
    print(f"  Embedding: {motor.nombre_embedding}")
    print(f"  Ollama: {'disponible' if ollama_disponible() else 'no disponible (modo respaldo)'}")
    print("  Abre: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
