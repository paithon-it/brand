# motion — lo stile delle animazioni paithon

Le clip esplicative (quelle che finiscono negli articoli e nei capitoli del
libro come GIF) hanno una firma visiva sola, definita qui. Chi le produce non
reinventa colori, tempi o composizione: importa questo tema.

| File | Cos'è |
|---|---|
| `paithon_anim.py` | **La fonte.** Tema Manim: palette, font, scala tipografica, helper di composizione, ritmo, firma di copyright. |
| `motion.css` | Gli stessi numeri per il web: durate, curva, il gesto `pt-entra`. |
| `fonts/` | I TTF usati nel rendering (Pango non legge i WOFF2 del tema). Stessi file per tutti i consumatori: stessa resa. |

## Che cos'è una clip paithon

Una figura animata, non un video. Dura **5–12 secondi**, si ripete in loop,
racconta **3–5 passaggi** e si guarda senza audio. Se servono più di cinque
passaggi, sono due clip.

- **Il testo è il protagonista.** Il movimento serve a scandire il
  ragionamento, non a decorarlo.
- **Palette fissa**: i cinque `--pt-illus-*` di `tokens.css` — terracotta
  `#B5532C`, teal `#2D5A5C`, ocra `#C9A961`, warm-black `#1A1A1A`, cream
  `#F8F5EE`. Niente gradienti, neon, glassmorphism, 3D lucido.
- **Tipografia**: Fraunces per i titoli, Inter per il testo, JetBrains Mono
  per il codice. Le formule sono LaTeX vero.
- Terracotta è l'unico accento caldo dominante: teal e ocra sono di supporto.

## Composizione

```
┌─────────────────────────────────────────┐
│ Titolo                                  │  intesta(): titolo + filetto
│ ─────────────────────────────────────── │
│                                         │
│              contenuto                  │  centra(): usa l'area libera
│                                         │
│ didascalia                  ▲ paithon.it│  firma: sempre in basso a destra
└─────────────────────────────────────────┘
```

La didascalia sta **a sinistra**, non centrata: al centro finirebbe sotto la
firma nelle composizioni larghe.

## Ritmo

| Costante | Manim | CSS | Quando |
|---|---|---|---|
| `RAPIDO` | 0.4 s | `--pt-motion-rapido` | comparsa di un dettaglio |
| `NORMALE` | 0.7 s | `--pt-motion-normale` | entrata standard |
| `LENTO` | 1.1 s | `--pt-motion-lento` | trasformazioni, morphing |
| `PAUSA` | 0.9 s | `--pt-motion-pausa` | stacco fra due passaggi |
| `PAUSA_FINALE` | 1.6 s | `--pt-motion-chiusura` | respiro prima del loop |

Il gesto d'ingresso è sempre lo stesso: opacità 0→1 con un micro-scorrimento
dal basso — `entra()` in Manim, `.pt-entra` nel CSS — e usa **`--pt-ease-out`**
di `tokens.css`, la stessa curva di card e view-transition. Non è
un'approssimazione: `paithon_anim.py` risolve la cubic-bezier come fa il
browser (`bezier_css()`), quindi le due entrate coincidono.

I passaggi interni di una clip usano invece la curva simmetrica di Manim
(`smooth`); se serve replicarla sul web c'è `--pt-motion-ease`, ricavata per
fitting (errore massimo 0.05).

## Firma di copyright

Ogni clip pubblicata porta **bollo tribar + `paithon.it`** in basso a destra.
È automatica: la disegna `ScenaPaithon`. Si toglie solo con `firma = False`, e
solo per materiale che non esce da qui.

Il tratto dell'SVG del bollo è tarato sul favicon: alla scala della firma Manim
non lo riscala e coprirebbe i tre colori, quindi il tema lo azzera.

## Chiaro e scuro

Il default è su crema e usa i `--pt-illus-*` esatti, che per definizione **non**
cambiano fra i due temi.

`PAITHON_TEMA=scuro` non ridefinisce quella palette: produce un rendering
diverso, pensato per stare su fondo scuro, che prende in prestito gli accenti
dark dell'interfaccia (terracotta `#E27B52`, teal `#5BA39C`, ocra `#DDB874` su
`#0E0C0A`). Serve perché il teal `#2D5A5C` su `#0E0C0A` sarebbe illeggibile.

Nel **libro** non serve: le pagine invertono le `<img>` in dark mode via CSS,
e una clip su crema diventa da sola la sua variante scura. Serve per social,
slide e ovunque il file venga usato così com'è su fondo scuro.

## Esportazione

| Uso | Formato |
|---|---|
| Articolo / capitolo | GIF 800 px, 15 fps, palette 64 colori (+ MP4 se serve leggerezza) |
| Social verticale | 9:16, `ScenaVerticale` |
| Anteprima | PNG dell'ultimo fotogramma, o griglia di fotogrammi |

## Come si consuma

Manim gira in Docker; monta questa cartella e mettila su `PYTHONPATH`:

```bash
docker run --rm \
  -v /percorso/al/brand:/brand:ro \
  -e PYTHONPATH=/brand/motion \
  manimcommunity/manim:v0.20.1 manim render -qm scena.py MiaScena
```

Dentro la scena:

```python
from paithon_anim import *

class ComeFunziona(ScenaPaithon):
    titolo_scena = "Come funziona"

    def costruisci(self):
        blocchi = VGroup(*[self.scatola(t) for t in ("input", "modello", "output")])
        blocchi.arrange(RIGHT, buff=1.0)
        self.centra(blocchi)
        self.play(entra(*blocchi))
        self.chiusura()
```

I consumatori attuali sono `paithon` (skill `run-animazioni`) e `paithonbook`
(skill `anima-manim`), entrambi via il submodule del brand.
