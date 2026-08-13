# Font

Tutte e tre di origine Google Fonts, free, sotto SIL Open Font License 1.1.

**Self-hostate, non da CDN.** Il Garante privacy considera il caricamento
remoto da Google Fonts un trasferimento di IP verso gli USA: il sito serve i
WOFF2 dal proprio dominio. In `motion/fonts/` stanno invece i TTF, perché Pango
(il motore di testo di Manim) non legge i WOFF2 (attribuzioni e licenza in
[`motion/fonts/NOTICE.md`](motion/fonts/NOTICE.md)).

**E in `stampa/fonts/` stanno le istanze statiche**, sedici, per la
composizione del libro in PDF: `fontspec` sotto LuaLaTeX di un font variabile
prende l'istanza di *default*, e il default di Fraunces è `wght 900, WONK 1`.
Non si scrivono a mano, le genera
[`stampa/genera-font.py`](stampa/genera-font.py); attribuzioni, assi congelati
e ragioni in [`stampa/fonts/NOTICE.md`](stampa/fonts/NOTICE.md).

| Ruolo | Famiglia | Pesi | Note |
|---|---|---|---|
| Display / headline | **Fraunces** | 400, 600, 800 | Variable, optical sizing (`opsz 9..144`), italic disponibile |
| Body | **Inter** | 400, 500, 600 | |
| Mono / codice | **JetBrains Mono** | 400, 500, 600 | |

Le famiglie sono referenziate nei token come `--pt-font-display`,
`--pt-font-body`, `--pt-font-mono` (vedi `tokens.css`), con fallback di sistema.

## URL Google Fonts (css2, `display=swap`, subset `latin,latin-ext`)

```
https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap&subset=latin,latin-ext
```
