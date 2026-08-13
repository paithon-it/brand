#!/usr/bin/env python3
"""Le istanze statiche dei font del brand, per chi non sa leggere i variabili.

Il sito carica Fraunces, Inter e JetBrains Mono come font variabili, e sta
bene cosi': un browser sa interpolare. Chi non sa sono gli altri due motori
che compongono roba nostra:

- **Pango**, dietro Manim, che dei font variabili prende quello che capita;
- **fontspec** sotto LuaLaTeX, che dal file variabile prende l'istanza di
  *default*, e i default di Fraunces sono `wght 900` e `WONK 1`. Vuol dire
  che un libro composto senza istanziare uscirebbe tutto in nero pesante con
  le varianti bizzarre delle lettere. Non e' un'ipotesi, e' il default.

Quindi qui si scaricano i variabili da `google/fonts` e si congelano nei pesi
che servono. Lo script e' la fonte: i `.ttf` in `stampa/fonts/` sono un
prodotto, e si rifanno con

    python3 stampa/genera-font.py

## Perche' WONK=1

Perche' cosi' fa il sito. Chiedendo a Google Fonts solo gli assi `opsz` e
`wght` (che e' l'URL in `fonts.md`), gli assi non chiesti restano al loro
default, e per Fraunces `WONK` di default e' 1. Le lettere bizzarre le vede
gia' chi legge online: la stampa non deve essere un font diverso.

## Perche' due tagli ottici di Fraunces

`opsz` non e' la dimensione del carattere, e' il disegno: a corpo grande i
tratti sottili possono assottigliarsi ancora, a corpo piccolo no o
scompaiono. Il taglio da 72 e' per i titoli; quello da 10 esiste perche' un
giorno si potrebbe comporre il testo in Fraunces invece che in Inter, ed e'
una prova che vale la pena poter fare senza tornare qui.
"""

import pathlib
import urllib.parse
import urllib.request

from fontTools import ttLib
from fontTools.varLib import instancer

QUI = pathlib.Path(__file__).resolve().parent
FONTS = QUI / "fonts"
BASE = "https://raw.githubusercontent.com/google/fonts/main/"

VARIABILI = {
    "fraunces": "ofl/fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf",
    "fraunces-italic": "ofl/fraunces/Fraunces-Italic[SOFT,WONK,opsz,wght].ttf",
    "inter": "ofl/inter/Inter[opsz,wght].ttf",
    "inter-italic": "ofl/inter/Inter-Italic[opsz,wght].ttf",
    "jetbrains": "ofl/jetbrainsmono/JetBrainsMono[wght].ttf",
    "jetbrains-italic": "ofl/jetbrainsmono/JetBrainsMono-Italic[wght].ttf",
}

LICENZE = {
    "fraunces": "ofl/fraunces/OFL.txt",
    "inter": "ofl/inter/OFL.txt",
    "jetbrainsmono": "ofl/jetbrainsmono/OFL.txt",
}

