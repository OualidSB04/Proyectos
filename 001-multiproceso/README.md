# Unidad 001 — Programación multiproceso (web)

**Proyecto:** Procesado de imagen en paralelo con **Web Workers**.

## Cómo abrir
Abre `index.html` en el navegador (doble clic). No necesita servidor ni instalación.

## Qué hace
Aplica un filtro a una imagen de dos formas y compara los tiempos:
- **Un solo hilo:** todo el procesado en el hilo principal.
- **Varios workers:** la imagen se divide en bloques de filas y cada Web Worker
  (un proceso independiente) procesa el suyo en paralelo.

Controles: filtro (grises, invertir, sepia, umbral), carga de trabajo y número de workers.

## Conceptos
Proceso, reparto de trabajo, paso de mensajes (`postMessage`/IPC) y concurrencia.

> La aceleración real depende de los núcleos de tu CPU. Con 1 núcleo los tiempos
> son parecidos; lo que se demuestra es el reparto y la coordinación de procesos.
