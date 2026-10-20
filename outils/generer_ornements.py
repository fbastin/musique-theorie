#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, les réponses de l'exercice et le fichier MusicXML du
guide « Les ornements ».

    python3 outils/generer_ornements.py

Comme pour les mordants, un ornement y est une règle : d'une note écrite, de
sa valeur, de ses petites notes et de l'armure, elle tire les notes jouées.
L'appogiature prend la moitié de la note, les deux tiers d'une note pointée,
toute la note devant un silence ; l'appogiature brève, une triple croche ; le
trille alterne jusqu'au bout de la valeur ; le trémolo répète une note, ou en
alterne deux, à la valeur que donnent ses barres ; le gruppetto tourne autour
de la note. Les portées « joué » des gravures, les réponses de l'exercice et le
fichier MusicXML en dérivent, et les affirmations du texte sont vérifiées avant
toute écriture.
"""

import os
import sys
from collections import namedtuple
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generer import DIR_LY, PREAMBULE, RACINE, ecrire
from generer_mordants import (ALT_MARKUP, TEMPO, TRIPLE_CROCHE, cle_armure,
                              lily_duree, n, nom_portee, taille, trille, voisine)
from generer_mordants import realiser as realiser_mordant
from intervalles import analyser
import musicxml

PREAMBULE_ORNEMENTS = PREAMBULE.replace("outils/generer.py", "outils/generer_ornements.py")

DOUBLE_CROCHE = Fraction(1, 16)
NOIRE = Fraction(1, 4)
N = Fraction

# ---------------------------------------------------------------------------
# Modèle : de l'écrit au joué
# ---------------------------------------------------------------------------
# Une note écrite : hauteur (None pour un silence), valeur en fraction de
# ronde, ornement, petites notes écrites (l'appogiature, la terminaison d'un
# trille, les notes d'une fioriture, la seconde note d'un trémolo), altérations
# écrites près du signe pour la voisine du dessus et celle du dessous, texte
# sous la note, nombre de barres d'un trémolo.
Ecrite = namedtuple("Ecrite", "note valeur orn petites alt_haut alt_bas sous barres",
                    defaults=(None, (), None, None, None, None))
# Un exemple : chiffrage, mesures — chacune une armure et des notes écrites —,
# lectures : (titre de la portée jouée, options). La seule option est la note
# de départ du trille, « voisine » (XVIIIe siècle) ou « note » (XIXe).
Exemple = namedtuple("Exemple", "temps mesures lectures",
                     defaults=((("joué", {}),),))

NOMS = {"appogiature": "appogiature", "acciaccatura": "appogiature brève",
        "mordant": "mordant inférieur", "trille": "trille", "gruppetto": "gruppetto",
        "trémolo": "trémolo", "trémolo à deux notes": "trémolo à deux notes",
        "gruppetto après": "gruppetto après la note",
        "gruppetto renversé": "gruppetto renversé", "fioriture": "fioriture"}


def pointee(valeur):
    """Une valeur pointée vaut trois fois une valeur simple : 3/4, 3/8, 3/16."""
    return valeur.numerator == 3


def part_appogiature(valeur):
    """La moitié d'une valeur simple, les deux tiers d'une valeur pointée."""
    return valeur * 2 / 3 if pointee(valeur) else valeur / 2


def voisines(e, armure):
    """Les voisines du dessus et du dessous, prises dans la gamme sauf altération écrite."""
    return (voisine(e.note, 1, armure, e.alt_haut),
            voisine(e.note, -1, armure, e.alt_bas))


def unite_tremolo(barres):
    """La valeur des notes d'un trémolo : une barre, des croches ; deux, des doubles croches…"""
    return Fraction(1, 2 ** (barres + 2))


