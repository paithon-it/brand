"""
paithon_anim — tema Manim del brand paithon. FONTE UNICA.

Lo consumano sia il sito (`paithon`) sia il libro (`paithonbook`), montando
questa cartella nel container e mettendola su PYTHONPATH. Le scene fanno:

    from paithon_anim import *

    class MiaScena(ScenaPaithon):
        titolo_scena = "Come funziona"
        def costruisci(self):
            ...

Regola inviolabile: la palette e' quella FISSA delle illustrazioni editoriali
(5 colori + neutri warm). Niente gradienti, niente neon, niente glassmorphism.
Il testo e' il protagonista.

Le regole di composizione e i numeri del ritmo sono spiegati in README.md,
accanto a questo file; gli stessi valori stanno in `motion.css` per il web.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

import manimpango
from manim import *  # noqa: F401,F403

_QUI = Path(__file__).resolve().parent
_BRAND = _QUI.parent

# --------------------------------------------------------------------------
# Palette illustrazioni — FISSA. Identica ai token colore di tokens.css.
# --------------------------------------------------------------------------
TERRACOTTA = "#B5532C"   # accent primario
TEAL = "#2D5A5C"         # secondario
OCRA = "#C9A961"         # terziario
INK = "#1A1A1A"          # warm black
CREAM = "#F8F5EE"        # sfondo

# Neutri warm (--pt-fg-muted / --pt-fg-subtle / --pt-border*)
FG_MUTED = "#5A524A"
FG_SUBTLE = "#8C8478"
BORDER = "#E2DCC9"
BORDER_STRONG = "#C5BEAA"

# Varianti dark ufficiali (blocco [data-theme="dark"] di tokens.css): piu'
# luminose per reggere sul fondo scuro, mai neon.
TERRACOTTA_DARK = "#E27B52"
TEAL_DARK = "#5BA39C"
OCRA_DARK = "#DDB874"
INK_DEEP = "#0E0C0A"
OSSO = "#F4ECDD"
FG_MUTED_DARK = "#BCB3A1"
FG_SUBTLE_DARK = "#8E8676"

# --------------------------------------------------------------------------
# Tema attivo — variabile d'ambiente PAITHON_TEMA (chiaro | scuro).
#
# Nel libro NON serve la variante scura: le pagine invertono le <img> in dark
# mode via CSS. Serve per social, slide e ovunque il file venga usato cosi'
# com'e' su fondo scuro.
# --------------------------------------------------------------------------
TEMA = os.environ.get("PAITHON_TEMA", "chiaro").strip().lower()
SCURO = TEMA in ("scuro", "dark")

SFONDO = INK_DEEP if SCURO else CREAM
TESTO = OSSO if SCURO else INK
TESTO_TENUE = FG_MUTED_DARK if SCURO else FG_MUTED
TESTO_LIEVE = FG_SUBTLE_DARK if SCURO else FG_SUBTLE
FILETTO = "#34302A" if SCURO else BORDER_STRONG

PRIMARIO = TERRACOTTA_DARK if SCURO else TERRACOTTA
SECONDARIO = TEAL_DARK if SCURO else TEAL
TERZIARIO = OCRA_DARK if SCURO else OCRA

# Sequenza d'uso quando servono piu' colori: terracotta e' l'accent caldo
# dominante, teal e ocra restano di supporto.
CICLO = [PRIMARIO, SECONDARIO, TERZIARIO]


def accento(i: int) -> str:
    """Colore d'accento i-esimo, ciclico. Utile nei cicli `for`."""
    return CICLO[i % len(CICLO)]


# --------------------------------------------------------------------------
# Font — registrati a runtime da file, senza toccare fontconfig di sistema.
# I WOFF2 del tema non sono leggibili da Pango: servono i TTF.
# --------------------------------------------------------------------------
_FONT_CANDIDATES = {
    "Fraunces": ["fraunces-600-og.ttf", "Fraunces.ttf"],
    "Inter": ["inter-400-og.ttf", "Inter.ttf"],
    "JetBrains Mono": ["jetbrains-mono.ttf", "JetBrainsMono.ttf"],
}

# In ordine di preferenza: i font del brand accanto a questo file vincono,
# poi i mount storici dei due driver (/fonts del sito, /skill/fonts).
_FONT_DIRS = [_QUI / "fonts", Path("/brand/motion/fonts"), Path("/fonts"), Path("/skill/fonts")]


def _register_fonts():
    """Registra i font paithon in Pango. Ritorna le famiglie disponibili."""
    for names in _FONT_CANDIDATES.values():
        registrato = False
        for name in names:
            for d in _FONT_DIRS:
                p = d / name
                if p.is_file():
                    manimpango.register_font(str(p))
                    registrato = True
                    break
            if registrato:
                break
    return set(manimpango.list_fonts())


