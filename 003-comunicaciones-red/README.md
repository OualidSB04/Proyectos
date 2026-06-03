# Unidad 003 — Comunicaciones en red (web)

**Proyecto:** Chat en tiempo real entre pestañas.

## Cómo abrir
Abre `index.html` **en dos o más pestañas** del mismo navegador. Pon un nombre,
pulsa *Conectar* y chatea entre ellas.

## Qué hace
Cada pestaña es un **cliente**. Los mensajes se difunden a todos los clientes a
través de un canal compartido (`BroadcastChannel`), igual que un servidor reenvía
mensajes por sockets. El panel derecho muestra el **protocolo**: las tramas
`JOIN`, `MSG`, `LEAVE`, etc. que entran y salen.

## Conceptos
Modelo cliente-servidor, difusión (broadcast), protocolo de aplicación y presencia.

> `BroadcastChannel` comunica pestañas del **mismo navegador y origen**. Es la forma
> de demostrar comunicación cliente-servidor sin montar un backend. El concepto es
> idéntico al de un chat por sockets TCP.
