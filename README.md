# Proyectos web — Servicios y Procesos

Una **página web ejecutable** por cada unidad del módulo *Programación de
Servicios y Procesos*, inspirado en
[`jocarsa/serviciosyprocesos`](https://github.com/jocarsa/serviciosyprocesos).

Todo es **HTML / CSS / JavaScript puro**. No hay Python, ni backend, ni
`npm install`: cada unidad es un único `index.html` que se abre en el navegador.

| Unidad | Proyecto | Tecnología web | Conceptos |
|--------|----------|----------------|-----------|
| **001 — Multiproceso** | Procesado de imagen en paralelo | **Web Workers** | Procesos, reparto de trabajo, IPC, concurrencia |
| **002 — Multihilo** | Condiciones de carrera | **SharedArrayBuffer + Atomics** | Hilos, recurso compartido, sincronización |
| **003 — Comunicaciones en red** | Chat en tiempo real entre pestañas | **BroadcastChannel** | Cliente-servidor, broadcast, protocolo |
| **004 — Servicios en red** | Cliente de una API REST | **fetch** | REST, métodos HTTP, JSON, códigos de estado |
| **005 — Programación segura** | Laboratorio de cifrado | **Web Crypto API** | Hash + salt, AES-GCM, integridad, CSPRNG |

## Cómo usarlas
Abre el `index.html` de cada carpeta haciendo doble clic.

Notas por unidad:
- **001 y 002** corren cálculo real en hilos del navegador. La *aceleración* (001) y
  algunos comportamientos de memoria compartida (002) dependen de tu CPU/navegador;
  cada página lo explica e incluye respaldo cuando hace falta.
- **003** se prueba abriendo el archivo **en dos o más pestañas** del mismo navegador.
- **004** necesita **conexión a internet** (usa una API pública real).
- **005** funciona del todo offline.

## Requisitos
Un navegador moderno (Chrome, Firefox, Edge o Safari recientes). Nada más.

## Verificación
La lógica de cada unidad se validó de forma independiente antes de entregarse:
el reparto por bloques de la 001 produce el mismo resultado que la versión
secuencial, y en la 005 el hash, el cifrado AES-GCM y la detección de
manipulación/clave errónea pasan sus pruebas.
