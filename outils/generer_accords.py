#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, les tableaux, les réponses de l'exercice et le fichier
MusicXML du guide « Les accords ».

    python3 outils/generer_accords.py

Un accord y est une pile de tierces prise dans une gamme : la fondamentale,
puis une lettre sur deux. Sa nature se mesure sur les intervalles qu'il forme
avec sa fondamentale, sa position sur la note qu'il a à la basse. Les accords
des gravures et de l'exercice sont construits ainsi, puis analysés en sens
inverse — à partir des seules notes écrites, comme le ferait un lecteur — et
les deux doivent concorder. Les affirmations du texte — la nature des accords
sur chaque degré, la structure de la septième de dominante et de la septième
diminuée, le chiffrage de chaque renversement — sont vérifiées sur les quinze
tonalités majeures et mineures avant toute écriture.
"""

import os
import sys
from collections import namedtuple
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import LETTRES, TONALITES, Note, gamme, note_de
from generer import DIR_LY, PREAMBULE, RACINE, ecrire
from intervalles import abrege, analyser, au_dessus
import musicxml

PREAMBULE_ACCORDS = PREAMBULE.replace("outils/generer.py", "outils/generer_accords.py")

# Dans le fichier MusicXML, chaque accord dure une ronde, à la noire 120 :
# deux secondes.
TEMPO = 120
RONDE = Fraction(1)

# ---------------------------------------------------------------------------
# Modèle : l'accord, pile de tierces
# ---------------------------------------------------------------------------
# Les accords se bâtissent sur la gamme majeure et, en mineur, sur la gamme
# mineure harmonique, celle qui a une sensible.
GAMME_DU_MODE = {"majeur": "majeure", "mineur": "mineure harmonique"}
ROMAINS = ["I", "II", "III", "IV", "V", "VI", "VII"]
MEMBRES = ["fondamentale", "tierce", "quinte", "septième"]
POSITIONS = ["position fondamentale", "premier renversement",
             "deuxième renversement", "troisième renversement"]

# Nature d'un accord, selon les qualités de sa tierce, de sa quinte et de sa
# septième, mesurées depuis la fondamentale.
NATURES = {
    ("majeure", "juste"): "accord parfait majeur",
    ("mineure", "juste"): "accord parfait mineur",
    ("mineure", "diminuée"): "accord de quinte diminuée",
    ("majeure", "augmentée"): "accord de quinte augmentée",
    ("majeure", "juste", "mineure"): "septième de dominante",
    ("mineure", "diminuée", "diminuée"): "septième diminuée",
    ("mineure", "diminuée", "mineure"): "septième de sensible",
}
# Abrégés des natures des accords de trois sons, sous les gravures.
ABREGES_NATURES = {"accord parfait majeur": "M", "accord parfait mineur": "m",
                   "accord de quinte diminuée": "dim.",
                   "accord de quinte augmentée": "aug."}

# Les mêmes, sans « accord », dans les tableaux.
COURTES = {"accord parfait majeur": "parfait majeur", "accord parfait mineur": "parfait mineur",
           "accord de quinte diminuée": "quinte diminuée",
           "accord de quinte augmentée": "quinte augmentée"}

# Le chiffrage abrégé de chaque position, selon le nombre de sons.
CHIFFRAGES = {3: ["5", "6", "6/4"], 4: ["7", "6/5", "4/3", "2"]}

Ton = namedtuple("Ton", "tonique mode")


def nom_ton(ton):
    """« la mineur », « si bémol majeur » : une tonalité est masculine."""
    return f"{ton.tonique.nom_fr()} {ton.mode}"


def echelle(ton):
    """Les sept degrés de la gamme, de la tonique à la sensible."""
    return gamme(ton.tonique, GAMME_DU_MODE[ton.mode])[:7]


def sur_degre(ton, degre, sons=3):
    """
    L'accord bâti sur un degré : la fondamentale, puis une lettre sur deux
    dans la gamme, en montant. Fondamentale, tierce, quinte, septième.
    """
    g = echelle(ton)
    res = []
    for k in range(sons):
        i = degre - 1 + 2 * k
        x = g[i % 7]
        res.append(Note(x.lettre, x.alt, x.octave + i // 7))
    return res


def octavier(note, d):
    return Note(note.lettre, note.alt, note.octave + d)


def renverser(notes, position):
    """Le membre `position` à la basse, les autres serrés au-dessus."""
    return notes[position:] + [octavier(x, 1) for x in notes[:position]]


def ecarter(notes):
    """
    Position large : la basse reste, la note qui la suit monte d'une octave.
    Do, mi, sol devient do, sol, mi ; les membres ne changent pas.
    """
    return [notes[0]] + notes[2:] + [octavier(notes[1], 1)]


def lignes_supplementaires(notes):
    """Ce qui dépasse la portée en clé de sol (mi3 à fa4), en demi-tons."""
    bas, haut = Note("E", 0, 4).hauteur, Note("F", 0, 5).hauteur
    return sum(max(0, bas - x.hauteur) + max(0, x.hauteur - haut) for x in notes)


def placer(notes):
    """L'accord transposé à l'octave qui le garde au plus près de la portée."""
    return min(([octavier(x, d) for x in notes] for d in range(-2, 3)),
               key=lignes_supplementaires)


# ---------------------------------------------------------------------------
# Analyse : des notes écrites à l'accord
# ---------------------------------------------------------------------------
Analyse = namedtuple("Analyse", "fondamentale membres sons qualites nature position chiffrage")


def au_dessus_de(fondamentale, note):
    """(numéro, qualité) d'une note au-dessus de la fondamentale, dans l'octave."""
    octave = fondamentale.octave + (1 if note.idx < fondamentale.idx else 0)
    return analyser(fondamentale, Note(note.lettre, note.alt, octave))


def analyser_accord(notes):
    """
    Ce qu'un lecteur tire des notes écrites : il les range en tierces, ce qui
    désigne la fondamentale, mesure les intervalles qu'elle forme avec les
    autres, et regarde la note la plus grave.

    La quinte peut manquer : la fondamentale et la tierce suffisent à
    désigner l'accord. Sa qualité vaut alors None, et la nature est celle dont
    les autres qualités concordent.
    """
    alterations = {}
    for x in notes:
        # Une lettre, une altération : un accord n'emploie pas do et do dièse.
        assert alterations.setdefault(x.lettre, x.alt) == x.alt, notes
    candidates = []
    for lettre, alt in alterations.items():
        i = LETTRES.index(lettre)
        ecarts = {(LETTRES.index(m) - i) % 7 for m in alterations}
        if {0, 2} <= ecarts <= {0, 2, 4, 6}:
            candidates.append((Note(lettre, alt, 4), ecarts))
    # Une seule note se prête à porter la pile de tierces.
    assert len(candidates) == 1, notes
    fondamentale, ecarts = candidates[0]
    sons = 4 if 6 in ecarts else 3
    membres = sorted((Note(l, a, 4) for l, a in alterations.items()),
                     key=lambda x: (x.idx - fondamentale.idx) % 7)
    par_ecart = {(x.idx - fondamentale.idx) % 7: x for x in membres}
    qualites = tuple(au_dessus_de(fondamentale, par_ecart[e])[1] if e in par_ecart else None
                     for e in (2, 4, 6)[:sons - 1])
    possibles = [nature for cle, nature in NATURES.items()
                 if len(cle) == len(qualites)
                 and all(q is None or q == c for q, c in zip(qualites, cle))]
    basse = min(notes, key=lambda x: x.hauteur)
    position = ((basse.idx - fondamentale.idx) % 7) // 2
    return Analyse(fondamentale, membres, sons, qualites,
                   possibles[0] if len(possibles) == 1 else None, position,
                   CHIFFRAGES[sons][position])


def chiffrage_complet(notes):
    """Les intervalles des autres notes au-dessus de la basse, du plus grand au plus petit."""
    basse = min(notes, key=lambda x: x.hauteur)
    return sorted({(x.idx - basse.idx) % 7 + 1 for x in notes if x.lettre != basse.lettre},
                  reverse=True)


def degre_dans(ton, fondamentale):
    """Le degré de la fondamentale dans la tonalité ; l'accord doit en faire partie."""
    g = echelle(ton)
    d = (fondamentale.idx - g[0].idx) % 7
    assert g[d].alt == fondamentale.alt, (ton, fondamentale)
    return d + 1


