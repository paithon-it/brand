# logos

- `paithon-mark.svg` — il segno (triangolo di Penrose), master. Palette-locked,
  uguale in light/dark. È lo stesso di header sito / favicon / copertina libro.
- `paithon-wordmark.svg` — il wordmark «paithon» vettorizzato, con il tribar al
  posto della «a»: il lockup del libro senza «book». Parola in `currentColor`,
  tribar a colori fissi con tratto `#1A1A1A`, in tutti e due i temi: sullo
  scuro basta che il testo attorno sia osso (vedi la tabella qui sotto).

Il logotipo "paithon" nasce **testuale**: Fraunces 800 (vedi `../fonts.md`).
Dove serve il segno composto, tribar incluso, c'è `paithon-wordmark.svg`.

## Il segno da solo, e il segno dentro un'interfaccia

Sono due usi diversi e seguono due regole diverse. Confonderli è la ragione
per cui questa sezione esiste.

**`paithon-mark.svg` è palette-locked**: i suoi tre colori non cambiano mai,
in nessun tema. È il segno come marchio, quello che va su un favicon, una
copertina, un adesivo, dove non c'è un tema attorno da cui dipendere.

**Un lockup dentro un'interfaccia ricolora solo la parola**, perché lì il
segno vive accanto al testo e la parola deve reggere lo stesso fondo. Il tribar
invece resta palette-locked anche lì: stesse tre facce e stesso tratto nei due
temi, perché i colori dell'interfaccia sono quelli del logo, e non il contrario.

| | chiaro | scuro |
|---|---|---|
| faccia 1 | `#B5532C` | `#B5532C` |
| faccia 2 | `#2D5A5C` | `#2D5A5C` |
| faccia 3 | `#C9A961` | `#C9A961` |
| tratto | `#1A1A1A` | `#1A1A1A` |
| wordmark | `#1A1714` | `#F4ECDD` |

Le facce sono i `--pt-illus-*` di `tokens.css`, il wordmark segue `--pt-fg`.
Sullo scuro il tratto `#1A1A1A` si confonde col fondo e le facce restano
separate dal colore: è voluto, ed è come appaiono i loghi scuri del libro.

Fino a settembre 2026 questa tabella dava sullo scuro gli accenti dark
dell'interfaccia (`#E27B52`, `#5BA39C`, `#DDB874`, tratto osso). I loghi del libro
non la seguono: si è allineato il documento ai file, non i file al
documento.

Il lockup del libro **Paithon Book**
(`paithonbook/book/_static/logo-{light,dark}.svg`, più le varianti `-inline-`)
segue questa convenzione ed è l'esempio da guardare (`-dark`: tribar
identico, parola `#F4ECDD`). Non sta qui perché è il
segno di quel prodotto, non della marca: `aria-label="Paithon Book"`.

Una cosa da non «correggere»: **nel disegno il lockup resta minuscolo**, perché
compone il wordmark `paithon` vettorizzato, che è il segno della marca e vale
anche per il sito. Il nome scritto invece va con le iniziali maiuscole, ed è la
convenzione normale dei marchi in minuscolo: il segno resta com'è disegnato, la
prosa lo scrive in tondo. Le due cose divergono di proposito.
