#!/usr/bin/env python3
"""
servidor/api.py — Ejercicios 1-3: el rol de SERVIDOR
=====================================================

Simula el sistema de gestión empresarial "ERP de almacén". Expone una API REST
para que OTROS sistemas (o clientes) consulten y modifiquen su inventario.

  Ejercicio 1: mecanismo de comunicación entre sistemas (la propia API).
  Ejercicio 2: este programa es el SERVIDOR (sirve la API).
  Ejercicio 3: la API cumple un contrato documentado (ver contrato/openapi.yaml)
               y publica su documentación interactiva en /docs.

Uso:
    pip install flask
    python3 servidor/api.py
    API:    http://127.0.0.1:8000
    Docs:   http://127.0.0.1:8000/docs
    Contrato: http://127.0.0.1:8000/openapi.yaml

Endpoints:
    GET    /productos            Listar productos (filtros: ?categoria=&min_stock=)
    GET    /productos/<sku>      Obtener un producto por SKU
    POST   /productos            Crear un producto
    PUT    /productos/<sku>      Actualizar un producto
    DELETE /productos/<sku>      Borrar un producto
    GET    /health               Estado del servicio
"""

import os
import re
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_from_directory, Response

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)

app = Flask(__name__)

# "Base de datos" en memoria del ERP
PRODUCTOS: dict[str, dict] = {
    "TEC-001": {"sku": "TEC-001", "nombre": "Teclado mecánico", "categoria": "perifericos",
                "precio": 79.90, "stock": 34},
    "RAT-002": {"sku": "RAT-002", "nombre": "Ratón inalámbrico", "categoria": "perifericos",
                "precio": 24.50, "stock": 8},
    "MON-003": {"sku": "MON-003", "nombre": "Monitor 27 pulgadas", "categoria": "pantallas",
                "precio": 199.00, "stock": 0},
}

SKU_RE = re.compile(r"^[A-Z]{2,4}-\d{3,}$")


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat()


def error(mensaje: str, codigo: int):
    return jsonify({"error": mensaje, "timestamp": ahora()}), codigo


def validar_producto(datos: dict, parcial: bool = False) -> str | None:
    """Devuelve un mensaje de error o None si es válido."""
    campos = {
        "nombre": str, "categoria": str, "precio": (int, float), "stock": int,
    }
    for campo, tipo in campos.items():
        if campo in datos:
            if not isinstance(datos[campo], tipo):
                return f"El campo '{campo}' debe ser de tipo {getattr(tipo,'__name__',tipo)}"
            if campo in ("precio", "stock") and datos[campo] < 0:
                return f"El campo '{campo}' no puede ser negativo"
        elif not parcial:
            return f"Falta el campo obligatorio '{campo}'"
    return None


# ----------------------------- ENDPOINTS -----------------------------
@app.route("/health")
def health():
    return jsonify({"estado": "ok", "productos": len(PRODUCTOS), "timestamp": ahora()})


@app.route("/productos", methods=["GET"])
def listar():
    categoria = request.args.get("categoria")
    min_stock = request.args.get("min_stock", type=int)
    items = list(PRODUCTOS.values())
    if categoria:
        items = [p for p in items if p["categoria"] == categoria]
    if min_stock is not None:
        items = [p for p in items if p["stock"] >= min_stock]
    return jsonify({"total": len(items), "productos": items})


@app.route("/productos/<sku>", methods=["GET"])
def obtener(sku):
    p = PRODUCTOS.get(sku)
    if not p:
        return error(f"No existe el producto '{sku}'", 404)
    return jsonify(p)


@app.route("/productos", methods=["POST"])
def crear():
    datos = request.get_json(silent=True) or {}
    sku = (datos.get("sku") or "").strip().upper()
    if not SKU_RE.match(sku):
        return error("SKU inválido. Formato esperado: 'ABC-123'", 400)
    if sku in PRODUCTOS:
        return error(f"El producto '{sku}' ya existe", 409)
    msg = validar_producto(datos)
    if msg:
        return error(msg, 400)
    producto = {
        "sku": sku, "nombre": datos["nombre"], "categoria": datos["categoria"],
        "precio": float(datos["precio"]), "stock": int(datos["stock"]),
    }
    PRODUCTOS[sku] = producto
    return jsonify(producto), 201


@app.route("/productos/<sku>", methods=["PUT"])
def actualizar(sku):
    if sku not in PRODUCTOS:
        return error(f"No existe el producto '{sku}'", 404)
    datos = request.get_json(silent=True) or {}
    msg = validar_producto(datos, parcial=True)
    if msg:
        return error(msg, 400)
    for campo in ("nombre", "categoria", "precio", "stock"):
        if campo in datos:
            PRODUCTOS[sku][campo] = (
                float(datos[campo]) if campo == "precio"
                else int(datos[campo]) if campo == "stock"
                else datos[campo]
            )
    return jsonify(PRODUCTOS[sku])


@app.route("/productos/<sku>", methods=["DELETE"])
def borrar(sku):
    if sku not in PRODUCTOS:
        return error(f"No existe el producto '{sku}'", 404)
    eliminado = PRODUCTOS.pop(sku)
    return jsonify({"borrado": eliminado["sku"]})


# --------------------- CONTRATO Y DOCUMENTACIÓN ---------------------
@app.route("/openapi.yaml")
def contrato():
    return send_from_directory(os.path.join(RAIZ, "contrato"), "openapi.yaml",
                               mimetype="text/yaml")


@app.route("/docs")
def docs():
    """Documentación interactiva (Swagger UI) que lee el contrato OpenAPI."""
    html = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>API Almacén · Documentación</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
</head><body><div id="swagger"></div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
SwaggerUIBundle({ url: '/openapi.yaml', dom_id: '#swagger' });
</script></body></html>"""
    return Response(html, mimetype="text/html")


# CORS para que el cliente web pueda consumir la API
@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/productos", methods=["OPTIONS"])
@app.route("/productos/<sku>", methods=["OPTIONS"])
def preflight(sku=None):
    return ("", 204)


if __name__ == "__main__":
    print("=" * 60)
    print(" SERVIDOR DE LA API (ERP de almacén)")
    print("  API:      http://127.0.0.1:8080")
    print("  Docs:     http://127.0.0.1:8080/docs")
    print("  Contrato: http://127.0.0.1:8080/openapi.yaml")
    print("=" * 60)
    app.run(host="127.0.0.1", port=8080, debug=False)
