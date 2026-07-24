# Font di terze parti

Questi file **non sono opera di paithon**. Sono ridistribuiti sotto
[SIL Open Font License 1.1](OFL.txt), che li accompagna come richiede la
licenza stessa (OFL 1.1 §2: ogni copia va distribuita con questo testo e con
la nota di copyright).

Servono perché Pango — il motore di testo di Manim — non legge i WOFF2 che il
sito usa sul web: per il rendering delle animazioni servono i TTF. Sono gli
stessi file per sito e libro, così la resa è identica.

| File | Famiglia | Peso reale | Copyright | Origine |
|---|---|---|---|---|
| `fraunces-600-og.ttf` | Fraunces SemiBold | 600 | 2020 The Fraunces Project Authors | [undercasetype/Fraunces](https://github.com/undercasetype/Fraunces) |
| `inter-400-og.ttf` | Inter SemiBold | **600** | 2016 The Inter Project Authors | [rsms/inter](https://github.com/rsms/inter) |
| `jetbrains-mono.ttf` | JetBrains Mono | 400 | 2020 The JetBrains Mono Project Authors | [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono) |

## Modifiche rispetto all'originale

Sono **Modified Versions** ai sensi della OFL, quindi vanno dichiarate:

- **Fraunces** e **Inter**: istanze statiche estratte dai variable font
  originali (un solo peso, niente asse `opsz`/`wght`).
- **JetBrains Mono**: convertito da WOFF2 a TTF (stessi glifi, solo cambio di
  contenitore). Il subset latin del sito ha 394 glifi contro i ~700 completi.

Nessuno dei tre originali dichiara un *Reserved Font Name* (la nota di
copyright non contiene la clausola `with Reserved Font Name`), quindi le
istanze conservano legittimamente il nome della famiglia originale. Se in
futuro si aggiunge un font che **ha** un RFN, va rinominato prima di essere
ridistribuito qui.

## Attenzione al nome dei file

Il suffisso `-og` viene dalla generazione delle og:image del sito (libreria GD),
non è una sigla tipografica.

`inter-400-og.ttf` **non è il peso 400**: la tabella `OS/2` dichiara
`usWeightClass 600` e la famiglia è `Inter SemiBold`. Il nome del file è
sbagliato, non il font. Va tenuto presente in due punti:

- nelle animazioni il testo di corpo esce in SemiBold, non in Regular;
- lo stesso file alimenta le og:image del tema, che quindi hanno lo stesso
  peso involontario.

Il file non è stato rinominato per non rompere i consumatori esistenti: è una
scelta da fare insieme al fix del peso.
