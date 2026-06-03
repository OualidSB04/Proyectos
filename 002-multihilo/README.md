# Unidad 002 — Programación multihilo (web)

**Proyecto:** Memoria compartida y condiciones de carrera.

## Cómo abrir
Abre `index.html` en el navegador. Sin servidor ni instalación.

## Qué hace
Varios hilos (Web Workers) incrementan **el mismo contador** en memoria
compartida (`SharedArrayBuffer`):
- **Sin Lock:** leen/escriben en pasos separados → se pisan → *condición de carrera*
  (se pierden incrementos).
- **Con `Atomics`:** el incremento es atómico (indivisible), como un Lock → resultado
  siempre correcto.

## Conceptos
Hilo, recurso compartido, condición de carrera y sincronización.

> Si el navegador no habilita `SharedArrayBuffer` (requiere cabeceras COOP/COEP),
> la página muestra automáticamente una **simulación** del mismo fenómeno.
> Abierto como archivo local funciona en la mayoría de navegadores; en algunos
> entornos verás la simulación.