_AVAILABLE = _register_fonts()

# Fallback onesti: se un font non c'e', si degrada invece di crashare.
DISPLAY = "Fraunces" if "Fraunces" in _AVAILABLE else "Nimbus Roman"
BODY = "Inter" if "Inter" in _AVAILABLE else "Nimbus Sans"
MONO = "JetBrains Mono" if "JetBrains Mono" in _AVAILABLE else "Noto Sans Mono"

# --------------------------------------------------------------------------
# Scala tipografica — in unita' Manim (l'altezza del frame e' 8).
# --------------------------------------------------------------------------
T_TITOLO = 0.60
T_SOTTO = 0.36
T_CORPO = 0.30
T_ETICHETTA = 0.26
T_PICCOLO = 0.22

# Sotto ~48pt Pango arrotonda le advance width dei glifi e il testo esce con
# buchi ("Com e funziona") o al contrario tutto appiccicato. Costruiamo SEMPRE
# a 96pt e riscaliamo: stessa dimensione a video, spaziatura corretta.
# Verificato: a 16/20/26/30 l'artefatto c'e', a 48/72/120 sparisce.
_FS_BASE = 96


def _testo(testo, scala, font, colore, **kw):
    t = Text(testo, font=font, font_size=_FS_BASE, color=colore, **kw)
    return t.scale(scala * 100 / _FS_BASE)


def _adatta_frame():
    """Riallinea il sistema di coordinate alla risoluzione reale.

    Manim con `-r 720,1280` aggiorna pixel_width/height e aspect_ratio ma
    LASCIA frame_width/frame_height ai valori 16:9 (14.22 x 8). Risultato: in
    verticale la scena resta schiacciata al centro e to_corner() finisce nel
    posto sbagliato. Qui il lato corto vale sempre 8 unita'.
    """
    a = config.pixel_width / config.pixel_height
    if a >= 1:
        config.frame_height, config.frame_width = 8.0, 8.0 * a
    else:
        config.frame_width, config.frame_height = 8.0, 8.0 / a


# DEVE girare all'import, non dentro construct(): la camera legge frame_width
# quando la Scene viene istanziata, cioe' dopo l'import del file di scena ma
# prima di construct(). Farlo dopo lascia camera e coordinate disallineate.
_adatta_frame()


# --------------------------------------------------------------------------
# Firma di copyright — bollo tribar + "paithon.it", in basso a destra.
# --------------------------------------------------------------------------

_MARK = _BRAND / "logos" / "paithon-mark.svg"
_mark_pronto = None


def _mark_scrivibile():
    """Copia del bollo in una cartella scrivibile.

    SVGMobject non si limita a leggere: accanto al sorgente scrive un file
    normalizzato (`paithon-mark_.svg`). I driver montano il brand in sola
    lettura, quindi caricarlo da li' fallisce con `Read-only file system`.
    """
    global _mark_pronto
    if _mark_pronto is None and _MARK.is_file():
        d = Path(tempfile.mkdtemp(prefix="paithon-brand-"))
        _mark_pronto = d / _MARK.name
        shutil.copy2(_MARK, _mark_pronto)
    return _mark_pronto


def firma_paithon(altezza=0.30, colore_nome=None) -> VGroup:
    """Il segno del brand piu' il dominio: sta in ogni animazione pubblicata.

    Il bollo e' l'SVG ufficiale (`logos/paithon-mark.svg`). Il suo tratto e'
    pensato per il favicon: a questa scala Manim NON riscala lo stroke, che
    coprirebbe i tre colori facendo un triangolo nero. Per questo si azzera.
    """
    pezzi = []
    sorgente = _mark_scrivibile()
    if sorgente is not None:
        try:
            mark = SVGMobject(str(sorgente))
            mark.set_stroke(width=0)
            mark.height = altezza
            pezzi.append(mark)
        except Exception as e:  # meglio la firma testuale che un crash, ma si dice
            print(f"! bollo non caricato ({type(e).__name__}: {e}) — firma solo testuale",
                  file=sys.stderr)
    else:
        print(f"! bollo non trovato in {_MARK} — firma solo testuale", file=sys.stderr)
    nome = _testo("paithon.it", 0.21, DISPLAY, colore_nome or TESTO_TENUE, weight=BOLD)
    return VGroup(*pezzi, nome).arrange(RIGHT, buff=0.13)


