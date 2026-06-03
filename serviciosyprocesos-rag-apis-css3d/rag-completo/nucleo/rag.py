"""
nucleo/rag.py — Motor RAG (Retrieval-Augmented Generation)
============================================================

Cubre los ejercicios:
  6) RAG básico: trocear texto -> embeddings -> ChromaDB -> consultas semánticas
  7) RAG + IA:   pasar los chunks recuperados a un LLM para redactar la respuesta

Embeddings:
  - Por defecto usa sentence-transformers (modelo all-MiniLM-L6-v2).
  - Si no está instalado o no hay internet, cae en un embedding TF de
    respaldo (hashing) para que el ejercicio funcione igualmente y se vea
    el flujo completo. En clase/producción se usa el modelo real.

IA (paso del ejercicio 7):
  - Usa Ollama en local (http://localhost:11434) con el modelo indicado
    (por defecto 'llama3.1:8b', igual que el repositorio original).
  - Si Ollama no está disponible, devuelve una respuesta extractiva
    construida a partir de los chunks, dejando claro que es el modo sin IA.
"""

from __future__ import annotations
import hashlib
import math
import re
import json
import urllib.request
from dataclasses import dataclass, field

import chromadb
from chromadb.utils import embedding_functions


# ---------------------------------------------------------------------
#  1) Troceado de texto (chunking)
# ---------------------------------------------------------------------
def trocear(texto: str, tam: int = 400, solape: int = 80) -> list[str]:
    """Divide el texto en chunks de ~`tam` caracteres con `solape` entre ellos.

    El solapamiento evita perder contexto en las fronteras entre chunks.
    Se intenta cortar en límites de frase para que los trozos sean legibles.
    """
    texto = re.sub(r"\s+", " ", texto).strip()
    if not texto:
        return []

    chunks: list[str] = []
    inicio = 0
    n = len(texto)
    while inicio < n:
        fin = min(inicio + tam, n)
        # intentar terminar en un punto/cierre de frase cercano
        if fin < n:
            corte = texto.rfind(". ", inicio, fin)
            if corte == -1:
                corte = texto.rfind(" ", inicio, fin)
            if corte > inicio + tam // 2:
                fin = corte + 1
        chunk = texto[inicio:fin].strip()
        if chunk:
            chunks.append(chunk)
        if fin >= n:
            break
        inicio = max(fin - solape, inicio + 1)
    return chunks


# ---------------------------------------------------------------------
#  2) Funciones de embedding
# ---------------------------------------------------------------------
class EmbeddingRespaldo(embedding_functions.EmbeddingFunction):
    """Embedding de respaldo SIN dependencias ni red (term-frequency hashing).

    No es semánticamente tan bueno como un modelo real, pero permite que el
    ejercicio funcione en cualquier máquina. Vector L2-normalizado de 256 dims.
    """

    DIM = 256

    def __init__(self) -> None:
        pass

    def __call__(self, input: list[str]) -> list[list[float]]:  # noqa: A002
        salida = []
        for texto in input:
            vec = [0.0] * self.DIM
            for palabra in re.findall(r"\w+", texto.lower()):
                h = int(hashlib.md5(palabra.encode()).hexdigest(), 16)
                vec[h % self.DIM] += 1.0
            norma = math.sqrt(sum(x * x for x in vec)) or 1.0
            salida.append([x / norma for x in vec])
        return salida


def obtener_embedding_function(preferir_modelo: bool = True):
    """Devuelve (función_embedding, nombre_legible).

    Intenta sentence-transformers; si falla, usa el de respaldo.
    """
    if preferir_modelo:
        try:
            ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            # forzar carga para detectar fallos de descarga ya mismo
            ef(["prueba"])
            return ef, "sentence-transformers/all-MiniLM-L6-v2"
        except Exception:
            pass
    return EmbeddingRespaldo(), "respaldo-hashing (sin modelo)"