def chiffre(ton, notes):
    """
    (chiffre romain, chiffrage) dans la tonalité. En position fondamentale, un
    accord de trois sons ne porte que son chiffre romain : I, IV, V.
    """
    a = analyser_accord(notes)
    romain = ROMAINS[degre_dans(ton, a.fondamentale) - 1]
    if a.sons == 3 and a.position == 0:
        return romain, ""
    return romain, a.chiffrage


# ---------------------------------------------------------------------------
# Les exemples
# ---------------------------------------------------------------------------
def n(txt):
    """« C5 », « F#4 » -> Note, octaves du modèle (4 : celle du do central)."""
    lettre, alt, octave = txt[0], txt[1:-1].count("#") - txt[1:-1].count("b"), int(txt[-1])
    return Note(lettre, alt, octave)


DO_MAJEUR = Ton(n("C4"), "majeur")
# La la mineur part du la grave, comme dans « Les gammes » : ses accords tiennent
# sur la portée en montant.
LA_MINEUR = Ton(n("A3"), "mineur")


def toutes_les_tonalites():
    """Les quinze tonalités majeures et les quinze mineures."""
    for _, majeur, mineur in TONALITES:
        yield Ton(note_de(majeur, 4), "majeur")
        yield Ton(note_de(mineur, 4), "mineur")