# (file che esce, variabile da cui viene, assi a cui congelare, nome interno)
#
# Il nome lo scriviamo noi. `instancer` lo aggiornerebbe da se', ma solo se i
# valori corrispondono a una istanza gia' battezzata dentro il font: il taglio
# ottico da 10 non lo e', e il font uscirebbe dichiarandosi «Fraunces 9pt
# Black», che e' il nome dell'istanza di default. Il disegno sarebbe giusto e
# il cartellino sbagliato, che e' il modo migliore per far perdere un
# pomeriggio a qualcuno fra due anni.
ISTANZE = [
    # Fraunces per i titoli: taglio ottico da 72.
    ("fraunces-400.ttf", "fraunces",
     {"wght": 400, "opsz": 72, "WONK": 1, "SOFT": 0}, "Fraunces 72pt", ""),
    ("fraunces-600.ttf", "fraunces",
     {"wght": 600, "opsz": 72, "WONK": 1, "SOFT": 0}, "Fraunces 72pt SemiBold", ""),
    ("fraunces-800.ttf", "fraunces",
     {"wght": 800, "opsz": 72, "WONK": 1, "SOFT": 0}, "Fraunces 72pt ExtraBold", ""),
    ("fraunces-400italic.ttf", "fraunces-italic",
     {"wght": 400, "opsz": 72, "WONK": 1, "SOFT": 0}, "Fraunces 72pt", "Italic"),
    ("fraunces-600italic.ttf", "fraunces-italic",
     {"wght": 600, "opsz": 72, "WONK": 1, "SOFT": 0},
     "Fraunces 72pt SemiBold", "Italic"),

    # Fraunces per il testo: taglio ottico da 10.
    ("fraunces-testo-400.ttf", "fraunces",
     {"wght": 400, "opsz": 10, "WONK": 1, "SOFT": 0}, "Fraunces 10pt", ""),
    ("fraunces-testo-600.ttf", "fraunces",
     {"wght": 600, "opsz": 10, "WONK": 1, "SOFT": 0}, "Fraunces 10pt SemiBold", ""),
    ("fraunces-testo-400italic.ttf", "fraunces-italic",
     {"wght": 400, "opsz": 10, "WONK": 1, "SOFT": 0}, "Fraunces 10pt", "Italic"),

    # Inter, il corpo del testo.
    ("inter-400.ttf", "inter", {"wght": 400, "opsz": 14}, "Inter", ""),
    ("inter-500.ttf", "inter", {"wght": 500, "opsz": 14}, "Inter Medium", ""),
    ("inter-600.ttf", "inter", {"wght": 600, "opsz": 14}, "Inter SemiBold", ""),
    ("inter-400italic.ttf", "inter-italic", {"wght": 400, "opsz": 14},
     "Inter", "Italic"),
    ("inter-600italic.ttf", "inter-italic", {"wght": 600, "opsz": 14},
     "Inter SemiBold", "Italic"),

    # JetBrains Mono, il codice.
    ("jetbrains-mono-400.ttf", "jetbrains", {"wght": 400}, "JetBrains Mono", ""),
    ("jetbrains-mono-600.ttf", "jetbrains", {"wght": 600},
     "JetBrains Mono SemiBold", ""),
    ("jetbrains-mono-400italic.ttf", "jetbrains-italic", {"wght": 400},
     "JetBrains Mono", "Italic"),
]


def scarica(percorso: str, dove: pathlib.Path) -> pathlib.Path:
    """Il file dal repository google/fonts. Le parentesi quadre del nome
    vanno codificate, altrimenti raw.githubusercontent risponde 404."""
    if dove.exists():
        return dove
    dove.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(BASE + urllib.parse.quote(percorso), dove)
    return dove


def battezza(font: ttLib.TTFont, famiglia: str, stile: str) -> None:
    """Scrive il nome dell'istanza nel font.

    `stile` e' "" o "Italic": sono i due soli valori che la sottofamiglia
    puo' prendere se si vuole che ogni istanza viva come famiglia a se',
    che e' come sono fatti i font statici e come `fontspec` se li aspetta.
    """
    sottofamiglia = stile or "Regular"
    intero = f"{famiglia} {stile}".strip()
    postscript = intero.replace(" ", "")
    for id_nome, valore in ((1, famiglia), (2, sottofamiglia),
                            (4, intero), (6, postscript)):
        font["name"].setName(valore, id_nome, 3, 1, 0x409)   # Windows
        font["name"].setName(valore, id_nome, 1, 0, 0)       # Macintosh


def main() -> None:
    FONTS.mkdir(parents=True, exist_ok=True)
    cache = QUI / ".variabili"

    for nome, percorso in VARIABILI.items():
        scarica(percorso, cache / f"{nome}.ttf")
    for nome, percorso in LICENZE.items():
        scarica(percorso, FONTS / f"OFL-{nome}.txt")

    for uscita, sorgente, assi, famiglia, stile in ISTANZE:
        font = ttLib.TTFont(cache / f"{sorgente}.ttf")
        statico = instancer.instantiateVariableFont(font, assi, inplace=False)
        battezza(statico, famiglia, stile)
        statico.save(FONTS / uscita)
        peso = statico["OS/2"].usWeightClass
        print(f"  {uscita:32} wght {peso:3}  "
              f"{(FONTS / uscita).stat().st_size // 1024:4} KB  "
              f"{statico['name'].getDebugName(4)}")

    print(f"\n{len(ISTANZE)} istanze in {FONTS}")


if __name__ == "__main__":
    main()
