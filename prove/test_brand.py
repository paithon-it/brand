"""Le prove del brand: quello che una copia sbagliata non mostrerebbe a occhio.

    python3 -m unittest discover -s prove

Solo libreria standard: il brand non ha dipendenze e non deve averne per
verificare se stesso. Ogni prova nasce da un errore che e' gia' successo in un
consumatore (un colore dichiarato in un tema solo, una mappa delle figure
copiata a mano e rimasta indietro, un testo chiaro fisso sopra un accento che
nello scuro si schiarisce).
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

BRAND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BRAND / "figure"))


# --------------------------------------------------------------------------
# Lettura dei fogli: quanto basta per i token, non un parser CSS
# --------------------------------------------------------------------------
def _senza_commenti(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _blocco(css: str, selettore: str) -> str:
    """Il corpo del primo blocco che si apre subito dopo `selettore`."""
    i = css.index(selettore)
    i = css.index("{", i) + 1
    profondita, j = 1, i
    while profondita:
        if css[j] == "{":
            profondita += 1
        elif css[j] == "}":
            profondita -= 1
        j += 1
    return css[i:j - 1]


def _dichiarazioni(corpo: str) -> dict[str, str]:
    return {m.group(1): " ".join(m.group(2).split())
            for m in re.finditer(r"(--pt-[\w-]+)\s*:\s*([^;]+);", corpo)}


TOKENS = _senza_commenti((BRAND / "tokens.css").read_text())
CHIARO = _dichiarazioni(_blocco(TOKENS, ":root {"))
SCURO_ATTR = _dichiarazioni(_blocco(TOKENS, '[data-theme="dark"] {'))
SCURO_MEDIA = _dichiarazioni(
    _blocco(_blocco(TOKENS, "@media (prefers-color-scheme: dark)"),
            ':root:not([data-theme="light"])'))
STAMPA = _dichiarazioni(_blocco(
    _senza_commenti((BRAND / "print.css").read_text()), "@media print {"))

TEMI = {
    "chiaro": CHIARO,
    "scuro": {**CHIARO, **SCURO_ATTR},
    "stampa": {**CHIARO, **STAMPA},
}


def risolvi(tema: dict[str, str], nome: str) -> str:
    valore = tema[nome]
    m = re.fullmatch(r"var\((--pt-[\w-]+)(?:,[^)]*)?\)", valore)
    return risolvi(tema, m.group(1)) if m else valore


def _lineare(x: float) -> float:
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def luminanza(colore: str) -> float:
    r, g, b = (_lineare(int(colore[i:i + 2], 16) / 255) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrasto(a: str, b: str) -> float:
    la, lb = luminanza(a), luminanza(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


ESADECIMALE = re.compile(r"#[0-9A-F]{6}")


# --------------------------------------------------------------------------
class TemaScuro(unittest.TestCase):
    """Lo scuro si dichiara due volte (attributo e preferenza di sistema)."""

    def test_i_due_blocchi_scuri_coincidono(self):
        # Il bug di agosto 2026: verde e ocra di sistema vivevano in un tema
        # solo. Qui la stessa cosa fra i due modi di chiedere lo scuro.
        self.assertEqual(SCURO_ATTR, SCURO_MEDIA)


class TestoSopraUnAccento(unittest.TestCase):
    COPPIE = {
        "--pt-on-accent": "--pt-accent",
        "--pt-on-accent-2": "--pt-accent-2",
        "--pt-on-accent-3": "--pt-accent-3",
        "--pt-on-success-solid": "--pt-success-solid",
    }

    def test_regge_a_schermo_in_tutti_e_due_i_temi(self):
        for tema in ("chiaro", "scuro"):
            valori = TEMI[tema]
            for testo, fondo in self.COPPIE.items():
                with self.subTest(tema=tema, testo=testo):
                    k = contrasto(risolvi(valori, testo), risolvi(valori, fondo))
                    self.assertGreaterEqual(k, 4.5, f"{testo} su {fondo}: {k:.2f}:1")

    def test_in_stampa_si_legge_sulla_carta(self):
        # Il browser di default non stampa gli sfondi: la campitura sparisce
        # e il testo finisce sulla carta. Un testo chiaro sarebbe invisibile.
        for testo in self.COPPIE:
            with self.subTest(testo=testo):
                k = contrasto(risolvi(TEMI["stampa"], testo), "#FFFFFF")
                self.assertGreaterEqual(k, 4.5, f"{testo} sulla carta: {k:.2f}:1")


class TavolozzaDelCodice(unittest.TestCase):
    RUOLI = ("fg", "kw", "str", "com", "dec", "num")

    def test_si_legge_sui_fondi_del_codice(self):
        for tema, valori in TEMI.items():
            for fondo in ("--pt-bg", "--pt-bg-elev"):
                for ruolo in self.RUOLI:
                    with self.subTest(tema=tema, fondo=fondo, ruolo=ruolo):
                        k = contrasto(risolvi(valori, f"--pt-code-{ruolo}"),
                                      risolvi(valori, fondo))
                        self.assertGreaterEqual(k, 4.5, f"{ruolo} su {fondo}: {k:.2f}:1")


class Tipografia(unittest.TestCase):
    def test_il_corpo_piu_piccolo_non_scende_sotto_i_12_px(self):
        valore = CHIARO["--pt-text-xs"]
        self.assertTrue(valore.endswith("rem"), valore)
        self.assertGreaterEqual(float(valore[:-3]), 0.75)

    @staticmethod
    def _px(valore: str, larghezza: float) -> float:
        """Un `clamp(a rem, b rem + c vw, d rem)` valutato a una larghezza."""
        m = re.fullmatch(r"clamp\(([\d.]+)rem, ([\d.]+)rem \+ ([\d.]+)vw, "
                         r"([\d.]+)rem\)", valore)
        assert m, valore
        lo, base, vw, hi = (float(x) for x in m.groups())
        return min(max(lo * 16, base * 16 + vw * larghezza / 100), hi * 16)

    def test_la_scala_di_lettura_scende_a_ogni_gradino(self):
        livelli = ["--pt-prose-h1", "--pt-prose-h2", "--pt-prose-h3",
                   "--pt-prose-h4", "--pt-prose-h5", "--pt-prose-body"]
        for larghezza in (320, 390, 768, 1024, 1280, 1440, 1920):
            misure = [self._px(CHIARO[k], larghezza) for k in livelli]
            for alto, basso, nome in zip(misure, misure[1:], livelli[1:]):
                self.assertGreater(alto, basso, f"{nome} a {larghezza}px")

    def test_il_corpo_di_lettura_resta_nel_corpo_fluido(self):
        for larghezza in (320, 768, 1440, 1920):
            lettura = self._px(CHIARO["--pt-prose-body"], larghezza)
            self.assertGreaterEqual(lettura, 16, larghezza)
            self.assertLessEqual(
                lettura, self._px(CHIARO["--pt-text-body-fluid"], 1920))

    def test_il_titolo_di_sezione_in_ocra_si_legge_ovunque(self):
        # L'ocra piena sul crema sta a 2,1:1: il titolo d'oro e' l'ocra da
        # testo, che si ribalta col tema. Si chiede il 4,5 del testo normale
        # anche se e' un titolo, perche' su telefono l'h2 scende a 24px.
        for tema, valori in TEMI.items():
            for fondo in ("--pt-bg", "--pt-bg-elev"):
                with self.subTest(tema=tema, fondo=fondo):
                    k = contrasto(risolvi(valori, "--pt-prose-h2-color"),
                                  risolvi(valori, fondo))
                    self.assertGreaterEqual(k, 4.5, f"h2 su {fondo}: {k:.2f}:1")


# --------------------------------------------------------------------------
class PaletteDelleFigure(unittest.TestCase):
    def setUp(self):
        self.dati = json.loads((BRAND / "figure" / "palette.json").read_text())
        self.ruoli = self.dati["ruoli"]

    def test_gli_esadecimali_sono_maiuscoli_e_completi(self):
        for nome, r in self.ruoli.items():
            for tema in ("chiaro", "scuro"):
                with self.subTest(ruolo=nome, tema=tema):
                    self.assertRegex(r[tema], ESADECIMALE)
        for sezione in ("colori", "sinonimi"):
            for colore in self.dati[sezione]:
                self.assertRegex(colore, ESADECIMALE)

    def test_lo_scuro_e_il_token_che_dichiara(self):
        # La mappa delle figure era copiata a mano in due repo, e una delle
        # due e' rimasta all'ocra di prima. Qui la mappa nomina il token e il
        # valore deve essere quello del blocco scuro di tokens.css.
        for nome, r in self.ruoli.items():
            if "token" not in r:
                continue
            with self.subTest(ruolo=nome):
                self.assertEqual(r["scuro"], risolvi(TEMI["scuro"], r["token"]).upper())

    def test_il_chiaro_e_quello_dei_token_delle_illustrazioni(self):
        for nome, r in self.ruoli.items():
            if "illus" not in r:
                continue
            with self.subTest(ruolo=nome):
                self.assertEqual(r["chiaro"], CHIARO[r["illus"]].upper())

    def test_colori_e_sinonimi_puntano_a_ruoli_che_esistono(self):
        for sezione in ("colori", "sinonimi"):
            for colore, ruolo in self.dati[sezione].items():
                with self.subTest(colore=colore):
                    self.assertIn(ruolo, self.ruoli)
        for colore, ruolo in self.dati["colori"].items():
            with self.subTest(colore=colore):
                self.assertEqual(self.ruoli[ruolo]["chiaro"], colore)
        self.assertFalse(set(self.dati["colori"]) & set(self.dati["sinonimi"]))

    def test_il_modulo_legge_la_stessa_mappa(self):
        import palette

        self.assertEqual(palette.ruolo("fondo"), ("#F8F5EE", "#16130F"))
        self.assertEqual(palette.scuro("#c9a961"), "#C9A961")
        self.assertEqual(palette.scuro("#5A524A"), palette.scuro("#5E5852"))
        with self.assertRaises(KeyError):
            palette.scuro("#123456")
        for chiaro, scuro in palette.MAPPA_SCURA.items():
            self.assertRegex(chiaro, ESADECIMALE)
            self.assertRegex(scuro, ESADECIMALE)

    def test_il_motore_manim_disegna_lo_scuro_con_la_stessa_mappa(self):
        sorgente = (BRAND / "motion" / "paithon_anim.py").read_text()
        self.assertNotRegex(sorgente, r'INK_DEEP\s*=\s*"#')
        self.assertIn("palette", sorgente)


# --------------------------------------------------------------------------
class FontWeb(unittest.TestCase):
    def setUp(self):
        self.css = _senza_commenti((BRAND / "fonts.css").read_text())
        self.facce = [_dichiarazioni_qualsiasi(m.group(1))
                      for m in re.finditer(r"@font-face\s*{([^}]*)}", self.css)]

    def test_ogni_file_citato_esiste(self):
        url = re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", self.css)
        self.assertTrue(url)
        for u in url:
            with self.subTest(url=u):
                self.assertTrue((BRAND / u).is_file(), u)

    def test_famiglie_e_pesi_sono_quelli_di_fonts_md(self):
        attese = {
            ("Fraunces", "normal"): "400 800",
            ("Fraunces", "italic"): "400 800",
            ("Inter", "normal"): "400 600",
            ("JetBrains Mono", "normal"): "400 600",
        }
        trovate = {}
        for f in self.facce:
            if "url(" not in f.get("src", ""):
                continue                  # i ripieghi metrici, con local()
            chiave = (f["font-family"].strip("'\""), f["font-style"])
            trovate.setdefault(chiave, set()).add(f["font-weight"])
        self.assertEqual({k: {v} for k, v in attese.items()}, trovate)


def _dichiarazioni_qualsiasi(corpo: str) -> dict[str, str]:
    return {m.group(1): " ".join(m.group(2).split())
            for m in re.finditer(r"([\w-]+)\s*:\s*([^;]+);", corpo)}


class Aurora(unittest.TestCase):
    def test_la_deriva_non_gira_all_infinito(self):
        css = _senza_commenti((BRAND / "aurora.css").read_text())
        animazioni = re.findall(r"animation:\s*(pt-gas[^;]+);", css)
        self.assertEqual(len(animazioni), 2)
        for a in animazioni:
            self.assertNotIn("infinite", a)


class Licenza(unittest.TestCase):
    def test_ogni_cartella_di_font_e_nell_eccezione_ofl(self):
        licenza = (BRAND / "LICENSE").read_text()
        for cartella in ("fonts/", "motion/fonts/", "stampa/fonts/"):
            with self.subTest(cartella=cartella):
                self.assertIn(f"`{cartella}`", licenza)
                self.assertTrue((BRAND / cartella / "NOTICE.md").is_file())


if __name__ == "__main__":
    unittest.main()
