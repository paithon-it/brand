# paithon — brand

Fonte unica della firma visiva di paithon (sito, libro, social, tutto ciò che
verrà). Si cambia **qui**, i consumatori la riprendono.

Repo **pubblico** — deve esserlo, perché il libro lo consuma come submodule e
chi clona `paithonbook` deve poterlo risolvere. Pubblico non vuol dire libero:
il materiale paithon è *all rights reserved* (vedi [`LICENSE`](LICENSE)). Fanno
eccezione i font, che sono di terze parti sotto SIL Open Font License 1.1 (in
`fonts/`, `motion/fonts/` e `stampa/fonts/`, ciascuna cartella con la sua
licenza e il suo `NOTICE.md`).

Prima di aggiungere un file qui: **finisce online**. Niente chiavi, niente
bozze, niente materiale di cui non abbiamo i diritti.

## Contenuto

| File | Cos'è |
|---|---|
| `tokens.css` | **La fonte.** Tutti i design token come CSS custom properties (`--pt-*`): colori (light/dark), tipografia, spacing, layout, radius, shadow, transizioni, tavolozza del codice. Nessun valore va duplicato altrove — si legge da qui. |
| `fonts.css` + `fonts/` | **I font web**, ospitati in proprio: `@font-face` dei WOFF2 di Fraunces, Inter e JetBrains Mono, più i font di ripiego tarati sulle metriche. Si importa accanto a `tokens.css`. Dettagli in `fonts.md`. |
| `aurora.css` | Lo sfondo «gas colorato» con la grana di carta: due giri di deriva e si ferma. |
| `figure/` | **La palette delle figure e la sua resa scura** (`palette.json`, letto da `palette.py`): una mappa sola per chi ricolora una figura, sito, libro o motori di `motion/`. Dettagli in `figure/README.md`. |
| `logos/paithon-mark.svg` | Il segno: triangolo di Penrose (tribar GEB), palette-locked, identico in light/dark. Stesso mark di header sito, favicon e copertina libro. |
| `logos/paithon-wordmark.svg` | Il wordmark «paithon» con il tribar al posto della «a». Convenzioni in `logos/README.md`. |
| `fonts.md` | Le 3 famiglie, i pesi, da dove vengono i file. |
| `motion/` | **Lo stile delle animazioni.** I due motori delle figure animate: SVG (`paithon_svg.py`, il default) e Manim (`paithon_anim.py`), più gli stessi tempi e la stessa curva per il web (`motion.css`) e i TTF per il rendering. Dettagli in `motion/README.md`. |
| `print.css` / `print.js` | **La stampa.** Il nucleo condiviso del foglio: i token tornano ai valori chiari e il JS scambia il tema per la durata della stampa, così segue anche ciò che i token non raggiungono. I selettori di ciascun consumatore restano da lui. |
| `stampa/` | Le istanze statiche dei font per la composizione in PDF (LuaLaTeX). |
| `prove/` | Le prove del brand: `python3 -m unittest discover -s prove`. Controllano quello che a occhio non si vede (i due blocchi scuri uguali, i contrasti nei tre temi, la mappa delle figure allineata ai token, i file dei font). |
| `social/` | Template per Instagram/YouTube/etc. (export PNG/SVG). |

## Palette (subset memorabile — l'elenco completo è in `tokens.css`)

Illustrazioni editoriali: **solo** questi 5 + i neutri delle illustrazioni
(`--pt-illus-ink-medio`, `-ink-tenue`, `-filetto`, `-filetto-forte`,
`-ocra-cupo`). La loro resa scura è in `figure/palette.json`. Niente gradienti
AI-style, neon, glassmorphism.

- `#B5532C` terracotta — accent primario
- `#1F5E58` verde petrolio — secondario (mirato: eyebrow, pill, marker)
- `#C9A961` ocra — terziario, come campitura; come testo `--pt-accent-3-ink` `#7A5E1F`
- `#1A1714` warm black
- `#F4F1E8` cream

## Font

Fraunces (display) · Inter (body) · JetBrains Mono (codice). Tutti Google
Fonts, free. Dettagli e URL in `fonts.md`.

## Token 2026 (modernizzazione)

Oltre a colori/tipo/spacing storici, `tokens.css` include ora:

- **Display fluidi** `--pt-display-{sm,md,lg,xl}` (`clamp`): headline che scalano
  senza salti di breakpoint.
