# logos

- `paithon-mark.svg` — il segno (triangolo di Penrose), master. Palette-locked,
  uguale in light/dark. È lo stesso di header sito / favicon / copertina libro.

Il logotipo "paithon" è **testuale**: Fraunces 800, non un file. Per ricrearlo
basta il font (vedi `../fonts.md`), così resta nitido a ogni dimensione.

## Il segno da solo, e il segno dentro un'interfaccia

Sono due usi diversi e seguono due regole diverse. Confonderli è la ragione
per cui questa sezione esiste.

**`paithon-mark.svg` è palette-locked**: i suoi tre colori non cambiano mai,
in nessun tema. È il segno come marchio, quello che va su un favicon, una
copertina, un adesivo, dove non c'è un tema attorno da cui dipendere.

**Un lockup dentro un'interfaccia si ricolora**, perché lì il segno vive
accanto al testo e deve reggere lo stesso fondo. La regola è che il tribar
prende i colori delle **illustrazioni** sul chiaro e gli accenti **dark**
dell'interfaccia sullo scuro, e il tratto passa da inchiostro a osso:

| | chiaro | scuro |
|---|---|---|
| faccia 1 | `#B5532C` | `#E27B52` |
| faccia 2 | `#2D5A5C` | `#5BA39C` |
| faccia 3 | `#C9A961` | `#DDB874` |
| tratto | `#1A1A1A` | `#F4ECDD` |
| wordmark | `#1A1714` | `#F4ECDD` |

Non sono colori nuovi: sono `--pt-illus-*` da una parte e gli accenti del
blocco `[data-theme="dark"]` di `tokens.css` dall'altra. Il teal `#2D5A5C` su
`#0E0C0A` sarebbe illeggibile, ed è lo stesso motivo per cui `PAITHON_TEMA=scuro`
esiste nelle animazioni.

Il lockup del libro **Paithon Book**
(`paithonbook/book/_static/logo-{light,dark}.svg`, più le varianti `-inline-`)
segue questa convenzione ed è l'esempio da guardare. Non sta qui perché è il
segno di quel prodotto, non della marca: `aria-label="Paithon Book"`.

Una cosa da non «correggere»: **nel disegno il lockup resta minuscolo**, perché
compone il wordmark `paithon` vettorizzato, che è il segno della marca e vale
anche per il sito. Il nome scritto invece va con le iniziali maiuscole, ed è la
convenzione normale dei marchi in minuscolo: il segno resta com'è disegnato, la
prosa lo scrive in tondo. Le due cose divergono di proposito.
