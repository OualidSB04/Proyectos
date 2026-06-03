#!/usr/bin/env python3
"""
cliente/cliente.py — Ejercicio 2: el rol de CLIENTE
====================================================

Este programa NO sirve nada: CONSUME la API del servidor (servidor/api.py).
Representa a otro sistema empresarial que se comunica con el ERP de almacén
a través de su API REST, siguiendo el contrato publicado.

Demuestra el ciclo completo de un cliente: GET, POST, PUT, DELETE, manejo de
códigos de estado y de errores.

Uso (con el servidor arrancado en otra terminal):
    python3 cliente/cliente.py
"""

import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8080"


class ClienteAPI:
    """Pequeño SDK que envuelve las llamadas HTTP a la API del almacén."""

    def __init__(self, base: str = BASE) -> None:
        self.base = base

    def _peticion(self, metodo: str, ruta: str, cuerpo: dict | None = None):
        url = f"{self.base}{ruta}"
        datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
        req = urllib.request.Request(url, data=datos, method=metodo)
        if datos:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode())
        except urllib.error.URLError as e:
            raise SystemExit(
                f"No se pudo conectar a {self.base}. "
                f"¿Está arrancado el servidor? ({e.reason})"
            )

    # Métodos del contrato
    def salud(self):
        return self._peticion("GET", "/health")

    def listar(self, categoria=None, min_stock=None):
        q = []
        if categoria:
            q.append(f"categoria={categoria}")
        if min_stock is not None:
            q.append(f"min_stock={min_stock}")
        ruta = "/productos" + ("?" + "&".join(q) if q else "")
        return self._peticion("GET", ruta)

    def obtener(self, sku):
        return self._peticion("GET", f"/productos/{sku}")

    def crear(self, producto: dict):
        return self._peticion("POST", "/productos", producto)

    def actualizar(self, sku, cambios: dict):
        return self._peticion("PUT", f"/productos/{sku}", cambios)

    def borrar(self, sku):
        return self._peticion("DELETE", f"/productos/{sku}")


def seccion(titulo: str):
    print("\n" + "-" * 60)
    print(f"  {titulo}")
    print("-" * 60)


def main() -> None:
    api = ClienteAPI()

    print("=" * 60)
    print("  EJERCICIO 2 — CLIENTE consumiendo la API del almacén")
    print("=" * 60)

    seccion("1) Comprobar estado del servicio (GET /health)")
    cod, datos = api.salud()
    print(f"  [{cod}] {datos}")

    seccion("2) Listar todos los productos (GET /productos)")
    cod, datos = api.listar()
    print(f"  [{cod}] {datos['total']} productos:")
    for p in datos["productos"]:
        print(f"     {p['sku']:>8}  {p['nombre']:<22} {p['precio']:>7.2f}€  stock={p['stock']}")

    seccion("3) Filtrar por stock disponible (GET /productos?min_stock=1)")
    cod, datos = api.listar(min_stock=1)
    print(f"  [{cod}] {datos['total']} productos con stock:")
    for p in datos["productos"]:
        print(f"     {p['sku']} — {p['nombre']}")

    seccion("4) Crear un producto (POST /productos)")
    nuevo = {"sku": "ALT-004", "nombre": "Altavoces Bluetooth",
             "categoria": "audio", "precio": 45.0, "stock": 12}
    cod, datos = api.crear(nuevo)
    print(f"  [{cod}] creado: {datos}")

    seccion("5) Intentar crear duplicado (POST → error 409)")
    cod, datos = api.crear(nuevo)
    print(f"  [{cod}] {datos['error']}")

    seccion("6) Actualizar stock (PUT /productos/ALT-004)")
    cod, datos = api.actualizar("ALT-004", {"stock": 30})
    print(f"  [{cod}] actualizado: stock ahora = {datos['stock']}")

    seccion("7) Pedir un producto inexistente (GET → error 404)")
    cod, datos = api.obtener("XYZ-999")
    print(f"  [{cod}] {datos['error']}")

    seccion("8) Borrar el producto creado (DELETE /productos/ALT-004)")
    cod, datos = api.borrar("ALT-004")
    print(f"  [{cod}] {datos}")

    print("\n" + "=" * 60)
    print("  Cliente y servidor se han comunicado por la API. ✓")
    print("=" * 60)


if __name__ == "__main__":
    main()