- **Tipografia di lettura** `--pt-prose-*`: la scala della pagina lunga (corpo
  17→18px, interlinea, distanza fra capoversi, h1-h5, peso dei titoli
  maggiori, filetto del h2, l'h2 `--pt-prose-h2-color`, verde petrolio sul chiaro e oro sullo
  scuro). La usano il
  libro e gli articoli lunghi del sito. Le prove controllano che scenda a
  ogni gradino, a ogni larghezza, e che l'h2 si legga nei due temi.
- **Enfasi nel testo** `--pt-prose-strong-weight` e
  `--pt-prose-underline-{color,thickness,offset}`: il grassetto in 600 (Inter
  non ha il 700) e la sottolineatura a matita, un tratto teal staccato dalle
  lettere sotto la frase che regge una sezione. Il selettore lo scrive il
  consumatore (`strong, b` e `u`), i valori stanno qui. Le prove controllano
  che il peso sia uno di quelli serviti da `fonts.css` e che la matita si
  veda in tutti i temi senza confondersi con i link o con l'ocra.
- **Superfici tint** `--pt-tint-accent{,-2,-3}`: accent a bassa opacità per
  hover/badge/stati attivi (via `color-mix`, seguono light/dark).
- **Focus ring** `--pt-ring` / `--pt-ring-offset`: anello unico token-driven.
- **Spaziatura di sezione fluida** `--pt-space-section{,-lg}`, `--pt-shadow-xs`.
- **`color-scheme` / `accent-color`** nativi per light/dark.
- Accent UI accessibile **`#A44B28`** (AA); `#B5532C` resta il terracotta delle
  illustrazioni (palette fissa). `--pt-terra` è lo stesso terracotta come ruolo
  (errori, segno caldo) e non segue l'accento se l'accento cambia.
- **Testo sopra un accento** `--pt-on-accent{,-2,-3}` e
  `--pt-on-success-solid`: sullo scuro gli accenti si schiariscono, e un
  bianco fisso sopra scende sotto 3:1. In stampa tornano inchiostro, perché
  il browser di default non stampa gli sfondi.
- **Tavolozza del codice** `--pt-code-{fg,kw,str,com,dec,num}`: tutta presa
  dai colori dell'interfaccia, quindi segue il tema da sola.
- **`--pt-text-xs` è 12px** (`0.75rem`), non il 10,24px della scala: è il
  pavimento di leggibilità di pillole ed eyebrow.
- **Misura di riga** `--pt-measure` / `--pt-measure-wide`, in `ch`: la colonna
  di lettura si misura in caratteri, non in pixel, perché il corpo del testo
  scala con la viewport e 680px valgono 26 caratteri su un telefono e 75 su un
  tablet. Sostituisce `--pt-reading`, che non esiste più: sul corpo desktop
  68ch fanno 680,73px, cioè la stessa colonna di prima, e la differenza si
  vede dove il testo rimpicciolisce.

## Come consumarlo

Sito e libro lo montano come **git submodule** (il repo è pubblico, quindi
anche i cloni e la CI del libro pubblico lo risolvono):

```bash
git submodule add https://github.com/paithon-it/brand <cartella>/brand
# nel CSS:  @import "brand/fonts.css";  @import "brand/tokens.css";
# aggiornare la firma:
git submodule update --remote <cartella>/brand && git commit -am "bump brand"
```

Si consuma **per riferimento, non per copia**: `fonts.css`, `tokens.css`,
`aurora.css`, `print.css` e `print.js` si importano così come sono, le figure
si ricolorano con `figure/palette.py`, le animazioni importano i motori di
`motion/`. Una copia (un valore riscritto a mano, un `@font-face` proprio,
una mappa dei colori nel consumatore) invecchia per conto suo, e il brand
non la raggiunge più.

Chi concatena i fogli in un bundle deve riscrivere gli `url()` di
`fonts.css`, che sono relativi a lui (`fonts/...`).

## Cosa può stare qui

Il repo è pubblico: tutto quello che c'è **finisce online**. Ci sta quello
che sito e libro servono già a ogni visitatore (fogli di stile, colori,
font, segno), e niente altro: niente chiavi, niente bozze, niente script o
documenti interni dei consumatori, niente materiale di cui non abbiamo i
diritti. Pubblico non vuol dire libero: vedi [`LICENSE`](LICENSE).