def septieme_de_dominante(ton):
    return sur_degre(ton, 5, 4)


def septieme_diminuee(ton):
    return sur_degre(ton, 7, 4)


# Sol, puis sa tierce, sa quinte et sa septième : la pile se construit.
def tierces_empilees():
    v7 = septieme_de_dominante(DO_MAJEUR)
    return [v7[:k] for k in range(1, 5)]


# Les quatre accords de trois sons, sur do.
def quatre_natures():
    do = n("C5")
    return [[do, au_dessus(do, 3, t), au_dessus(do, 5, q)]
            for t, q in (("majeure", "juste"), ("mineure", "juste"),
                         ("mineure", "diminuée"), ("majeure", "augmentée"))]


def accords_des_degres(ton):
    """Les accords des sept degrés, en montant dans la gamme."""
    return [sur_degre(ton, d) for d in range(1, 8)]


def renversements(notes, centrer=True):
    """
    Un accord dans chacune de ses positions. Centrés, les accords sont chacun
    ramenés au plus près de la portée ; sinon, la basse monte d'une position à
    l'autre.
    """
    return [placer(renverser(notes, p)) if centrer else renverser(notes, p)
            for p in range(len(notes))]


# Les septièmes diminuées de quatre tonalités mineures à une tierce mineure
# l'une de l'autre : un même son, quatre orthographes.
TONS_DIMINUEE = [Ton(n(x), "mineur") for x in ("A4", "C4", "Eb4", "F#4")]

# La septième de dominante et sa résolution, en do majeur : à la main droite,
# sol reste, si monte à do, fa descend à mi ; à la basse, sol monte à do. La
# quinte, ré, est omise : l'accord de tonique est complet.
RESOLUTION = {
    "droite": ([n("G4"), n("B4"), n("F5")], [n("G4"), n("C5"), n("E5")]),
    "basse": (n("G3"), n("C4")),
}

# Un accord écrit en désordre, puis rangé en tierces : ré, si, fa, sol devient
# sol, si, ré, fa.
ECRIT_EN_DESORDRE = [n("D4"), n("B4"), n("F5"), n("G5")]
EN_TIERCES = [n("G4"), n("B4"), n("D5"), n("F5")]

# L'exercice : (tonalité, degré, nombre de sons, position, position large).
Item = namedtuple("Item", "ton degre sons position large", defaults=(False,))
EXERCICE = [
    Item(Ton(n("G4"), "majeur"), 1, 3, 1),
    Item(Ton(n("D4"), "mineur"), 4, 3, 0),
    Item(Ton(n("F4"), "majeur"), 5, 4, 1),
    Item(Ton(n("A4"), "mineur"), 7, 4, 0),
    Item(Ton(n("Bb4"), "majeur"), 1, 3, 2),
    Item(Ton(n("E4"), "mineur"), 5, 4, 3, True),
    Item(Ton(n("C4"), "mineur"), 3, 3, 0),
    Item(Ton(n("D4"), "majeur"), 5, 4, 2, True),
    Item(Ton(n("Eb4"), "majeur"), 2, 3, 1),
    Item(Ton(n("B4"), "mineur"), 2, 3, 0),
]


# ---------------------------------------------------------------------------
# Les symboles anglo-saxons : la lettre de la fondamentale, puis la nature
# ---------------------------------------------------------------------------
SUFFIXES = {"accord parfait majeur": "", "accord parfait mineur": "m",
            "accord de quinte diminuée": "°", "accord de quinte augmentée": "+",
            "septième de dominante": "7", "septième diminuée": "°7",
            "septième de sensible": "m7b5"}
ALT_SYMBOLE = {-1: "b", 0: "", 1: "#"}


def lettre(note):
    return note.lettre + ALT_SYMBOLE[note.alt]


def symbole(notes):
    """« G7/B » : la fondamentale en lettre, la nature, et la basse si ce n'est pas elle."""
    a = analyser_accord(notes)
    basse = min(notes, key=lambda x: x.hauteur)
    s = lettre(a.fondamentale) + SUFFIXES[a.nature]
    return s if a.position == 0 else s + "/" + lettre(basse)


MATH_SYMBOLE = {"#": r"\sharp", "b": r"\flat", "°": r"^{\circ}"}


def tex_symbole(txt):
    """Le symbole en LaTeX : dièse, bémol et rond en exposant, dans un seul mode mathématique par suite."""
    res, math = [], []
    for c in txt + " ":
        if c in MATH_SYMBOLE:
            math.append(MATH_SYMBOLE[c])
            continue
        if math:
            res.append("$" + "".join(math) + "$")
            math = []
        res.append(c)
    return "".join(res).rstrip()


