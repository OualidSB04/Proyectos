# Proyectos — Servicios y Procesos (RAG, APIs y CSS 3D)

Tres proyectos que cubren los ejercicios de evaluación:

| Carpeta | Ejercicios | Qué es | Stack |
|---------|-----------|--------|-------|
| **`apis-rest/`** | 1, 2, 3 | Comunicación entre sistemas vía API REST: servidor, cliente y contrato OpenAPI | Python (Flask) + cliente web |
| **`rag-completo/`** | 6, 7, 8 | RAG básico → RAG + IA → RAG empaquetado en Flask | Python (ChromaDB + Ollama + Flask) |
| **`css3d/`** | 9 | Espacio vectorial de un RAG en 3D | HTML/CSS/JS (CSS 3D puro) |

Cada carpeta tiene su propio `README.md` con instrucciones detalladas.

---

## apis-rest — Ejercicios 1, 2 y 3
Un ERP de almacén que expone su inventario por una API REST.
- **Servidor** (`servidor/api.py`) sirve la API.
- **Cliente** (`cliente/cliente.py` y `cliente/cliente_web.html`) la consume.
- **Contrato** (`contrato/openapi.yaml`) documenta la API; visible en `/docs`.

```bash
cd apis-rest
pip install -r requirements.txt
python3 servidor/api.py          # terminal 1  -> http://127.0.0.1:8000/docs
python3 cliente/cliente.py       # terminal 2
```

## rag-completo — Ejercicios 6, 7 y 8
El ciclo RAG de menos a más, sobre un motor común (`nucleo/rag.py`).
- **6** recuperación de chunks con ChromaDB.
- **7** los chunks pasan por un LLM (Ollama) para redactar la respuesta.
- **8** interfaz Flask para que cualquiera entrene su propio RAG.

```bash
cd rag-completo
pip install -r requirements.txt
python3 06_rag_basico.py
python3 07_rag_con_ia.py
python3 08_rag_flask.py          # -> http://127.0.0.1:5000
```

## css3d — Ejercicio 9
Visualización 3D navegable del flujo RAG (documento → chunks → vectores → query),
hecha solo con transforms CSS. Abre `css3d/index.html` en el navegador.

---

## Requisitos
- **Python 3.10+** para `apis-rest` y `rag-completo`.
- Un **navegador moderno** para los clientes web y `css3d`.
- **Opcional:** [Ollama](https://ollama.com) con `llama3.1:8b` para la IA real de
  los ejercicios 7 y 8; y `sentence-transformers` para embeddings de calidad. Ambos
  tienen respaldo automático, así que los proyectos funcionan sin ellos (indicándolo).

## Notas de honestidad técnica
- El **RAG real** necesita Python + ChromaDB; por eso esos ejercicios no son web pura.
  Se probaron el chunking, el indexado y la recuperación (los chunks correctos suben
  al top en las consultas).
- La **parte de IA** (7 y 8) requiere Ollama corriendo. Sin él, se muestran los
  fragmentos crudos en modo respaldo: así se ve exactamente qué añade la IA.
- En **css3d** la "similitud" es una aproximación por palabras para funcionar sin
  backend; el concepto (cercanía en el espacio vectorial) es el mismo que en 6-8.
- La **API** (1-3) se verificó de extremo a extremo: el cliente Python ejecuta
  GET/POST/PUT/DELETE contra el servidor y recibe los códigos correctos (200, 201,
  404, 409), y `/docs` sirve el contrato.
