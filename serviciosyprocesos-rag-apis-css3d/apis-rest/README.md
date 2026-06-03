# APIs REST — Ejercicios 1, 2 y 3

Comunicación entre sistemas empresariales mediante una API REST. Simula un
**ERP de almacén** que expone su inventario para que otros sistemas lo consuman.

- **1 · Mecanismo de comunicación:** la propia API REST.
- **2 · Roles servidor y cliente:** `servidor/api.py` *sirve* la API;
  `cliente/cliente.py` (y `cliente/cliente_web.html`) la *consumen*.
- **3 · Contrato documentado:** `contrato/openapi.yaml` (OpenAPI 3.0), publicado
  como documentación interactiva en `/docs` para desarrolladores externos.

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecutar
**1) Arranca el servidor** (una terminal):
```bash
python3 servidor/api.py
# API:      http://127.0.0.1:8000
# Docs:     http://127.0.0.1:8000/docs
# Contrato: http://127.0.0.1:8000/openapi.yaml
```

**2) Consume la API** con cualquiera de los dos clientes:
```bash
# Cliente de consola (otra terminal)
python3 cliente/cliente.py
```
o abre **`cliente/cliente_web.html`** en el navegador (cliente visual).

## El contrato (ejercicio 3)
`contrato/openapi.yaml` describe cada endpoint, sus parámetros, los cuerpos de
petición/respuesta y los códigos de estado. Un desarrollador externo puede leerlo
(o verlo en `/docs` con Swagger UI) e integrarse sin necesidad de ver el código.

## Endpoints
| Método | Ruta               | Acción                        |
|--------|--------------------|-------------------------------|
| GET    | `/health`          | Estado del servicio           |
| GET    | `/productos`       | Listar (`?categoria=&min_stock=`) |
| GET    | `/productos/{sku}` | Obtener uno                   |
| POST   | `/productos`       | Crear                         |
| PUT    | `/productos/{sku}` | Actualizar (parcial)          |
| DELETE | `/productos/{sku}` | Borrar                        |

Respuestas en JSON. Errores con `{ "error": "...", "timestamp": "..." }` y el
código HTTP adecuado (400, 404, 409).