class ScenaPaithon(Scene):
    """Base per tutte le animazioni paithon.

    Imposta lo sfondo, espone gli helper tipografici e la firma di copyright.
    Le scene concrete implementano `costruisci()`, non `construct()`.
    """

    firma = True          # bollo + "paithon.it" in basso a destra
    titolo_scena = None   # se valorizzato, viene disegnato in alto

    def construct(self):
        self.camera.background_color = SFONDO
        if self.firma:
            self._firma()
        if self.titolo_scena:
            self.intesta(self.titolo_scena)
        self.costruisci()

    def costruisci(self):
        raise NotImplementedError("Implementa costruisci() nella tua scena")

    # -- tipografia -------------------------------------------------------
    def titolo(self, testo, scala=T_TITOLO, colore=None, **kw):
        kw.setdefault("weight", BOLD)
        return _testo(testo, scala, DISPLAY, colore or TESTO, **kw)

    def corpo(self, testo, scala=T_CORPO, colore=None, **kw):
        return _testo(testo, scala, BODY, colore or TESTO, **kw)

    def etichetta(self, testo, scala=T_ETICHETTA, colore=None, **kw):
        return _testo(testo, scala, BODY, colore or TESTO_TENUE, **kw)

    def codice(self, testo, scala=T_ETICHETTA, colore=None, **kw):
        return _testo(testo, scala, MONO, colore or TESTO, **kw)

    def formula(self, tex, scala=1.0, colore=None, **kw):
        """LaTeX vero (TeX Live e' dentro l'immagine Docker).

        `tex` puo' essere una stringa o una lista di pezzi: con la lista ogni
        pezzo resta indicizzabile (f[2]) per evidenziarlo separatamente.
        """
        pezzi = [tex] if isinstance(tex, str) else list(tex)
        return MathTex(*pezzi, color=colore or TESTO, **kw).scale(scala)

    def eyebrow(self, testo, colore=None, scala=T_PICCOLO):
        """Occhiello maiuscoletto, come le pillole meta del sito."""
        return _testo(testo.upper(), scala, BODY, colore or SECONDARIO, weight=SEMIBOLD)

    def didascalia(self, testo, scala=T_ETICHETTA, colore=None):
        """Riga di servizio in basso: dice cosa si e' visto.

        Sta a sinistra della firma, non centrata sul frame: al centro finirebbe
        sotto il bollo nelle composizioni larghe.
        """
        t = _testo(testo, scala, BODY, colore or TESTO_TENUE)
        t.to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.55)
        return t

    # -- elementi ---------------------------------------------------------
    def intesta(self, testo):
        """Titolo fisso in alto a sinistra + filetto di separazione."""
        t = self.titolo(testo, scala=T_SOTTO).to_corner(UL, buff=0.5)
        riga = Line(LEFT, RIGHT, color=FILETTO, stroke_width=2)
        riga.set_width(config.frame_width - 1.0)
        riga.next_to(t, DOWN, buff=0.22, aligned_edge=LEFT).set_x(0)
        self.add(t, riga)
        self._testata = VGroup(t, riga)
        return self._testata

    def centra(self, mob, margine_basso=0.75, margine_lato=0.7):
        """Centra nell'area libera tra testata e firma, rientrando se sborda.

        Senza questo il contenuto resta centrato sul frame intero e sotto la
        testata si apre una banda vuota che sbilancia la composizione. Il
        rientro in larghezza serve soprattutto in verticale (--vertical): il
        frame passa da 14.2 a 8 unita' e una composizione pensata per il 16:9
        uscirebbe dai bordi.
        """
        alto = (self._testata.get_bottom()[1] - 0.35
                if getattr(self, "_testata", None) is not None
                else config.frame_height / 2 - 0.4)
        basso = -config.frame_height / 2 + margine_basso
        larghezza_max = config.frame_width - 2 * margine_lato

        if mob.width > larghezza_max:
            mob.scale_to_fit_width(larghezza_max)
        if mob.height > alto - basso:
            mob.scale_to_fit_height(alto - basso)
        mob.move_to([0, (alto + basso) / 2, 0])
        return mob

    def scatola(self, testo, colore=None, larghezza=3.0, riempimento=0.0,
                mono=False):
        """Nodo rettangolare con etichetta — mattone dei diagrammi di flusso."""
        lab = (self.codice(testo) if mono else self.corpo(testo, T_ETICHETTA))
        lab.set_color(TESTO)
        box = RoundedRectangle(
            corner_radius=0.08,
            width=max(larghezza, lab.width + 0.6),
            height=lab.height + 0.55,
            stroke_color=colore or SECONDARIO, stroke_width=3,
            fill_color=colore or SECONDARIO, fill_opacity=riempimento,
        )
        return VGroup(box, lab.move_to(box))

    def freccia(self, da, a, colore=None, buff=0.18):
        return Arrow(da, a, color=colore or TESTO_TENUE, buff=buff, stroke_width=3,
                     max_tip_length_to_length_ratio=0.16,
                     tip_length=0.2)

    def assi(self, x_range=(0, 6, 1), y_range=(0, 4, 1), larghezza=8.0,
             altezza=4.0, **kw):
        """Assi in palette: tratto tenue, niente griglia rumorosa, niente punte.

        Serve ai grafici del libro (curve di costo, funzioni d'attivazione).
        """
        kw.setdefault("tips", False)
        config_asse = {"color": TESTO_TENUE, "stroke_width": 3,
                       "include_numbers": False, "font_size": 24}
        config_asse.update(kw.pop("axis_config", {}))
        return Axes(x_range=list(x_range), y_range=list(y_range),
                    x_length=larghezza, y_length=altezza,
                    axis_config=config_asse, **kw)

    def riquadro(self, mob, colore=None, **kw):
        """Riquadro d'evidenziazione attorno a un mobject."""
        kw.setdefault("buff", 0.2)
        kw.setdefault("corner_radius", 0.08)
        kw.setdefault("stroke_width", 3)
        return SurroundingRectangle(mob, color=colore or PRIMARIO, **kw)

    # -- ritmo ------------------------------------------------------------
    def pausa(self, t=None):
        self.wait(PAUSA if t is None else t)

    def chiusura(self, t=None):
        """Pausa finale: da' il tempo di leggere prima che il loop riparta."""
        self.wait(PAUSA_FINALE if t is None else t)

    def _firma(self):
        f = firma_paithon()
        f.to_corner(DR, buff=0.3)
        self.add(f)
        self._firma_mob = f
        return f