def verifier_symboles():
    """Les symboles que cite le texte."""
    assert [symbole(x) for x in quatre_natures()] == ["C", "Cm", "C°", "C+"]
    assert symbole(septieme_de_dominante(DO_MAJEUR)) == "G7"
    assert symbole(septieme_diminuee(LA_MINEUR)) == "G#°7"
    assert symbole(sur_degre(DO_MAJEUR, 7, 4)) == "Bm7b5"
    assert symbole(renverser(sur_degre(DO_MAJEUR, 1), 1)) == "C/E"
    # Les lettres : A pour la, B pour si, C pour do… G pour sol.
    assert [n(x + "4").nom_fr() for x in "ABCDEFG"] == ["la", "si", "do", "ré", "mi", "fa", "sol"]
    # Le symbole ne dépend pas de la tonalité : la–do–mi est Am en do majeur
    # (VI) comme en sol majeur (II).
    assert symbole(sur_degre(DO_MAJEUR, 6)) == symbole(sur_degre(Ton(n("G4"), "majeur"), 2)) == "Am"
    # L'accord parfait majeur dans le son : les harmoniques 4, 5 et 6 d'un do
    # grave tombent, à l'arrondi près, sur do, mi et sol.
    from math import log2
    assert [round(12 * log2(k)) % 12 for k in (4, 5, 6)] == [0, 4, 7]


def accord_exercice(item):
    notes = renverser(sur_degre(item.ton, item.degre, item.sons), item.position)
    return placer(ecarter(notes) if item.large else notes)


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def qualites_des_tierces(notes):
    """Les qualités des tierces successives d'une pile."""
    res = []
    for a, b in zip(notes, notes[1:]):
        numero, qualite = analyser(a, b)
        assert numero == 3, (a, b)
        res.append(qualite)
    return res


def demi_tons_entre(a, b):
    return b.hauteur - a.hauteur


