#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle de hauteurs et construction des gammes.

Source de vérité unique : les gravures LilyPond du guide et les fichiers
MusicXML sont dérivés de ce module. Écrire les deux à la main garantirait
qu'ils finissent par se contredire.

Une hauteur est un couple (lettre, altération) et non un numéro de demi-ton :
sol dièse et la bémol sonnent pareil mais ne s'écrivent pas pareil, et une
gamme se définit par son orthographe autant que par ses sons. C'est ce qui
permet d'obtenir si dièse majeur ou ré dièse mineur harmonique — avec son
double dièse — sans cas particulier.
"""

LETTRES = "CDEFGAB"
# Demi-tons de do à la lettre, dans l'octave.
DEMI_TONS = [0, 2, 4, 5, 7, 9, 11]

# Noms français, pour les tableaux du guide.
NOMS_FR = {"C": "do", "D": "ré", "E": "mi", "F": "fa",
           "G": "sol", "A": "la", "B": "si"}
ALT_FR = {-2: "double bémol", -1: "bémol", 0: "", 1: "dièse", 2: "double dièse"}


class Note:
    """Hauteur écrite : lettre, altération en demi-tons, octave (4 = octave du do central)."""

    __slots__ = ("lettre", "alt", "octave")

    def __init__(self, lettre, alt=0, octave=4):
        self.lettre = lettre
        self.alt = alt
        self.octave = octave

    @property
    def idx(self):
        return LETTRES.index(self.lettre)

    @property
    def hauteur(self):
        """Hauteur absolue en demi-tons ; do4 = 0."""
        return DEMI_TONS[self.idx] + self.alt + 12 * (self.octave - 4)

    def suivante(self, demi_tons):
        """
        Note à l'intervalle `demi_tons` au-dessus, sur la *lettre suivante*.

        C'est le cœur du modèle : la lettre est imposée par le degré, et
        l'altération s'en déduit. Une gamme n'emprunte jamais deux fois la même
        lettre, ce qui interdit d'écrire fa dièse puis sol bémol.
        """
        i = (self.idx + 1) % 7
        oct_suiv = self.octave + (1 if i == 0 else 0)
        # Altération telle que l'intervalle tombe juste.
        base = DEMI_TONS[i] + 12 * (oct_suiv - 4)
        alt = self.hauteur + demi_tons - base
        return Note(LETTRES[i], alt, oct_suiv)

    def alteree(self, d):
        """Même lettre, altération décalée de `d` demi-tons."""
        return Note(self.lettre, self.alt + d, self.octave)

    # --- sorties ---------------------------------------------------------
    def lily(self):
        suff = {-2: "eses", -1: "es", 0: "", 1: "is", 2: "isis"}[self.alt]
        # LilyPond : do3 = c, do4 = c', do5 = c''
        marque = "'" * (self.octave - 3) if self.octave >= 3 else "," * (3 - self.octave)
        return self.lettre.lower() + suff + marque

    def musicxml_step(self):
        return self.lettre

    def nom_fr(self):
        a = ALT_FR[self.alt]
        return NOMS_FR[self.lettre] + (" " + a if a else "")

    def __repr__(self):
        return f"{self.lettre}{'#' * self.alt if self.alt > 0 else 'b' * -self.alt}{self.octave}"


# ---------------------------------------------------------------------------
# Tétracordes
# ---------------------------------------------------------------------------
# Un tétracorde est un groupe de quatre notes couvrant une quarte juste
# (5 demi-tons). Trois intervalles le décrivent donc entièrement.
TETRACORDES = {
    "majeur":    (2, 2, 1),   # ton - ton - demi-ton
    "mineur":    (2, 1, 2),   # ton - demi-ton - ton   (dit « dorien »)
    "phrygien":  (1, 2, 2),   # demi-ton - ton - ton
    "harmonique": (1, 3, 1),  # demi-ton - seconde augmentée - demi-ton
    "lydien":    (2, 2, 2),   # ton - ton - ton : couvre un triton, pas une quarte
}

# Une gamme heptatonique = tétracorde inférieur + ton disjonctif + tétracorde
# supérieur. Ce tableau est la thèse du guide.
GAMMES = {
    "majeure":            ("majeur", "majeur"),
    "mineure naturelle":  ("mineur", "phrygien"),
    "mineure harmonique": ("mineur", "harmonique"),
    "mineure mélodique":  ("mineur", "majeur"),
}

TON_DISJONCTIF = 2


def intervalles(nom_gamme):
    """Les sept intervalles d'une gamme, du premier degré à l'octave."""
    bas, haut = GAMMES[nom_gamme]
    return list(TETRACORDES[bas]) + [TON_DISJONCTIF] + list(TETRACORDES[haut])


def gamme(tonique, nom_gamme):
    """Les huit notes écrites de la gamme, tonique incluse aux deux bouts."""
    notes = [tonique]
    for pas in intervalles(nom_gamme):
        notes.append(notes[-1].suivante(pas))
    return notes


def tetracorde(depart, type_):
    """Les quatre notes d'un tétracorde à partir de `depart`."""
    notes = [depart]
    for pas in TETRACORDES[type_]:
        notes.append(notes[-1].suivante(pas))
    return notes


# ---------------------------------------------------------------------------
# Les quinze tonalités
# ---------------------------------------------------------------------------
def note_de(txt, octave=4):
    """« Fa# » -> Note. Accepte # et b, simples ou doubles."""
    lettre = txt[0].upper()
    alt = txt[1:].count("#") - txt[1:].count("b")
    return Note(lettre, alt, octave)


# (armure, tonique majeure, tonique mineure relative)
# L'armure est signée : positive en dièses, négative en bémols. MusicXML et
# LilyPond utilisent tous deux cette convention.
TONALITES = [
    (-7, "Cb", "Ab"), (-6, "Gb", "Eb"), (-5, "Db", "Bb"), (-4, "Ab", "F"),
    (-3, "Eb", "C"),  (-2, "Bb", "G"),  (-1, "F", "D"),   (0, "C", "A"),
    (1, "G", "E"),    (2, "D", "B"),    (3, "A", "F#"),   (4, "E", "C#"),
    (5, "B", "G#"),   (6, "F#", "D#"),  (7, "C#", "A#"),
]

ORDRE_DIESES = "FCGDAEB"
ORDRE_BEMOLS = "BEADGCF"


def armure_notes(k):
    """Les lettres altérées par une armure de `k` dièses (>0) ou bémols (<0)."""
    if k > 0:
        return [ORDRE_DIESES[i] for i in range(k)]
    return [ORDRE_BEMOLS[i] for i in range(-k)]


def octave_depart(tonique, plancher=4):
    """
    Octave qui garde la gamme lisible sur une portée en clé de sol.

    Les toniques graves (la, si) partent de l'octave inférieure pour que la
    gamme ne sorte pas de la portée par le haut.
    """
    return plancher if tonique.idx <= 4 else plancher - 1
