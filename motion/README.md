# motion — lo stile delle animazioni paithon

Le figure animate (quelle che finiscono negli articoli e nei capitoli del
libro) hanno una firma visiva sola, definita qui. Chi le produce non reinventa
colori, tempi o composizione: importa questo tema.

| File | Cos'è |
|---|---|
| `paithon_svg.py` | **Il motore di default.** Figure animate in SVG: geometria, palette, `@keyframes`, i tre controlli di `scrivi()` e il provino di stampa. |
| `paithon_anim.py` | **Il motore Manim**, per ciò che i keyframe non danno: palette, font, scala tipografica, helper di composizione, ritmo, firma di copyright. |
| `motion.css` | Gli stessi numeri per il web: durate, curva, il gesto `pt-entra`. |
| `fonts/` | I TTF usati nel rendering Manim (Pango non legge i WOFF2 del tema). Stessi file per tutti i consumatori: stessa resa. |

## Che cos'è una clip paithon

Una figura animata, non un video. Dura **5–12 secondi**, si ripete in loop,
racconta **3–5 passaggi** e si guarda senza audio. Se servono più di cinque
passaggi, sono due clip.

- **Il testo è il protagonista.** Il movimento serve a scandire il
  ragionamento, non a decorarlo.
- **Palette fissa**: i cinque `--pt-illus-*` di `tokens.css` (terracotta
  `#B5532C`, teal `#2D5A5C`, ocra `#C9A961`, warm-black `#1A1A1A`, cream
  `#F8F5EE`). Niente gradienti, neon, glassmorphism, 3D lucido.
- **Tipografia**: Fraunces per i titoli, Inter per il testo, JetBrains Mono
  per il codice. Le formule sono LaTeX vero.
- Terracotta è l'unico accento caldo dominante: teal e ocra sono di supporto.

## Due motori, due problemi diversi

| | SVG animato (`paithon_svg.py`) | Manim (`paithon_anim.py`) |
|---|---|---|
| uscita | `.svg`, testo | `.gif` raster |
| peso | **~6 KB** a figura | ~570 KB a clip |
| in git | diffabile | blob binario nuovo a ogni render |
| versione ferma | si congela da sé | la striscia, da produrre |
| serve per | geometria, barre, reti, griglie | LaTeX composto, curve, coreografie |
| dipendenze | nessuna (`cairosvg` solo per il provino) | Docker, Manim, LaTeX |

**Di default l'SVG.** Costa meno, si legge in git, e in stampa si risolve da
solo. Si passa a Manim quando serve davvero ciò che solo lui dà: formule LaTeX
composte, grafici di funzione con tangenti, coreografie con molti oggetti che
si inseguono. Non è una gerarchia di qualità: *rendere fotogrammi* e
*descrivere keyframe* risolvono problemi diversi.

### La regola che tiene in piedi l'SVG

Il disegno **fermo è lo stato finale**, scritto con coordinate e attributi
veri, senza nessun `transform`; l'animazione parte dalla trasformazione
inversa e finisce sull'identità. Così il riposo non dipende dal CSS e regge in
stampa, nei PDF, con `prefers-reduced-motion` e in qualunque rasterizzatore.

È l'equivalente di «l'ultimo fotogramma deve reggere da solo» per Manim, con
una differenza che conta: là lo verifica l'occhio, qui lo garantisce la
struttura. I due stati non possono divergere.

`scrivi(nome, titolo, fig, dest)` rifiuta il file se contiene colori fuori
palette, uno `<script>` o XML malformato, e scrive un provino PNG in
`~/.cache/paithon-svg/`: è lo stato di riposo rasterizzato, cioè esattamente
ciò che vedrà la stampa. Va guardato prima di pubblicare, e ha già
intercettato una volta un errore di segno che avrebbe mandato in stampa una
retta con la pendenza sbagliata.

Niente `<script>` dentro un SVG, mai: molti visualizzatori non lo eseguono, e
chi lo esegue lo fa in un contesto che non controlliamo.

## Quando animare (e quando no)

Vale per tutti e due i motori: decide *se* animare, non *con che cosa*.

Il loop cambia segno a seconda di dove sta.

**Nell'articolo è un pregio.** Si scorre, la clip cattura, spesso è l'unica
figura del pezzo, si condivide. Lì l'animazione fa un lavoro che una figura
ferma non fa.

**Nel libro è spesso un difetto.** Il lettore sta su quel paragrafo due minuti,
magari rileggendo, e intanto la figura ripete all'infinito a un metro
dall'occhio: non si mette in pausa, non ci si torna sopra a un fotogramma
preciso. E il libro **esiste anche su carta**, dove una figura che ha senso
solo in movimento è un buco.

Da qui tre regole:

