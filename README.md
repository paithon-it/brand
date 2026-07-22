# paithon — brand

Fonte unica della firma visiva di paithon (sito, libro, social, tutto ciò che
verrà). Si cambia **qui**, i consumatori la riprendono. Repo privato, nessuna
licenza = *all rights reserved*.

## Contenuto

| File | Cos'è |
|---|---|
| `tokens.css` | **La fonte.** Tutti i design token come CSS custom properties (`--pt-*`): colori (light/dark), tipografia, spacing, layout, radius, shadow, transizioni. Nessun valore va duplicato altrove — si legge da qui. |
| `logos/paithon-mark.svg` | Il segno: triangolo di Penrose (tribar GEB), palette-locked, identico in light/dark. Stesso mark di header sito, favicon e copertina libro. |
| `fonts.md` | Le 3 famiglie + pesi + URL Google Fonts esatto. |
| `social/` | Template per Instagram/YouTube/etc. (export PNG/SVG). |

## Palette (subset memorabile — l'elenco completo è in `tokens.css`)

Illustrazioni editoriali: **solo** questi 5 + neutri warm. Niente gradienti
AI-style, neon, glassmorphism.

- `#B5532C` terracotta — accent primario
- `#1F5E58` verde petrolio — secondario (mirato: eyebrow, pill, marker)
- `#C9A961` ocra — terziario
- `#1A1714` warm black
- `#F4F1E8` cream

## Font

Fraunces (display) · Inter (body) · JetBrains Mono (codice). Tutti Google
Fonts, free. Dettagli e URL in `fonts.md`.

## Token 2026 (modernizzazione)

Oltre a colori/tipo/spacing storici, `tokens.css` include ora:

- **Display fluidi** `--pt-display-{sm,md,lg,xl}` (`clamp`): headline che scalano
  senza salti di breakpoint.
- **Superfici tint** `--pt-tint-accent{,-2,-3}`: accent a bassa opacità per
  hover/badge/stati attivi (via `color-mix`, seguono light/dark).
- **Focus ring** `--pt-ring` / `--pt-ring-offset`: anello unico token-driven.
- **Spaziatura di sezione fluida** `--pt-space-section{,-lg}`, `--pt-shadow-xs`.
- **`color-scheme` / `accent-color`** nativi per light/dark.
- Accent UI accessibile **`#A44B28`** (AA); `#B5532C` resta il terracotta delle
  illustrazioni (palette fissa).

## Come consumarlo

Il token è **CSS custom properties**, quindi qualsiasi consumatore web fa
`@import` di `tokens.css` e legge le `var(--pt-*)`.

**Consumatore privato** (es. sito WordPress) → git submodule:

```bash
git submodule add https://github.com/paithon-it/brand assets/brand
# poi nel CSS del tema:  @import "../brand/tokens.css";
# aggiornare la firma ovunque:
git submodule update --remote assets/brand && git commit -am "bump brand"
```

**Consumatore pubblico** (es. `paithonbook`, pubblico) → **NON** submodule:
un repo pubblico non può clonare un submodule privato (CI e cloni esterni non
hanno le credenziali). Fai vendoring del solo `tokens.css` con uno script di
sync, oppure rendi pubblico questo repo (i token non sono segreti: sono già
serviti nel CSS di ogni pagina). Vedi la nota in fondo.

## Nota pubblico/privato

`tokens.css` **non è materiale segreto** — è servito a ogni visitatore del
sito. Tenere il repo privato ha senso solo per asset non ancora rilasciati
(loghi in lavorazione, template). Se il libro pubblico deve dipendere da qui,
la scelta pulita è rendere pubblico `brand` (o almeno i token) ed evitare il
vendoring manuale.