def jouer(e, armure, options):
    """Les notes jouées pour une note écrite : liste de (note, valeur, liée)."""
    if e.note is None or e.orn is None:
        return [(e.note, e.valeur, False)]
    v = e.valeur
    if e.orn == "appogiature":
        part = part_appogiature(v)
        return [(e.petites[0], part, False), (e.note, v - part, False)]
    if e.orn == "acciaccatura":
        return [(e.petites[0], TRIPLE_CROCHE, False), (e.note, v - TRIPLE_CROCHE, False)]
    if e.orn == "mordant":
        return realiser_mordant(e.note, v, "mordant inférieur", armure, e.alt_bas)
    if e.orn in ("trémolo", "trémolo à deux notes"):
        # La note écrite donne la durée de tout le trémolo, les barres la valeur
        # des notes répétées ; à deux notes, elles alternent.
        unite = unite_tremolo(e.barres)
        autre = e.petites[0] if e.petites else e.note
        return [(e.note if i % 2 == 0 else autre, unite, False) for i in range(int(v / unite))]
    haut, bas = voisines(e, armure)
    if e.orn == "trille":
        return trille(e.note, v, haut, bas, options.get("trille", "voisine"), bool(e.petites))
    if e.orn in ("gruppetto", "gruppetto renversé"):
        tour = [haut, e.note, bas] if e.orn == "gruppetto" else [bas, e.note, haut]
        return [(x, DOUBLE_CROCHE, False) for x in tour] + [(e.note, v - 3 * DOUBLE_CROCHE, False)]
    if e.orn == "gruppetto après":
        # La note d'abord, la moitié de sa valeur ; le tour dans l'autre moitié.
        return [(e.note, v / 2, False)] + [(x, v / 8, False) for x in (haut, e.note, bas, e.note)]
    if e.orn == "fioriture":
        # Les petites notes prennent leur temps à la fin de la note qu'elles suivent.
        reste = v - len(e.petites) * TRIPLE_CROCHE
        assert reste > 0, e
        return [(e.note, reste, False)] + [(x, TRIPLE_CROCHE, False) for x in e.petites]
    raise ValueError(e.orn)


def jouer_mesure(notes, armure, options):
    """
    Les notes jouées d'une mesure, note écrite par note écrite : liste de
    (indices des notes écrites, notes jouées). Une appogiature suivie d'un
    silence prend toute la note ; la note principale tombe à la place du silence.
    """
    res, i = [], 0
    while i < len(notes):
        e = notes[i]
        if e.orn == "appogiature" and i + 1 < len(notes) and notes[i + 1].note is None:
            res.append(((i, i + 1), [(e.petites[0], e.valeur, False),
                                     (e.note, notes[i + 1].valeur, False)]))
            i += 2
        else:
            res.append(((i,), jouer(e, armure, options)))
            i += 1
    return res


# ---------------------------------------------------------------------------
# Les exemples
# ---------------------------------------------------------------------------
def e(txt, valeur, orn=None, petites=(), alt_haut=None, alt_bas=None, sous=None, barres=None):
    return Ecrite(n(txt) if txt else None, valeur, orn,
                  tuple(n(x) for x in petites), alt_haut, alt_bas, sous, barres)


EPOQUES = (("XVIIIe s.", {"trille": "voisine"}), ("XIXe s.", {"trille": "note"}))

