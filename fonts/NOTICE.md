# Font di terze parti (web)

Questi file **non sono opera di paithon**. Sono ridistribuiti sotto
SIL Open Font License 1.1, che li accompagna come richiede la licenza stessa
(OFL 1.1 §2: ogni copia va distribuita con il testo della licenza e con la
nota di copyright). Una copia della licenza per ciascuna famiglia sta
accanto, così com'è stata pubblicata dagli autori:
[`OFL-fraunces.txt`](OFL-fraunces.txt), [`OFL-inter.txt`](OFL-inter.txt),
[`OFL-jetbrainsmono.txt`](OFL-jetbrainsmono.txt).

Li carica [`../fonts.css`](../fonts.css). Sono i WOFF2 che Google Fonts serve
per l'API css2, subset `latin` e `latin-ext`, scaricati così come sono.

| File | Famiglia | Versione | Assi | Copyright |
|---|---|---|---|---|
| `fraunces-normal-{latin,latin-ext}.woff2` | Fraunces | 1.000 | `opsz 9–144`, `wght 100–900` | 2020 The Fraunces Project Authors ([undercasetype/Fraunces](https://github.com/undercasetype/Fraunces)) |
| `fraunces-italic-{latin,latin-ext}.woff2` | Fraunces Italic | 1.000 | `opsz 9–144`, `wght 100–900` | ” |
| `inter-normal-{latin,latin-ext}.woff2` | Inter | 4.001 | `wght 100–900` | 2016 The Inter Project Authors ([rsms/inter](https://github.com/rsms/inter)) |
| `jetbrains-mono-normal-{latin,latin-ext}.woff2` | JetBrains Mono | 2.211 | `wght 400–800` | 2020 The JetBrains Mono Project Authors ([JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono)) |

`fonts.css` dichiara solo una parte degli assi (Fraunces 400–800, Inter e
JetBrains Mono 400–600): sono i pesi di [`../fonts.md`](../fonts.md). Il resto
dell'intervallo sta nel file perché così lo serve Google, e tagliarlo
vorrebbe dire produrre una versione modificata da dichiarare.

## Modifiche rispetto all'originale

Il subset per blocchi Unicode è quello di Google Fonts, non nostro. Nessun
altro intervento. Nessuna delle tre famiglie dichiara un *Reserved Font Name*
(la nota di copyright non contiene la clausola `with Reserved Font Name`),
quindi i nomi originali si possono tenere.