class ScenaVerticale(ScenaPaithon):
    """Variante 9:16 per storie/social. Il driver imposta il formato."""


# --------------------------------------------------------------------------
# Ritmo: durate coerenti con "transition base 200ms" del design system,
# riscalate al video (una GIF di 6-10s non regge tempi da UI).
# Gli stessi numeri stanno in motion.css come --pt-motion-*.
# --------------------------------------------------------------------------
RAPIDO = 0.4
NORMALE = 0.7
LENTO = 1.1
PAUSA = 0.9
PAUSA_FINALE = 1.6


def bezier_css(x1, y1, x2, y2):
    """Rate function equivalente alla `cubic-bezier(x1,y1,x2,y2)` del CSS.

    Serve a far combaciare davvero il movimento del sito e quello delle clip:
    invece di cercare la rate function di Manim "piu' somigliante", si usa la
    stessa curva dei token. Come i browser: si risolve x(u)=t e si valuta y(u).
    """
    def f(t):
        t = min(1.0, max(0.0, float(t)))
        lo, hi = 0.0, 1.0
        for _ in range(24):  # ~1e-7 di precisione, irrilevante il costo
            u = (lo + hi) / 2
            x = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u ** 2 * x2 + u ** 3
            if x < t:
                lo = u
            else:
                hi = u
        u = (lo + hi) / 2
        return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3
    return f


#: La curva del design system: `--pt-ease-out` in tokens.css. Decelerazione
#: morbida senza overshoot, la stessa di card e view-transition del sito.
EASE_OUT = bezier_css(0.22, 1, 0.36, 1)


def entra(*mobs, shift=UP * 0.25, run_time=NORMALE, lag=0.12, rate_func=EASE_OUT):
    """Fade-in con micro-shift: l'equivalente del fade-in-on-scroll del sito.

    Stessa curva (`--pt-ease-out`) e stesso spostamento del CSS: un blocco che
    entra in una pagina e un elemento che entra in una clip si muovono uguale.
    """
    return AnimationGroup(
        *[FadeIn(m, shift=shift, run_time=run_time, rate_func=rate_func) for m in mobs],
        lag_ratio=lag,
    )


def dentro_frame(mob, margine=0.4):
    """Rientra un mobject nel frame se sborda a sinistra o a destra.

    Serve soprattutto alle timeline: le etichette del primo e dell'ultimo
    punto escono sempre dall'inquadratura, e Manim non se ne accorge.
    """
    limite = config.frame_width / 2 - margine
    if mob.get_left()[0] < -limite:
        mob.shift(RIGHT * (-limite - mob.get_left()[0]))
    if mob.get_right()[0] > limite:
        mob.shift(LEFT * (mob.get_right()[0] - limite))
    return mob


def sottolinea(mob, colore=None, run_time=NORMALE):
    """Underline che si forma da sinistra — come i link del tema."""
    riga = Line(
        mob.get_corner(DL) + DOWN * 0.12,
        mob.get_corner(DR) + DOWN * 0.12,
        color=colore or PRIMARIO, stroke_width=4,
    )
    return Create(riga, run_time=run_time), riga


def evidenzia(mob, colore=None, scala=1.15):
    """Animazione di richiamo su un elemento gia' in scena."""
    return Indicate(mob, color=colore or PRIMARIO, scale_factor=scala)