EXEMPLES = {
    # Les quatre ornements les plus courants sur une même note.
    "o-apercu": Exemple((4, 4), [(0, [
        e("C5", N(1, 4), "appogiature", ["D5"], sous="appogiature"),
        e("C5", N(1, 4), "mordant", sous="mordant"),
        e("C5", N(1, 4), "trille", sous="trille"),
        e("C5", N(1, 4), "gruppetto", sous="gruppetto")])]),
    # La moitié : d'une blanche, d'une noire, d'une croche ; d'en haut ou d'en bas.
    "o-appogiature": Exemple((2, 4), [
        (0, [e("C5", N(1, 2), "appogiature", ["D5"])]),
        (0, [e("C5", N(1, 4), "appogiature", ["B4"]), e("D5", N(1, 4))]),
        (0, [e("E5", N(1, 8), "appogiature", ["F5"]), e("D5", N(1, 8), "appogiature", ["E5"]),
             e("C5", N(1, 4))])]),
    # Les deux tiers d'une note pointée ; toute la note devant un silence.
    "o-appog-longues": Exemple((3, 4), [
        (0, [e("C5", N(3, 4), "appogiature", ["D5"])]),
        (0, [e("C5", N(3, 8), "appogiature", ["D5"]), e("B4", N(1, 8)), e("C5", N(1, 4))]),
        (0, [e("C5", N(1, 4), "appogiature", ["D5"]), e(None, N(1, 4)), e(None, N(1, 4))])]),
    # La même petite note, longue puis brève ; brève, elle ne dépend pas de la valeur.
    "o-acciaccatura": Exemple((2, 4), [
        (0, [e("C5", N(1, 4), "appogiature", ["D5"]), e("C5", N(1, 4), "acciaccatura", ["D5"])]),
        (0, [e("C5", N(1, 2), "acciaccatura", ["D5"])])]),
    # Le trille de cadence, sur la sensible : long, avec l'ondulée et la
    # terminaison ; bref, lu à deux époques.
    "o-trille": Exemple((2, 4), [(0, [e("B4", N(1, 2), "trille", ["A4", "B4"])]),
                                 (0, [e("C5", N(1, 2))])]),
    "o-trille-epoques": Exemple((2, 4), [(0, [e("B4", N(1, 4), "trille"), e("C5", N(1, 4))])],
                                EPOQUES),
    # Une blanche à une barre, puis à deux ; une blanche partagée entre do et mi.
    "o-tremolo": Exemple((2, 4), [
        (0, [e("C5", N(1, 2), "trémolo", barres=1, sous="une barre")]),
        (0, [e("C5", N(1, 2), "trémolo", barres=2, sous="deux barres")]),
        (0, [e("C5", N(1, 2), "trémolo à deux notes", ["E5"], barres=2, sous="deux notes")])]),
    "o-gruppetto": Exemple((2, 4), [
        (0, [e("C5", N(1, 4), "gruppetto", sous="sur la note"), e("B4", N(1, 4))]),
        (0, [e("C5", N(1, 4), "gruppetto après", sous="après la note"), e("D5", N(1, 4))]),
        (0, [e("C5", N(1, 4), "gruppetto renversé", sous="renversé"), e("B4", N(1, 4))])]),
    # La voisine du dessous de sol : fa par la gamme de do, fa dièse par le dièse écrit.
    "o-gruppetto-alt": Exemple((2, 4), [(0, [e("G4", N(1, 4), "gruppetto"),
                                             e("G4", N(1, 4), "gruppetto", alt_bas=1)])]),
    "o-fioriture": Exemple((4, 4), [(0, [
        e("E5", N(1, 2), "fioriture", ["F5", "G5", "A5", "G5", "F5", "E5", "D5", "E5"]),
        e("F5", N(1, 2))])]),
}

# L'exercice : une mélodie en fa majeur, à trois temps, ses ornements numérotés.
EXERCICE = Exemple((3, 4), [
    (-1, [e("C5", N(3, 4), "appogiature", ["D5"])]),
    (-1, [e("A4", N(1, 2), "gruppetto après"), e("Bb4", N(1, 4), "mordant")]),
    (-1, [e("G4", N(1, 4), "acciaccatura", ["A4"]), e("C5", N(1, 4), "gruppetto"),
          e("F5", N(1, 4), "appogiature", ["G5"])]),
    (-1, [e("E5", N(1, 2), "trille", ["D5", "E5"]), e("F5", N(1, 4))]),
])


def ecrivable(valeur):
    """Une valeur qui s'écrit d'une seule note, pointée au plus deux fois."""
    try:
        lily_duree(valeur)
        return True
    except ValueError:
        return False


