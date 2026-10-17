# Font

Tutte e tre di origine Google Fonts, free, sotto SIL Open Font License 1.1.

**Self-hostate, non da CDN.** Il Garante privacy considera il caricamento
remoto da Google Fonts un trasferimento di IP verso gli USA: i WOFF2 stanno
qui, in `fonts/`, e li dichiara [`fonts.css`](fonts.css), con i font di
ripiego tarati sulle metriche (niente salto di layout quando il font arriva).
Un consumatore web importa `fonts.css` accanto a `tokens.css` e non scrive
nessun `@font-face` suo; nessuna pagina carica `fonts.googleapis.com`.

In `motion/fonts/` stanno invece i TTF, perché Pango (il motore di testo di
Manim) non legge i WOFF2 (attribuzioni e licenza in
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
| Body | **Inter** | 400, 500, 600 | Il grassetto è il 600, a schermo e in stampa: niente 700 né 800 |
| Mono / codice | **JetBrains Mono** | 400, 500, 600 | |

**Fraunces ha due pesi di titolo, secondo dove sta.**

- **Lettura**: nella pagina lunga, cioè un capitolo del libro o un articolo
  lungo, h1 e h2 sono in **400**, il tondo leggero
  (`--pt-prose-heading-weight`), e h3–h5 in 600. Alla misura grande il 400
  regge senza gridare, e la gerarchia fra i titoli la fa la scala
  `--pt-prose-*` di `tokens.css`, non il peso.
- **Display**: landing, copertine e headline del sito hanno l'h1 in **800** e
  i titoli sotto in 600, sulla scala `--pt-display-*`.

Sul web Inter e JetBrains Mono non hanno il corsivo e il browser lo
sintetizza; il PDF ha i corsivi veri (`stampa/fonts/`).

Le famiglie sono referenziate nei token come `--pt-font-display`,
`--pt-font-body`, `--pt-font-mono` (vedi `tokens.css`), con fallback di sistema.

## URL Google Fonts (css2, `display=swap`, subset `latin,latin-ext`)

Da dove vengono i file, non da mettere in pagina: è la richiesta da cui sono
stati scaricati i WOFF2 di `fonts/`, e quella a cui si riferisce
`stampa/fonts/NOTICE.md` per gli assi.

```
https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap&subset=latin,latin-ext
```
