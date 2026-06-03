# Unidad 005 — Programación segura (web)

**Proyecto:** Laboratorio de criptografía con **Web Crypto API**.

## Cómo abrir
Abre `index.html` en el navegador. Sin servidor ni librerías. Todo el cálculo es
local (no se envía nada a ningún sitio).

## Qué hace
Tres módulos con criptografía real (`crypto.subtle`):
1. **Hash de contraseñas** — PBKDF2-SHA256 con salt y 150.000 iteraciones; verificación.
2. **Cifrado autenticado** — AES-GCM 256 con clave derivada de contraseña. Incluye
   botones para *manipular un byte* y *probar clave errónea*: en ambos casos el
   descifrado se rechaza (integridad garantizada).
3. **Generador seguro** — contraseñas con `crypto.getRandomValues` (CSPRNG) y medidor
   de fortaleza en tiempo real.

## Conceptos
Hash con salt, cifrado simétrico, integridad (cifrado autenticado) y aleatoriedad segura.

> Buenas prácticas: nada de MD5/SHA1 a secas ni `Math.random` para material
> criptográfico. Salt, IV y claves vienen del CSPRNG del navegador.