def verifier():
    # Une lettre sur deux : sol, si, ré, fa.
    assert [x.nom_fr() for x in tierces_empilees()[-1]] == ["sol", "si", "ré", "fa"]

    # Les quatre accords de trois sons : leurs tierces empilées et leur nature.
    attendu = [("accord parfait majeur", ["majeure", "mineure"]),
               ("accord parfait mineur", ["mineure", "majeure"]),
               ("accord de quinte diminuée", ["mineure", "mineure"]),
               ("accord de quinte augmentée", ["majeure", "majeure"])]
    for notes, (nature, tierces) in zip(quatre_natures(), attendu):
        assert analyser_accord(notes).nature == nature
        assert qualites_des_tierces(notes) == tierces
    # Les deux accords parfaits ne diffèrent que par leur tierce.
    majeur, mineur = quatre_natures()[:2]
    assert majeur[0].hauteur == mineur[0].hauteur
    assert majeur[2].hauteur == mineur[2].hauteur and majeur[1].hauteur - mineur[1].hauteur == 1

    # Sur chaque degré, dans les quinze tonalités de chaque mode.
    schema = {"majeur": ["M", "m", "m", "M", "M", "m", "dim."],
              "mineur": ["m", "dim.", "aug.", "m", "M", "M", "dim."]}
    for ton in toutes_les_tonalites():
        natures = [ABREGES_NATURES[analyser_accord(sur_degre(ton, d)).nature]
                   for d in range(1, 8)]
        assert natures == schema[ton.mode], (nom_ton(ton), natures)
        # I, IV et V réunissent les sept notes de la gamme.
        notes = {(x.lettre, x.alt) for d in (1, 4, 5) for x in sur_degre(ton, d)}
        assert notes == {(x.lettre, x.alt) for x in echelle(ton)}

        # Accords de quatre sons : la structure de la septième de dominante
        # n'apparaît que sur V, celle de la septième diminuée que sur VII du
        # mineur ; en majeur, VII porte la septième de sensible.
        qualites = [analyser_accord(sur_degre(ton, d, 4)).qualites for d in range(1, 8)]
        assert [d + 1 for d, q in enumerate(qualites)
                if q == ("majeure", "juste", "mineure")] == [5]
        diminuees = [d + 1 for d, q in enumerate(qualites)
                     if q == ("mineure", "diminuée", "diminuée")]
        assert diminuees == ([7] if ton.mode == "mineur" else [])
        if ton.mode == "majeur":
            assert qualites[6] == ("mineure", "diminuée", "mineure")

        # La septième de dominante : 3ce M, 5te J, 7e m. La tonique est une
        # quinte juste sous sa fondamentale.
        v7 = septieme_de_dominante(ton)
        assert [abrege(*au_dessus_de(v7[0], x)) for x in v7[1:]] == ["3ce M", "5te J", "7e m"]
        assert analyser(ton.tonique, v7[0]) == (5, "juste")
        # Sa tierce est la sensible, à un demi-ton sous la tonique ; sa septième
        # est le quatrième degré, qui descend d'un degré sur la médiante.
        g = echelle(ton)
        assert (v7[1].lettre, v7[1].alt) == (g[6].lettre, g[6].alt)
        assert (octavier(ton.tonique, 1).hauteur - v7[1].hauteur) % 12 == 1
        assert (v7[3].lettre, v7[3].alt) == (g[3].lettre, g[3].alt)
        # La sensible et la septième forment un triton.
        assert analyser(v7[1], v7[3]) == (5, "diminuée")

        if ton.mode == "mineur":
            # La septième diminuée : trois tierces mineures, une septième
            # diminuée de neuf demi-tons, et une seconde augmentée de trois
            # demi-tons jusqu'à l'octave : quatre parts égales.
            vii7 = septieme_diminuee(ton)
            assert qualites_des_tierces(vii7) == ["mineure"] * 3
            assert au_dessus_de(vii7[0], vii7[3]) == (7, "diminuée")
            assert demi_tons_entre(vii7[0], vii7[3]) == 9
            assert analyser(vii7[3], octavier(vii7[0], 1)) == (2, "augmentée")
            assert demi_tons_entre(vii7[3], octavier(vii7[0], 1)) == 3

    # La septième de dominante est la même en majeur et en mineur, sur une
    # même tonique : mi, sol dièse, si, ré en la majeur comme en la mineur.
    majeurs = {note_de(m, 4).hauteur % 12: note_de(m, 4) for _, m, _ in TONALITES}
    for _, _, mineur in TONALITES:
        t = note_de(mineur, 4)
        if any((x.lettre, x.alt) == (t.lettre, t.alt) for x in majeurs.values()):
            a = septieme_de_dominante(Ton(t, "majeur"))
            b = septieme_de_dominante(Ton(t, "mineur"))
            assert [(x.lettre, x.alt) for x in a] == [(x.lettre, x.alt) for x in b]
    la_mineur = [x.nom_fr() for x in septieme_de_dominante(LA_MINEUR)]
    assert la_mineur == ["mi", "sol dièse", "si", "ré"]

    # La résolution, en do majeur : si monte d'un demi-ton à do, fa descend
    # d'un demi-ton à mi ; la quinte diminuée si–fa se resserre en tierce
    # majeure do–mi, la quarte augmentée fa–si s'ouvre en sixte mineure mi–do.
    si, fa, do, mi = n("B4"), n("F5"), n("C5"), n("E5")
    assert analyser(si, do) == (2, "mineure") and analyser(mi, fa) == (2, "mineure")
    assert analyser(si, fa) == (5, "diminuée") and analyser(do, mi) == (3, "majeure")
    assert analyser(n("F4"), si) == (4, "augmentée") and analyser(n("E4"), do) == (6, "mineure")
    # En la mineur, la septième, ré, descend d'un ton sur la médiante, do.
    assert analyser(n("C5"), n("D5")) == (2, "majeure")
    (avant, apres), (b1, b2) = RESOLUTION["droite"], RESOLUTION["basse"]
    v = analyser_accord([b1] + avant)
    i = analyser_accord([b2] + apres)
    assert v.nature == "septième de dominante" and v.position == 0
    assert i.nature == "accord parfait majeur" and i.position == 0
    assert i.fondamentale.nom_fr() == "do" and i.sons == 3 and len(i.membres) == 3
    assert v.sons == 4 and len(v.membres) == 3
    assert v.qualites == ("majeure", None, "mineure")

    # La septième diminuée : un même son pour quatre tonalités, à une tierce
    # mineure l'une de l'autre ; trois septièmes diminuées en tout à l'oreille.
    sons = [sorted(x.hauteur % 12 for x in septieme_diminuee(t)) for t in TONS_DIMINUEE]
    assert all(s == sons[0] for s in sons)
    for a, b in zip(TONS_DIMINUEE, TONS_DIMINUEE[1:]):
        assert demi_tons_entre(a.tonique, b.tonique) % 12 == 3
    distincts = {tuple(sorted(x.hauteur % 12 for x in septieme_diminuee(t)))
                 for t in toutes_les_tonalites() if t.mode == "mineur"}
    assert len(distincts) == 3
    # Renversée, elle sonne comme une autre en position fondamentale : si, ré,
    # fa, sol dièse s'entend comme si, ré, fa, la bémol, celle de do mineur.
    la = renverser(septieme_diminuee(LA_MINEUR), 1)
    do_m = septieme_diminuee(Ton(n("C4"), "mineur"))
    assert [x.nom_fr() for x in do_m] == ["si", "ré", "fa", "la bémol"]
    assert (la[0].hauteur - do_m[0].hauteur) % 12 == 0
    assert [x.hauteur - la[0].hauteur for x in la] == [x.hauteur - do_m[0].hauteur for x in do_m]

    # Chaque renversement, dans chaque tonalité : l'analyse retrouve ce que la
    # construction a fait, et le chiffrage complet est celui du texte.
    complets = {3: [[5, 3], [6, 3], [6, 4]], 4: [[7, 5, 3], [6, 5, 3], [6, 4, 3], [6, 4, 2]]}
    for ton in toutes_les_tonalites():
        for d in range(1, 8):
            for sons in (3, 4):
                pile = sur_degre(ton, d, sons)
                for p in range(sons):
                    for disposition in (renverser(pile, p), ecarter(renverser(pile, p))):
                        a = analyser_accord(disposition)
                        assert (a.fondamentale.lettre, a.fondamentale.alt) == \
                            (pile[0].lettre, pile[0].alt)
                        assert a.position == p and degre_dans(ton, a.fondamentale) == d
                        assert chiffrage_complet(disposition) == complets[sons][p]
    # Le chiffrage abrégé : on omet la tierce de l'accord de trois sons ; celui
    # de l'accord de quatre sons ne garde que la fondamentale et la septième.
    for p, complet in enumerate(complets[3]):
        assert "/".join(str(c) for c in complet if c != 3) == CHIFFRAGES[3][p]
    v7 = septieme_de_dominante(DO_MAJEUR)
    for p in range(4):
        disposition = renverser(v7, p)
        basse = disposition[0]
        garde = [(x.idx - basse.idx) % 7 + 1 for x in (v7[0], v7[3]) if x.lettre != basse.lettre]
        assert "/".join(str(c) for c in garde) == CHIFFRAGES[4][p]

    # Le premier exemple de reconnaissance : ré, si, fa, sol est V4/3 en do majeur.
    a = analyser_accord(ECRIT_EN_DESORDRE)
    assert a.fondamentale.nom_fr() == "sol" and a.nature == "septième de dominante"
    assert a.position == 2 and chiffre(DO_MAJEUR, ECRIT_EN_DESORDRE) == ("V", "4/3")

    # L'exercice : chaque accord, analysé, redonne sa construction.
    for item in EXERCICE:
        notes = accord_exercice(item)
        a = analyser_accord(notes)
        assert a.position == item.position and a.sons == item.sons
        assert degre_dans(item.ton, a.fondamentale) == item.degre
        assert a.nature is not None
    natures = {analyser_accord(accord_exercice(i)).nature for i in EXERCICE}
    assert len(natures) >= 5


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def ly_accord(notes, duree="1"):
    return "<" + " ".join(x.lily() for x in notes) + ">" + duree


