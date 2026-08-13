# Font di terze parti (composizione in PDF)

Questi file **non sono opera di paithon**. Sono ridistribuiti sotto
[SIL Open Font License 1.1](OFL-fraunces.txt), che li accompagna come richiede
la licenza stessa (OFL 1.1 §2: ogni copia va distribuita con questo testo e
con la nota di copyright). Una copia della licenza per ciascuna famiglia sta
accanto, così com'è stata pubblicata dagli autori.

Servono perché `fontspec`, sotto LuaLaTeX, dei font variabili prende
l'**istanza di default**, e i default di Fraunces sono `wght 900` e `WONK 1`:
un libro composto dal file variabile uscirebbe tutto in nero pesante con le
varianti bizzarre delle lettere. Non è un'ipotesi, è il default.

Non si scrivono a mano: li genera `../genera-font.py`, che scarica i variabili
da `google/fonts` e li congela. Quel file è la fonte, questi sono il prodotto.

| File | Famiglia | Peso | Taglio ottico | Copyright |
|---|---|---|---|---|
| `fraunces-400.ttf` | Fraunces 72pt | 400 | `opsz 72` | 2020 The Fraunces Project Authors |
| `fraunces-600.ttf` | Fraunces 72pt SemiBold | 600 | `opsz 72` | ” |
| `fraunces-800.ttf` | Fraunces 72pt ExtraBold | 800 | `opsz 72` | ” |
| `fraunces-400italic.ttf` | Fraunces 72pt Italic | 400 | `opsz 72` | ” |
| `fraunces-600italic.ttf` | Fraunces 72pt SemiBold Italic | 600 | `opsz 72` | ” |
| `fraunces-testo-400.ttf` | Fraunces 10pt | 400 | `opsz 10` | ” |
| `fraunces-testo-600.ttf` | Fraunces 10pt SemiBold | 600 | `opsz 10` | ” |
| `fraunces-testo-400italic.ttf` | Fraunces 10pt Italic | 400 | `opsz 10` | ” |
| `inter-400.ttf` | Inter | 400 | `opsz 14` | 2016 The Inter Project Authors |
| `inter-500.ttf` | Inter Medium | 500 | `opsz 14` | ” |
| `inter-600.ttf` | Inter SemiBold | 600 | `opsz 14` | ” |
| `inter-400italic.ttf` | Inter Italic | 400 | `opsz 14` | ” |
| `inter-600italic.ttf` | Inter SemiBold Italic | 600 | `opsz 14` | ” |
| `jetbrains-mono-400.ttf` | JetBrains Mono | 400 | | 2020 The JetBrains Mono Project Authors |
| `jetbrains-mono-600.ttf` | JetBrains Mono SemiBold | 600 | | ” |
| `jetbrains-mono-400italic.ttf` | JetBrains Mono Italic | 400 | | ” |

## Perché due tagli ottici di Fraunces

`opsz` non è la dimensione a cui si compone, è il **disegno**: a corpo grande
i tratti sottili possono assottigliarsi ancora e le grazie farsi più fini, a
corpo piccolo no, o spariscono in stampa. Il taglio da 72 è per i titoli;
quello da 10 esiste perché il corpo del testo del libro potrebbe passare da
Inter a Fraunces, ed è una prova che si deve poter fare senza tornare qui.

## Perché `WONK 1`

Perché così fa il sito. L'URL di Google Fonts in [`../../fonts.md`](../../fonts.md)
chiede i soli assi `opsz` e `wght`; gli assi non chiesti restano al loro
default, e per Fraunces `WONK` di default è 1. Le varianti bizzarre di
alcune lettere le vede già chi legge online, e la stampa non deve sembrare un
font diverso.

## Modifiche rispetto all'originale

Sono **Modified Versions** ai sensi della OFL, quindi vanno dichiarate:
istanze statiche estratte dai variable font originali, con gli assi congelati
ai valori della tabella qui sopra, e il nome interno riscritto perché ogni
istanza si dichiari per quello che è.

Nessuna delle tre famiglie dichiara un *Reserved Font Name* (la nota di
copyright non contiene la clausola `with Reserved Font Name`), quindi le
istanze conservano legittimamente il nome della famiglia originale. Se in
futuro si aggiunge un font che **ha** un RFN, va rinominato prima di essere
ridistribuito qui.

## Non sono gli stessi di `motion/fonts/`

Là ce ne sono tre, quelli che servono a Pango per comporre le animazioni, e
uno dei tre porta un peso diverso da quello che dice il nome (è documentato
in [`../../motion/fonts/NOTICE.md`](../../motion/fonts/NOTICE.md)). Qui sono
sedici, generati da uno script, e ciascuno si dichiara per quello che è.
Unirle è una cosa da fare, ma vuol dire toccare le animazioni già rese e le
og:image del sito, quindi è una decisione a parte.
