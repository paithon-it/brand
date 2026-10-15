"""La palette delle figure, letta da `palette.json` che le sta accanto.

    import sys; sys.path.insert(0, "<brand>/figure")
    import palette

    palette.ruolo("fondo")        # ("#F8F5EE", "#16130F")
    palette.scuro("#5E5852")      # "#BCB3A1"
    palette.MAPPA_SCURA           # {chiaro: scuro} per chi ricolora per colore

Due modi di ricolorare, due ingressi. Chi sa il RUOLO di un elemento (il sito
lo ricava dalla geometria) usa `ruolo()`. Chi ricolora per esadecimale (le
copie scure del libro) usa `scuro()` o `MAPPA_SCURA`, che passano dai colori
e dai sinonimi del file: un colore che non c'e' solleva KeyError, perche'
indovinarlo darebbe una figura plausibile e sbagliata in un punto solo.
"""

from __future__ import annotations

import json
from pathlib import Path

_DATI = json.loads((Path(__file__).resolve().parent / "palette.json").read_text())

RUOLI: dict[str, tuple[str, str]] = {
    nome: (r["chiaro"], r["scuro"]) for nome, r in _DATI["ruoli"].items()
}

MAPPA_SCURA: dict[str, str] = {
    colore: RUOLI[ruolo][1]
    for sezione in ("colori", "sinonimi")
    for colore, ruolo in _DATI[sezione].items()
}


def ruolo(nome: str) -> tuple[str, str]:
    """(chiaro, scuro) di un ruolo."""
    return RUOLI[nome]


def scuro(colore: str) -> str:
    """La resa scura di un esadecimale della palette chiara."""
    return MAPPA_SCURA[colore.upper()]