def chiffre_markup(romain, chiffrage):
    """Un chiffre romain suivi de son chiffrage, les chiffres empilés."""
    chiffres = chiffrage.split("/") if chiffrage else []
    if not chiffres:
        return r'\markup "%s"' % romain
    pile = " ".join('"%s"' % c for c in chiffres)
    hauteur = 1.15 if len(chiffres) == 1 else 0.55
    return (r'\markup \concat { "%s" \hspace #0.15 \raise #%.2f \fontsize #-3.5 '
            r"\override #'(baseline-skip . 1.3) \column { %s } }" % (romain, hauteur, pile))


def figures_markup(chiffrage):
    """Le chiffrage seul, ses chiffres empilés : 5, 6, 6 sur 4."""
    pile = " ".join('"%s"' % c for c in chiffrage.split("/"))
    return r"\markup \fontsize #-1 \override #'(baseline-skip . 1.7) \center-column { %s }" % pile


def syllabe(texte):
    """Une étiquette de paroles : un markup tel quel, sinon un texte entre guillemets."""
    return texte if texte.startswith("\\markup") else '"%s"' % texte


def portee_accords(accords, rangees, dessus=None, barres=False, coupure=None,
                   espacement=2.4):
    """
    Des accords en rondes, sur une portée en clé de sol sans armure, chacun
    légendé en dessous : une rangée de paroles par ligne de légendes. `dessus` :
    un texte au-dessus de chaque accord (les numéros de l'exercice).
    """
    corps = []
    for i, a in enumerate(accords):
        txt = ly_accord(a)
        if dessus:
            txt += r'^\markup \small "%s"' % dessus[i]
        corps.append(txt)
        if i < len(accords) - 1:
            if coupure and i == coupure - 1:
                corps.append(r'\bar "|" \break' if barres else r'\bar "" \break')
            elif barres:
                corps.append(r'\bar "|"')
    paroles = "\n".join(r"    \addlyrics { %s }" % " ".join(syllabe(t) for t in r)
                        for r in rangees)
    return r"""\score {
  <<
    \new Staff {
      \accidentalStyle forget
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      %s
      \bar "|."
    }
%s
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #%.1f
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
""" % (" ".join(corps), paroles, espacement)


def noms(notes):
    return " ".join(x.nom_fr() for x in notes)


