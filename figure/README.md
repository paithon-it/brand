# figure

La palette delle figure e la sua resa scura, in un posto solo.

Le figure (SVG statici, SVG animati, clip Manim) si disegnano sul chiaro con
la palette fissa delle illustrazioni: i cinque `--pt-illus-*` più i loro
neutri. In tema scuro sito e libro ne mostrano una resa ricolorata. Fino a
ottobre 2026 ognuno aveva la sua mappa chiaro→scuro, copiata a mano: le due
divergevano sul fondo (`#16130F` contro `#0E0C0A`) e una era rimasta all'ocra
scura di prima (`#DDB874`). Ora la mappa è [`palette.json`](palette.json), e
chi ricolora legge da qui.

## Il file

- **`ruoli`**: il mestiere di un colore dentro una figura, con il valore
  chiaro e quello scuro. `illus` è il token del chiaro in `tokens.css`,
  `token` quello del blocco scuro da cui viene lo scuro: le prove in
  `../prove/` verificano che coincidano, così un ritocco ai token che non
  arriva qui fa fallire qualcosa.
- **`colori`**: per chi ricolora per esadecimale, ogni colore della palette
  chiara e il suo ruolo.
- **`sinonimi`**: grigi storici che compaiono nelle figure esistenti e nei
  motori di [`../motion/`](../motion/) (sono i neutri dell'interfaccia, non
  quelli delle illustrazioni). Si ricolorano come il ruolo a cui puntano;
  in una figura nuova non si usano.

## Le scelte

- **Il fondo scuro è `--pt-bg-elev` (`#16130F`)**, non il nero della pagina:
  la figura si stacca appena, come una card. Vale anche per le clip Manim.
- **L'ocra non cambia** (`#C9A961` in tutti e due i temi): è quella del logo,
  e sul nero regge da sola come testo (8,7:1). L'ocra cupa, che sul crema fa
  da testo, sullo scuro diventa la stessa ocra, per la stessa ragione di
  `--pt-accent-3-ink`.
- **Le etichette** sono testo sopra una campitura, e la campitura sullo scuro
  si ribalta: per questo hanno ruoli propri, che chi ricolora per esadecimale
  non può distinguere e quindi non usa.

## Come si legge

```python
import sys
sys.path.insert(0, "<brand>/figure")
import palette

palette.ruolo("fondo")        # ("#F8F5EE", "#16130F")
palette.scuro("#5E5852")      # "#BCB3A1"
palette.MAPPA_SCURA           # {chiaro: scuro}, colori più sinonimi
```

Un colore che non è nel file solleva `KeyError`: chi aggiunge un colore a una
figura lo aggiunge qui, guardando i token, e non lo lascia indovinare.