def lier(jouees):
    """
    Les notes jouées d'une mesure, prêtes à graver : une durée qui ne s'écrit
    pas d'une seule note — la blanche moins une triple croche — est coupée au
    temps suivant, et ses morceaux liés.
    """
    res, pos = [], Fraction(0)
    for note, v, liee in jouees:
        while not ecrivable(v):
            coupe = (pos // NOIRE + 1) * NOIRE - pos
            assert 0 < coupe < v and ecrivable(coupe), (note, v)
            res.append((note, coupe, note is not None))
            pos, v = pos + coupe, v - coupe
        res.append((note, v, liee))
        pos += v
    return res


def mesures_jouees(exemple, options):
    """Pour chaque mesure : son armure et ses notes jouées, à plat, prêtes à graver."""
    return [(a, lier([j for _, jouees in jouer_mesure(notes, a, options) for j in jouees]))
            for a, notes in exemple.mesures]


def ornees(exemple, options):
    """Les notes ornées, dans l'ordre : (note écrite, armure, notes jouées)."""
    res = []
    for a, notes in exemple.mesures:
        for indices, jouees in jouer_mesure(notes, a, options):
            if notes[indices[0]].orn:
                res.append((notes[indices[0]], a, jouees))
    return res


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def noms(jouees):
    return [x.nom_fr() for x, _, _ in jouees]


def verifier():
    tous = list(EXEMPLES.values()) + [EXERCICE]
    # Chaque mesure écrite est complète, et chaque mesure jouée aussi : un
    # ornement prend son temps sur la note qu'il orne, jamais au-delà.
    for exemple in tous:
        for _, notes in exemple.mesures:
            assert sum(x.valeur for x in notes) == Fraction(*exemple.temps)
        for _, options in exemple.lectures:
            for (a, notes), (_, jouees) in zip(exemple.mesures, mesures_jouees(exemple, options)):
                assert sum(v for _, v, _ in jouees) == Fraction(*exemple.temps)
            # Chaque ornement commence sur le temps de sa note et remplit sa valeur,
            # sauf l'appogiature devant un silence, qui prend aussi le silence.
            for x, a, jouees in ornees(exemple, options):
                total = sum(v for _, v, _ in jouees)
                assert total == x.valeur or (x.orn == "appogiature" and total > x.valeur)

    # L'appogiature est une seconde au-dessus ou au-dessous de la note.
    for exemple in tous:
        for _, notes in exemple.mesures:
            for x in notes:
                if x.orn in ("appogiature", "acciaccatura"):
                    grave, aigu = sorted((x.note, x.petites[0]), key=lambda k: k.hauteur)
                    assert analyser(grave, aigu)[0] == 2, x

    do = n("C5")
    # La moitié d'une blanche, d'une noire, d'une croche ; les deux tiers d'une
    # blanche pointée (une blanche) et d'une noire pointée (une noire).
    for v, part in ((N(1, 2), N(1, 4)), (N(1, 4), N(1, 8)), (N(1, 8), N(1, 16)),
                    (N(3, 4), N(1, 2)), (N(3, 8), N(1, 4))):
        assert jouer(Ecrite(do, v, "appogiature", (n("D5"),)), 0, {})[0][1] == part
    # Devant un silence, toute la valeur ; la note principale prend la place du silence.
    indices, devant_silence = jouer_mesure(EXEMPLES["o-appog-longues"].mesures[2][1], 0, {})[0]
    assert indices == (0, 1)
    assert [(x.nom_fr(), v) for x, v, _ in devant_silence] == [("ré", N(1, 4)), ("do", N(1, 4))]

    # L'appogiature brève : une triple croche, quelle que soit la valeur.
    for v in (N(1, 2), N(1, 4), N(1, 8)):
        assert jouer(Ecrite(do, v, "acciaccatura", (n("D5"),)), 0, {})[0][1] == TRIPLE_CROCHE
    # À la noire 80, une triple croche dure un peu moins d'un dixième de seconde.
    assert 0.09 < 60 / TEMPO / 8 < 0.1

    # Le trille : sur une noire, huit triples croches ; commencé sur la voisine,
    # il finit sur la note ; commencé sur la note aussi. La terminaison descend
    # à la voisine du dessous avant de revenir.
    si = n("B4")
    trille_18 = jouer(Ecrite(si, N(1, 4), "trille"), 0, {"trille": "voisine"})
    trille_19 = jouer(Ecrite(si, N(1, 4), "trille"), 0, {"trille": "note"})
    assert noms(trille_18) == ["do", "si"] * 4
    assert noms(trille_19) == ["si", "do"] * 3 + ["si"]
    termine = jouer(Ecrite(si, N(1, 2), "trille", (n("A4"), si)), 0, {})
    assert len(termine) == 16 and noms(termine)[-3:] == ["si", "la", "si"]
    for t in (trille_18, trille_19, termine):
        assert t[-1][0] is si
    # La voisine du dessus de si est à un demi-ton : do.
    assert taille(si, voisine(si, 1, 0)) == "demi-ton"

    # Le gruppetto : ré do si do sur la note ; si do ré do renversé ; après la
    # note, do tenu la moitié de sa valeur. Il est le même que dans le guide des
    # mordants.
    g = jouer(Ecrite(do, N(1, 4), "gruppetto"), 0, {})
    assert noms(g) == ["ré", "do", "si", "do"]
    assert [(repr(x), v) for x, v, _ in g] == \
        [(repr(x), v) for x, v, _ in realiser_mordant(do, N(1, 4), "gruppetto", 0)]
    assert noms(jouer(Ecrite(do, N(1, 4), "gruppetto renversé"), 0, {})) == ["si", "do", "ré", "do"]
    apres = jouer(Ecrite(do, N(1, 4), "gruppetto après"), 0, {})
    assert noms(apres) == ["do", "ré", "do", "si", "do"] and apres[0][1] == N(1, 8)
    # Une altération sous le signe change la voisine du dessous : fa dièse sous sol.
    sol = n("G4")
    assert noms(jouer(Ecrite(sol, N(1, 4), "gruppetto"), 0, {})) == ["la", "sol", "fa", "sol"]
    assert noms(jouer(Ecrite(sol, N(1, 4), "gruppetto", alt_bas=1), 0, {})) == \
        ["la", "sol", "fa dièse", "sol"]

    # Le trémolo : une barre sur une blanche, quatre croches ; deux barres, huit
    # doubles croches ; à deux notes, une blanche partagée en huit doubles
    # croches qui alternent do et mi, plus éloignés qu'un ton.
    t1, t2, t3 = [jouer(notes[0], 0, {}) for _, notes in EXEMPLES["o-tremolo"].mesures]
    assert [(x.nom_fr(), v) for x, v, _ in t1] == [("do", N(1, 8))] * 4
    assert [(x.nom_fr(), v) for x, v, _ in t2] == [("do", N(1, 16))] * 8
    assert noms(t3) == ["do", "mi"] * 4 and all(v == N(1, 16) for _, v, _ in t3)
    assert analyser(n("C5"), n("E5"))[0] > 2

    # La fioriture prend son temps à la fin de la note qui la précède ; la note
    # suivante tombe à sa place.
    _, jouees = mesures_jouees(EXEMPLES["o-fioriture"], {})[0]
    assert jouees[0][1] == NOIRE and sum(v for _, v, _ in jouees[:-1]) == N(1, 2)
    assert (jouees[-1][0].nom_fr(), jouees[-1][1]) == ("fa", N(1, 2))

    # L'exercice : l'armure donne si bémol sous do et au-dessus de la ; les
    # deux tiers de la blanche pointée ; la voisine du trille de mi est fa.
    rep = reponses_exercice()
    assert rep[0] == ("appogiature", [("ré", N(1, 2)), ("do", N(1, 4))])
    assert [x for x, _ in rep[1][1]] == ["la", "si bémol", "la", "sol", "la"]
    assert [x for x, _ in rep[2][1]] == ["si bémol", "la", "si bémol"]
    assert [x for x, _ in rep[4][1]] == ["ré", "do", "si bémol", "do"]
    assert [x for x, _ in rep[6][1]] == ["fa", "mi"] * 7 + ["ré", "mi"]


def reponses_exercice():
    """Pour chaque ornement de l'exercice : son nom et les notes jouées, avec leurs valeurs."""
    _, options = EXERCICE.lectures[0]
    res = []
    for x, a, jouees in ornees(EXERCICE, options):
        nom = NOMS[x.orn] + (" avec terminaison" if x.orn == "trille" and x.petites else "")
        res.append((nom, [(k.nom_fr(), v) for k, v, _ in jouees]))
    return res


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def signe(glyphe, alt_haut=None, alt_bas=None):
    """Le signe, et les altérations qui l'accompagnent au-dessus ou au-dessous."""
    if alt_haut is None and alt_bas is None:
        return "\\" + glyphe
    pile = ([rf"\teeny {ALT_MARKUP[alt_haut]}"] if alt_haut is not None else []) \
        + [rf'\musicglyph "scripts.{glyphe}"'] \
        + ([rf"\teeny {ALT_MARKUP[alt_bas]}"] if alt_bas is not None else [])
    return (r"-\tweak self-alignment-X #CENTER ^\markup \override #'(baseline-skip . 1.9) "
            r"\center-column { %s }" % " ".join(pile))


def lily_ecrite(notes, i, etiquette=""):
    """Une note écrite, avec ses petites notes et son signe ; `etiquette` va sous la note."""
    x = notes[i]
    duree = lily_duree(x.valeur)
    if x.note is None:
        return "r" + duree
    tete = x.note.lily() + duree
    if x.orn is None:
        return tete + etiquette
    if x.orn == "appogiature":
        # Les petites notes sont gravées en croches, comme dans les éditions
        # anciennes : la règle, non la valeur écrite, donne leur durée.
        return r"\appoggiatura %s8 %s%s" % (x.petites[0].lily(), tete, etiquette)
    if x.orn == "acciaccatura":
        return r"\acciaccatura %s8 %s%s" % (x.petites[0].lily(), tete, etiquette)
    if x.orn == "mordant":
        return tete + signe("mordent", alt_bas=x.alt_bas) + etiquette
    if x.orn == "trémolo":
        return "%s:%d%s" % (tete, unite_tremolo(x.barres).denominator, etiquette)
    if x.orn == "trémolo à deux notes":
        unite = unite_tremolo(x.barres)
        return r"\repeat tremolo %d { %s%d%s %s%d }" % (
            x.valeur / (2 * unite), x.note.lily(), unite.denominator, etiquette,
            x.petites[0].lily(), unite.denominator)
    if x.orn == "trille" and x.petites:
        bas, fin = x.petites
        return r"\afterGrace %s\startTrillSpan%s { %s16[ %s16\stopTrillSpan] }" % (
            tete, etiquette, bas.lily(), fin.lily())
    if x.orn == "trille":
        return tete + signe("trill", x.alt_haut) + etiquette
    if x.orn == "gruppetto":
        return tete + signe("turn", x.alt_haut, x.alt_bas) + etiquette
    if x.orn == "gruppetto renversé":
        return tete + signe("reverseturn", x.alt_haut, x.alt_bas) + etiquette
    if x.orn == "gruppetto après":
        # La note n'occupe que la moitié de sa place ; le signe, posé sur un
        # silence invisible, tombe entre elle et la suivante.
        moitie = lily_duree(x.valeur / 2)
        return r"%s*1/2%s s%s%s" % (tete, etiquette, moitie, signe("turn", x.alt_haut, x.alt_bas))
    if x.orn == "fioriture":
        petites = [k.lily() + ("16[" if j == 0 else "]" if j == len(x.petites) - 1 else "")
                   for j, k in enumerate(x.petites)]
        return r"%s%s \grace { %s }" % (tete, etiquette, " ".join(petites))
    raise ValueError(x.orn)


def portee_ecrite(exemple, numeros=False):
    corps, armure, k = [], None, 0
    for a, notes in exemple.mesures:
        if a != armure:
            corps.append(cle_armure(a))
            armure = a
        for i, x in enumerate(notes):
            etiquette = ""
            if x.orn:
                k += 1
                if numeros:
                    etiquette += r"_\markup \small %d" % k
            if x.sous:
                etiquette += r'_\markup \small \italic "%s"' % x.sous
            corps.append(lily_ecrite(notes, i, etiquette))
        corps.append("|")
    return corps


def groupes(jouees):
    """
    Les notes jouées d'une mesure, en groupes réunis par des poutres : les
    notes brèves consécutives d'un même temps (la noire).
    """
    res, pos, temps_courant = [], Fraction(0), None
    for j in jouees:
        note, v, _ = j
        breve = note is not None and v < NOIRE
        temps = pos // NOIRE
        dans_le_temps = pos + v <= (temps + 1) * NOIRE
        if breve and dans_le_temps and temps == temps_courant and res:
            res[-1].append(j)
        else:
            res.append([j])
            temps_courant = temps if breve and dans_le_temps else None
        pos += v
    return res


def portee_jouee(exemple, options):
    corps, armure = [], None
    for a, jouees in mesures_jouees(exemple, options):
        if a != armure:
            corps.append(cle_armure(a))
            armure = a
        for g in groupes(jouees):
            for k, (note, valeur, liee) in enumerate(g):
                txt = ("r" if note is None else note.lily()) + lily_duree(valeur)
                if len(g) > 1 and k == 0:
                    txt += "["
                if len(g) > 1 and k == len(g) - 1:
                    txt += "]"
                if liee:
                    txt += "~"
                corps.append(txt)
        corps.append("|")
    return corps


def figure(exemple, numeros=False):
    temps = r"\time %d/%d" % exemple.temps
    portees = [("écrit", portee_ecrite(exemple, numeros))]
    if not numeros:
        portees += [(titre, portee_jouee(exemple, options)) for titre, options in exemple.lectures]
    # Une petite note au tout début de la portée écrite doit avoir son pendant,
    # invisible, dans les autres : sans lui, LilyPond y répète clé et chiffrage.
    if portees[0][1][1].startswith(("\\appoggiatura", "\\acciaccatura")):
        for _, corps in portees[1:]:
            corps.insert(1, r"\grace s8")
    blocs = []
    for i, (titre, corps) in enumerate(portees):
        nom = (r"\with { instrumentName = %s }" % nom_portee(titre)) if len(portees) > 1 else ""
        # Les portées jouées posent leurs poutres elles-mêmes, temps par temps ;
        # les numéros de l'exercice s'alignent à distance fixe de la portée.
        reglages = r" \autoBeamOff" if i > 0 else ""
        if numeros:
            reglages += r" \override TextScript.staff-padding = #4"
        blocs.append(r"""    \new Staff %s {
      \clef treble %s%s
      %s
      \bar "|."
    }""" % (nom, temps, reglages, " ".join(corps[:-1])))
    if len(blocs) == 1:
        musique = blocs[0].strip()
    else:
        musique = "\\new StaffGroup <<\n" + "\n".join(blocs) + "\n  >>"
    retrait = "indent = 17\\mm" if len(portees) > 1 else ""
    return r"""\score {
  %s
  \layout {
    %s
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
""" % (musique, retrait)


def ecrire_gravures():
    produits = [ecrire(nom, figure(ex), preambule=PREAMBULE_ORNEMENTS)
                for nom, ex in EXEMPLES.items()]
    produits.append(ecrire("o-exercice", figure(EXERCICE, numeros=True),
                           preambule=PREAMBULE_ORNEMENTS))
    return produits


# ---------------------------------------------------------------------------
# Réponses et MusicXML
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_ornements.py — ne pas modifier à la main.\n"

VALEURS = {N(1, 2): ("blanche", "blanches"), N(1, 4): ("noire", "noires"),
           N(1, 8): ("croche", "croches"), N(1, 16): ("double croche", "doubles croches"),
           N(1, 32): ("triple croche", "triples croches"),
           N(3, 4): ("blanche pointée", "blanches pointées"),
           N(3, 8): ("noire pointée", "noires pointées"),
           N(3, 16): ("croche pointée", "croches pointées"),
           N(7, 32): ("croche doublement pointée", "croches doublement pointées")}
FOIS = {3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit"}


def decrire_suite(noms_notes):
    """Une suite de noms ; une alternance répétée se dit en une fois."""
    a = noms_notes[:2]
    k = 0
    while noms_notes[2 * k:2 * k + 2] == a:
        k += 1
    if len(a) == 2 and k >= 3:
        reste = noms_notes[2 * k:]
        txt = f"{a[0]} et {a[1]} {FOIS[k]} fois"
        return txt + (", puis " + ", ".join(reste) if reste else "")
    return ", ".join(noms_notes)


def decrire(jouees):
    """Les notes jouées, groupées par valeur : « ré (blanche), do (noire) »."""
    morceaux, i = [], 0
    while i < len(jouees):
        j = i
        while j < len(jouees) and jouees[j][1] == jouees[i][1]:
            j += 1
        singulier, pluriel = VALEURS[jouees[i][1]]
        noms_notes = [x for x, _ in jouees[i:j]]
        morceaux.append(f"{decrire_suite(noms_notes)} ({pluriel if j - i > 1 else singulier})")
        i = j
    return ", ".join(morceaux)


def ecrire_reponses():
    lignes = [r"\begin{enumerate}[label=\textbf{\arabic*}~:, leftmargin=2.2em, itemsep=1pt]"]
    lignes += [rf"  \item {nom} --- {decrire(jouees)}." for nom, jouees in reponses_exercice()]
    lignes.append(r"\end{enumerate}")
    chemin = os.path.join(DIR_LY, "ornements-reponses.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + "\n".join(lignes) + "\n")
    return chemin


# Les entrées du fichier MusicXML : chaque exemple, sous chacune de ses lectures.
LIBELLES = {
    "o-apercu": "appogiature, mordant, trille, gruppetto sur do",
    "o-appogiature": "l'appogiature sur une blanche, une noire, des croches",
    "o-appog-longues": "l'appogiature sur des notes pointées, puis devant un silence",
    "o-acciaccatura": "appogiature longue, puis brève",
    "o-trille": "le trille avec terminaison",
    "o-trille-epoques": "le trille sur si",
    "o-tremolo": "trémolo à une barre, à deux barres, puis à deux notes",
    "o-gruppetto": "gruppetto sur la note, après la note, renversé",
    "o-gruppetto-alt": "gruppetto sur sol, puis avec un dièse sous le signe",
    "o-fioriture": "une fioriture",
}
SUFFIXES = {"XVIIIe s.": "au XVIIIe siècle", "XIXe s.": "au XIXe siècle"}


def ecrire_musicxml():
    entrees = []
    for nom, ex in list(EXEMPLES.items()) + [("o-exercice", EXERCICE)]:
        for titre, options in ex.lectures:
            libelle = LIBELLES.get(nom, "l'exercice, joué")
            if len(ex.lectures) > 1:
                libelle += f", {SUFFIXES[titre]}"
            mesures = [(a, groupes(jouees)) for a, jouees in mesures_jouees(ex, options)]
            # Une entrée MusicXML garde une armure : on la coupe à chaque changement.
            debut = 0
            for i in range(1, len(mesures) + 1):
                if i == len(mesures) or mesures[i][0] != mesures[debut][0]:
                    entrees.append((libelle if debut == 0 else "", mesures[debut][0], "major",
                                    ex.temps, [grps for _, grps in mesures[debut:i]]))
                    debut = i
    chemin = os.path.join(RACINE, "ornements.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_rythmee(
            "Les ornements",
            "Les exemples du guide, écrits en toutes notes tels qu'ils se jouent, "
            f"à la noire {TEMPO}.", entrees, "Piano", TEMPO))
    return chemin


if __name__ == "__main__":
    verifier()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, RACINE))
    print("Réponses :", os.path.relpath(ecrire_reponses(), RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