def figure_tierces():
    piles = tierces_empilees()
    return portee_accords(piles, [["sol", "+ si", "+ ré", "+ fa"],
                                  [MEMBRES[k] for k in range(4)]])


def figure_natures():
    return portee_accords(quatre_natures(),
                          [["parfait majeur", "parfait mineur", "quinte diminuée",
                            "quinte augmentée"]], espacement=3.2)


def figure_degres(ton):
    accords = accords_des_degres(ton)
    return portee_accords(accords, [[chiffre_markup(r, "") for r in ROMAINS],
                                    [ABREGES_NATURES[analyser_accord(a).nature]
                                     for a in accords]])


def figure_renversements():
    accords = renversements(sur_degre(DO_MAJEUR, 1), centrer=False)
    return portee_accords(accords, [["position fondamentale", "1er renversement",
                                     "2e renversement"],
                                    [figures_markup(c) for c in CHIFFRAGES[3]]],
                          espacement=3.4)


def figure_septieme():
    accords = renversements(septieme_de_dominante(DO_MAJEUR))
    return portee_accords(accords, [[chiffre_markup(*chiffre(DO_MAJEUR, a)) for a in accords],
                                    ["basse : " + a[0].nom_fr() for a in accords]],
                          espacement=3.0)


def figure_resolution():
    (avant, apres), (b1, b2) = RESOLUTION["droite"], RESOLUTION["basse"]
    v = chiffre(DO_MAJEUR, [b1] + avant)
    i = chiffre(DO_MAJEUR, [b2] + apres)
    return r"""\score {
  \new PianoStaff <<
    \new Staff {
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      %s %s
      \bar "|."
    }
    \new Staff {
      \clef bass \key c \major \omit Staff.TimeSignature \cadenzaOn
      %s1 %s1
      \bar "|."
    }
    \addlyrics { %s %s }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #3.4
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
""" % (ly_accord(avant), ly_accord(apres), b1.lily(), b2.lily(),
       chiffre_markup(*v), chiffre_markup(*i))


def figure_diminuee():
    accords = [placer(septieme_diminuee(t)) for t in TONS_DIMINUEE]
    return portee_accords(accords, [[nom_ton(t) for t in TONS_DIMINUEE]], espacement=3.2)


def figure_reconnaitre():
    a = analyser_accord(ECRIT_EN_DESORDRE)
    return portee_accords([ECRIT_EN_DESORDRE, EN_TIERCES],
                          [["écrit", "en tierces"],
                           ["basse : " + ECRIT_EN_DESORDRE[0].nom_fr(),
                            "fondamentale : " + a.fondamentale.nom_fr()]],
                          barres=True, espacement=4.0)


def figure_exercice(debut, fin):
    """
    Une ligne de l'exercice. Les deux lignes sont deux gravures : rognées par
    LilyPond, deux lignes d'une même gravure seraient collées l'une à l'autre.
    """
    items = EXERCICE[debut:fin]
    return portee_accords([accord_exercice(i) for i in items], [[nom_ton(i.ton) for i in items]],
                          dessus=[str(k) for k in range(debut + 1, fin + 1)],
                          barres=True, espacement=2.6)


FIGURES = {
    "a-tierces": figure_tierces,
    "a-natures": figure_natures,
    "a-degres-majeur": lambda: figure_degres(DO_MAJEUR),
    "a-degres-mineur": lambda: figure_degres(LA_MINEUR),
    "a-renversements": figure_renversements,
    "a-septieme": figure_septieme,
    "a-resolution": figure_resolution,
    "a-diminuee": figure_diminuee,
    "a-reconnaitre": figure_reconnaitre,
    "a-exercice-1": lambda: figure_exercice(0, 5),
    "a-exercice-2": lambda: figure_exercice(5, 10),
}


def ecrire_gravures():
    return [ecrire(nom, fabrique(), preambule=PREAMBULE_ACCORDS)
            for nom, fabrique in FIGURES.items()]


# ---------------------------------------------------------------------------
# Tableaux et réponses
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_accords.py — ne pas modifier à la main.\n"


def tex_chiffre(romain, chiffrage):
    """\\ch{V}{6}{5} : le chiffre romain et ses chiffres empilés."""
    c = chiffrage.split("/") if chiffrage else []
    return r"\ch{%s}{%s}{%s}" % (romain, c[0] if c else "", c[1] if len(c) > 1 else "")


def tex_pile(chiffres):
    return r"\fig{%s}" % r"\\".join(str(c) for c in chiffres)


def ecrire_tex(nom, lignes):
    chemin = os.path.join(DIR_LY, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + "\n".join(lignes) + "\n")
    return chemin


