# Unidad 004 — Generación de servicios en red (web)

**Proyecto:** Cliente de un servicio REST.

## Cómo abrir
Abre `index.html` en el navegador. **Requiere conexión a internet** (consume una
API pública real).

## Qué hace
La página es el **cliente** de un servicio web. Llama a la API REST pública
`jsonplaceholder.typicode.com` con `fetch` usando los métodos HTTP:
- **GET** (leer), **POST** (crear), **PUT** (actualizar), **DELETE** (borrar).

Muestra la petición (URL, método, cuerpo) y la respuesta (código de estado,
tiempo y JSON recibido).

## Conceptos
API REST, métodos HTTP, formato JSON y códigos de estado.

> JSONPlaceholder es una API de pruebas: responde como si guardara los cambios
> pero no persiste. Perfecta para practicar el lado **cliente** de un servicio.