1. **Animare solo quando il tempo è il contenuto.** Discesa del gradiente,
   denoising della diffusione, convoluzione che scorre, backprop che risale,
   campionamento autoregressivo: lì il "prima → dopo" *è* il concetto, e una
   figura ferma deve barare con tre pannelli affiancati. Architetture,
   tassonomie, confronti e pipeline restano **figure ferme** (che sono SVG
   pure loro: qui la differenza non è il formato, è se c'è del movimento).
2. **Lo stato di riposo deve reggere da solo.** Con l'SVG lo garantisce la
   struttura. Con Manim va verificato a mano: estrai l'ultimo fotogramma, e se
   non si capisce niente la clip non va nel libro. Taglia via quasi tutti i
   casi dubbi, e lo fa in due secondi.
3. **Una clip per sezione.** Due animazioni nella stessa schermata si rubano
   l'attenzione: se una sezione ne merita due, quasi sempre sono due sezioni.

Il tetto nel libro è **5–10 per capitolo**. È un tetto, non una quota da
riempire: a decidere è la regola 1, e un capitolo con due candidati veri ne ha
due. Sopra la cinquantina di clip **Manim** conviene passare al WebP: misurato
sulle prime otto del libro, una clip di 7–9 s a 800 px pesa ~570 KB in GIF e
~300 in WebP. Per l'SVG il problema non si pone: a 6 KB l'una, cinquanta
figure pesano meno di una sola GIF.

### La striscia: la versione ferma, e solo per Manim

Quando la clip serve ma il movimento non arriva (carta, PDF, feed senza
autoplay), si campiona su 2–3 fotogrammi e li si affianca in serie. Diventa una
figura statica che racconta lo stesso passaggio. I driver Manim la producono
con `--striscia`: campionano dal 30% della durata in poi (l'incipit è la
dissolvenza del titolo e non dice niente) e includono sempre l'ultimo
fotogramma.

Due riquadri bastano quando la clip è un "prima/dopo"; tre quando c'è un
passaggio intermedio che serve davvero.

**Un SVG animato non ha bisogno di striscia**, ed è metà del suo vantaggio: il
suo stato di riposo *è già* la versione ferma, quindi lo stesso file serve lo
schermo e la carta. Non c'è un secondo artefatto da generare, da referenziare
e da tenere allineato.

### Lo stesso concetto in due posti

Non duplicare il sorgente della scena. Se un articolo riprende un capitolo, il
`.py` resta dove vive il contenuto originale e per l'altra superficie si
riusa il file renderizzato. Due copie della stessa scena divergono in un mese:
esattamente come stavano divergendo i due temi prima di questa cartella, e come
stava divergendo il motore SVG finché è rimasto dentro il libro.

## Composizione (Manim)

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

Il gesto d'ingresso è sempre lo stesso (opacità 0→1 con un micro-scorrimento
dal basso: `entra()` in Manim, `.pt-entra` nel CSS) e usa **`--pt-ease-out`**
di `tokens.css`, la stessa curva di card e view-transition. Non è
un'approssimazione: `paithon_anim.py` risolve la cubic-bezier come fa il
browser (`bezier_css()`), quindi le due entrate coincidono.

I passaggi interni di una clip usano invece la curva simmetrica di Manim
(`smooth`); se serve replicarla sul web c'è `--pt-motion-ease`, ricavata per
fitting (errore massimo 0.05).

## Firma di copyright

Ogni clip **Manim** pubblicata porta **bollo tribar + `paithon.it`** in basso a
destra. È automatica: la disegna `ScenaPaithon`. Si toglie solo con
`firma = False`, e solo per materiale che non esce da qui.

Le figure SVG non la portano, ed è voluto: nascono dentro una pagina che è già
firmata, e a 6 KB il bollo peserebbe quanto il disegno. Una figura SVG che
esca dal suo contesto (una slide, un social) va firmata a mano.

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

Le figure SVG seguono la stessa logica e non hanno l'equivalente di
`PAITHON_TEMA`: disegnano su crema con i `--pt-illus-*`, e sul dark ci pensa
l'inversione CSS della pagina. Un file solo, come per il resto delle figure.

## Esportazione

| Uso | Formato |
|---|---|
| Articolo / capitolo, SVG | il `.svg` così com'è: serve lo schermo e la carta |
| Articolo / capitolo, Manim | GIF 800 px, 15 fps, palette 64 colori (+ MP4 se serve leggerezza) |
| Social verticale | 9:16, `ScenaVerticale` (solo Manim) |
| Anteprima | il provino PNG per l'SVG; per Manim l'ultimo fotogramma o una griglia |

## Come si consuma

### SVG

Nessuna dipendenza e nessun container: basta mettere questa cartella su
`sys.path`. Il consumatore decide dove finiscono le figure.

```python
import sys
from pathlib import Path

sys.path.insert(0, "percorso/al/brand/motion")
from paithon_svg import Figura, Riquadro, scrivi, TERRACOTTA

scrivi(NOME, TITOLO, costruisci(), Path("book/figures"))
```

Nel libro questo lo fa `animazioni/svg/genera.py`, che tiene l'unica cosa che
sa del libro: la cartella di destinazione.

### Manim

Gira in Docker; monta questa cartella e mettila su `PYTHONPATH`:

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
