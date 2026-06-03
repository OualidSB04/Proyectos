# RAG completo — Ejercicios 6, 7 y 8

Un solo proyecto que cubre los tres ejercicios de RAG, de menos a más:

- **6 · RAG básico** (`06_rag_basico.py`): trocea un texto, calcula embeddings,
  los guarda en **ChromaDB** y recupera los chunks más similares a una pregunta.
- **7 · RAG + IA** (`07_rag_con_ia.py`): pasa esos chunks a un **LLM (Ollama)**
  para que redacte una respuesta natural en lugar de devolver fragmentos crudos.
- **8 · RAG empaquetado** (`08_rag_flask.py`): una **interfaz Flask** para que
  cualquier persona entrene su propio RAG (pegar texto → entrenar → preguntar).

El motor común está en `nucleo/rag.py`.

## Instalación
```bash
pip install -r requirements.txt
```

`sentence-transformers` es **opcional**: da embeddings de calidad, pero si no está
instalado (o no hay internet la primera vez), el motor usa un embedding de respaldo
para que todo funcione igualmente. Verás qué embedding se está usando al arrancar.

## Ejecutar
```bash
python3 06_rag_basico.py                    # demo de recuperación
python3 06_rag_basico.py --pregunta "..."   # tu propia pregunta

python3 07_rag_con_ia.py                    # con respuesta de IA
python3 07_rag_con_ia.py --pregunta "..." --modelo llama3.1:8b

python3 08_rag_flask.py                     # interfaz web -> http://127.0.0.1:5000
```

## Activar la IA (ejercicios 7 y 8)
La parte de IA usa **Ollama** en local (igual que el repositorio original con
`llama3.1:8b`):
1. Instala Ollama: <https://ollama.com>
2. Descarga el modelo: `ollama pull llama3.1:8b`
3. Deja el servicio activo (`ollama serve`).

Sin Ollama, los ejercicios 7 y 8 funcionan igual pero muestran los fragmentos
crudos, indicando que están en modo respaldo. Esto deja claro **qué aporta la IA**:
convertir los chunks en una respuesta legible.

## Cómo funciona (resumen del flujo RAG)
1. **Chunking** — el texto se parte en trozos con solapamiento (`nucleo/rag.py: trocear`).
2. **Embeddings** — cada chunk se convierte en un vector que captura su significado.
3. **Indexado** — los vectores se guardan en ChromaDB.
4. **Recuperación** — la pregunta se vectoriza y ChromaDB devuelve los chunks más cercanos.
5. **Generación (7 y 8)** — un LLM redacta la respuesta usando solo esos chunks.

> La base de datos de la app Flask se guarda en `datos/chroma_db/` (persistente).