# ---------------------------------------------------------------------
#  3) Cliente del LLM (Ollama) — paso de IA del ejercicio 7
# ---------------------------------------------------------------------
def ollama_disponible(url: str = "http://localhost:11434") -> bool:
    try:
        with urllib.request.urlopen(f"{url}/api/tags", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def generar_con_ollama(
    pregunta: str,
    contexto: str,
    modelo: str = "llama3.1:8b",
    url: str = "http://localhost:11434",
) -> str:
    """Pide al LLM que responda usando SOLO el contexto recuperado."""
    prompt = (
        "Eres un asistente que responde preguntas usando únicamente el "
        "CONTEXTO proporcionado. Si la respuesta no está en el contexto, "
        "dilo claramente. Responde en español, de forma clara y concisa.\n\n"
        f"CONTEXTO:\n{contexto}\n\n"
        f"PREGUNTA: {pregunta}\n\nRESPUESTA:"
    )
    datos = json.dumps({"model": modelo, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        f"{url}/api/generate", data=datos,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    return resp.get("response", "").strip()


def respuesta_extractiva(pregunta: str, chunks: list[str]) -> str:
    """Respuesta de respaldo SIN IA: simplemente presenta los chunks.

    Deja explícito que es el modo crudo (raw), que es justo lo que el
    ejercicio 7 quiere mejorar pasándolo por un LLM.
    """
    cuerpo = "\n\n".join(f"• {c}" for c in chunks)
    return (
        "[Modo sin IA — fragmentos crudos recuperados]\n\n"
        f"{cuerpo}\n\n"
        "(Con Ollama activo, estos fragmentos se redactarían como una "
        "respuesta natural y unificada.)"
    )


# ---------------------------------------------------------------------
#  4) Clase principal del RAG
# ---------------------------------------------------------------------
@dataclass
class ResultadoConsulta:
    pregunta: str
    chunks: list[str]
    distancias: list[float]
    respuesta_ia: str | None = None
    fuente_ia: str = ""
    metadatos: list[dict] = field(default_factory=list)


class MotorRAG:
    """Encapsula todo el ciclo RAG sobre una colección de ChromaDB."""

    def __init__(
        self,
        nombre_coleccion: str = "documentos",
        ruta_persistencia: str | None = None,
        preferir_modelo: bool = True,
    ) -> None:
        self.ef, self.nombre_embedding = obtener_embedding_function(preferir_modelo)
        if ruta_persistencia:
            self.cliente = chromadb.PersistentClient(path=ruta_persistencia)
        else:
            self.cliente = chromadb.Client()
        self.coleccion = self.cliente.get_or_create_collection(
            name=nombre_coleccion, embedding_function=self.ef
        )

    # ---- Indexación (ejercicio 6: meter embeddings en ChromaDB) ----
    def indexar_texto(
        self, texto: str, fuente: str = "documento", tam: int = 400, solape: int = 80
    ) -> int:
        chunks = trocear(texto, tam, solape)
        if not chunks:
            return 0
        base = self.coleccion.count()
        ids = [f"{fuente}-{base + i}" for i in range(len(chunks))]
        metadatos = [{"fuente": fuente, "indice": i} for i in range(len(chunks))]
        self.coleccion.add(documents=chunks, ids=ids, metadatas=metadatos)
        return len(chunks)

    # ---- Recuperación (ejercicio 6: query semántica) ----
    def consultar(self, pregunta: str, k: int = 4) -> ResultadoConsulta:
        n = min(k, max(self.coleccion.count(), 1))
        res = self.coleccion.query(query_texts=[pregunta], n_results=n)
        chunks = res["documents"][0] if res["documents"] else []
        dists = res["distances"][0] if res.get("distances") else []
        metas = res["metadatos"][0] if res.get("metadatos") else (
            res["metadatas"][0] if res.get("metadatas") else []
        )
        return ResultadoConsulta(
            pregunta=pregunta, chunks=chunks, distancias=dists, metadatos=metas
        )

    # ---- RAG + IA (ejercicio 7) ----
    def consultar_con_ia(
        self, pregunta: str, k: int = 4, modelo: str = "llama3.1:8b"
    ) -> ResultadoConsulta:
        r = self.consultar(pregunta, k)
        contexto = "\n\n".join(r.chunks)
        if contexto and ollama_disponible():
            try:
                r.respuesta_ia = generar_con_ollama(pregunta, contexto, modelo)
                r.fuente_ia = f"ollama:{modelo}"
            except Exception as e:  # noqa: BLE001
                r.respuesta_ia = respuesta_extractiva(pregunta, r.chunks)
                r.fuente_ia = f"respaldo (error Ollama: {e})"
        else:
            r.respuesta_ia = respuesta_extractiva(pregunta, r.chunks)
            r.fuente_ia = "respaldo (Ollama no disponible)"
        return r

    def vaciar(self) -> None:
        nombre = self.coleccion.name
        self.cliente.delete_collection(nombre)
        self.coleccion = self.cliente.get_or_create_collection(
            name=nombre, embedding_function=self.ef
        )

    def total_chunks(self) -> int:
        return self.coleccion.count()