def table_natures():
    # Six colonnes : on resserre les intervalles entre elles pour tenir dans la ligne.
    l = [r"\setlength{\tabcolsep}{4pt}%", r"\begin{tabular}{@{}l l l l l l@{}}", r"\toprule",
         r"\textbf{Accord} & \textbf{Tierce} & \textbf{Quinte} & "
         r"\textbf{Tierces empilées} & \textbf{Sur do} & \textbf{Symbole} \\", r"\midrule"]
    for notes in quatre_natures():
        a = analyser_accord(notes)
        t, q = (abrege(*au_dessus_de(notes[0], x)) for x in notes[1:])
        empilees = " + ".join(abrege(*analyser(x, y)) for x, y in zip(notes, notes[1:]))
        l.append(f"{COURTES[a.nature]} & {t} & {q} & {empilees} & "
                 f"{' -- '.join(x.nom_fr() for x in notes)} & {tex_symbole(symbole(notes))} \\\\")
    l += [r"\bottomrule", r"\end{tabular}"]
    return ecrire_tex("accords-natures.tex", l)


def table_chiffrages(nom, pile, entete_exemple):
    l = [r"\begin{tabular}{@{}l l c c l@{}}", r"\toprule",
         r"\textbf{Position} & \textbf{À la basse} & \textbf{Complet} & "
         r"\textbf{Abrégé} & \textbf{%s} \\" % entete_exemple, r"\midrule"]
    for p in range(len(pile)):
        notes = renverser(pile, p)
        a = analyser_accord(notes)
        l.append(f"{POSITIONS[p]} & {MEMBRES[p]} & {tex_pile(chiffrage_complet(notes))} & "
                 f"{tex_pile(a.chiffrage.split('/'))} & {noms(notes)} \\\\[7pt]")
    l += [r"\bottomrule", r"\end{tabular}"]
    return ecrire_tex(nom, l)


def reponses_exercice():
    res = []
    for item in EXERCICE:
        notes = accord_exercice(item)
        a = analyser_accord(notes)
        res.append((chiffre(item.ton, notes), a.fondamentale.nom_fr(), a.nature,
                    POSITIONS[a.position]))
    return res


def ecrire_reponses():
    l = [r"\begin{enumerate}[leftmargin=*, itemsep=1pt]"]
    for ((romain, chiff), fond, nature, position), item in zip(reponses_exercice(), EXERCICE):
        sym = tex_symbole(symbole(accord_exercice(item)))
        l.append(rf"  \item {tex_chiffre(romain, chiff)}~: fondamentale {fond}, "
                 rf"{nature}, {position}~; {sym}.")
    l.append(r"\end{enumerate}")
    return ecrire_tex("accords-reponses.tex", l)


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
def entree(libelle, accords, mode="major"):
    """Une entrée : chaque accord en ronde, une mesure chacun."""
    return (libelle, 0, mode, (4, 4), [[[(a, RONDE, False)]] for a in accords])


def ecrire_musicxml():
    (avant, apres), (b1, b2) = RESOLUTION["droite"], RESOLUTION["basse"]
    entrees = [
        entree("sol, puis sa tierce, sa quinte, sa septième", tierces_empilees()),
        entree("les quatre accords de trois sons, sur do", quatre_natures()),
        entree("un accord sur chaque degré de do majeur", accords_des_degres(DO_MAJEUR)),
        entree("un accord sur chaque degré de la mineur harmonique",
               accords_des_degres(LA_MINEUR), "minor"),
        entree("l'accord de do majeur et ses renversements",
               renversements(sur_degre(DO_MAJEUR, 1), centrer=False)),
        entree("la septième de dominante de do majeur et ses renversements",
               renversements(septieme_de_dominante(DO_MAJEUR))),
        entree("la septième de dominante résolue sur la tonique",
               [[b1] + avant, [b2] + apres]),
        entree("septièmes diminuées de la, do, mi bémol et fa dièse mineur",
               [placer(septieme_diminuee(t)) for t in TONS_DIMINUEE], "minor"),
        entree("un accord écrit, puis rangé en tierces",
               [ECRIT_EN_DESORDRE, EN_TIERCES]),
        entree("l'exercice", [accord_exercice(i) for i in EXERCICE]),
    ]
    chemin = os.path.join(RACINE, "accords.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_rythmee(
            "Les accords",
            f"Les accords des gravures du guide, une ronde chacun, à la noire {TEMPO}.",
            entrees, "Piano", TEMPO))
    return chemin


if __name__ == "__main__":
    verifier()
    verifier_symboles()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, RACINE))
    for c in (table_natures(),
              table_chiffrages("accords-chiffrages-3.tex", sur_degre(DO_MAJEUR, 1),
                               "Sur do"),
              table_chiffrages("accords-chiffrages-4.tex", septieme_de_dominante(DO_MAJEUR),
                               "En do majeur"),
              ecrire_reponses()):
        print("LaTeX :", os.path.relpath(c, RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
