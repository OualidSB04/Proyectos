# CSS 3D — Ejercicio 9

**Espacio vectorial de un RAG** visualizado en 3D usando únicamente transforms
de CSS (sin WebGL ni librerías).

## Cómo abrir
Abre `index.html` en el navegador.

## Qué muestra
El recorrido de un RAG, en un entorno 3D navegable:
1. **Documento** (amarillo) — el texto original.
2. **Chunks** (verde) — el documento troceado.
3. **Vectores** (azul) — cada chunk convertido en un punto en el espacio vectorial,
   distribuido en una esfera.
4. **Query** (rosa) — tu pregunta en el centro; al buscar, ilumina los vectores
   semánticamente más cercanos y dibuja rayos hacia ellos.

## Controles
- **Arrastrar** con el ratón (o el dedo) → girar la escena.
- **Rueda** del ratón → acercar/alejar.
- **Buscar** → escribe una pregunta y pulsa el botón; prueba con "proceso",
  "cifrado", "red", "embeddings"…
- **Auto-girar** → activa/desactiva la rotación automática.

## Conceptos de CSS 3D aplicados
`perspective`, `transform-style: preserve-3d`, `translate3d`, `rotateX/Y/Z`,
`backface-visibility`, y composición de elementos en profundidad. La "búsqueda"
relaciona el ejercicio con RAG e IA: ilumina los vectores más afines a la pregunta.

> La similitud aquí es una aproximación por palabras (para que funcione sin
> backend). En un RAG real la cercanía se mide entre vectores de embeddings,
> como en los ejercicios 6-8.
