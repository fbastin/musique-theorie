#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, les réponses de l'exercice et le fichier MusicXML du
guide « Les mordants ».

    python3 outils/generer_mordants.py

Un ornement y est une règle : d'une note écrite, de sa valeur et de l'armure,
elle tire les notes jouées. Les portées « joué » des gravures, les réponses de
l'exercice et le fichier MusicXML en dérivent, si bien que le signe et ce qu'il
faut jouer ne peuvent pas se contredire. Les affirmations du texte — la
voisine à un ton ou à un demi-ton, l'ornement de même durée sur toute valeur,
la note principale sur le temps, le mordant supérieur au début du trille — sont
vérifiées avant toute écriture.
"""

import os
import re
import sys
from collections import namedtuple
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import LETTRES, Note, armure_notes
from generer import DIR_LY, PREAMBULE, RACINE, _lily_tonique, ecrire
from intervalles import analyser
import musicxml

PREAMBULE_MORDANTS = PREAMBULE.replace("outils/generer.py", "outils/generer_mordants.py")

# Une note d'ornement dure une triple croche ; à la noire 80, un peu moins
# d'un dixième de seconde. Elle ne dépend pas de la valeur de la note ornée.
TRIPLE_CROCHE = Fraction(1, 32)
NOIRE = Fraction(1, 4)
TEMPO = 80

# ---------------------------------------------------------------------------
# Modèle : du signe aux notes jouées
# ---------------------------------------------------------------------------
# Un ornement est un motif joué vite, puis la note principale tenue jusqu'au
# bout de sa valeur. Le motif s'écrit avec trois lettres : P pour la note
# principale, H pour sa voisine du dessus, B pour sa voisine du dessous.
# Le gruppetto se joue en doubles croches : à l'allure d'un mordant, il
# sonnerait comme un trait.
ORNEMENTS = {
    "mordant inférieur": ("PB", TRIPLE_CROCHE),
    "mordant supérieur": ("PH", TRIPLE_CROCHE),
    "mordant long": ("PBPB", TRIPLE_CROCHE),
    "trille court": ("HPHP", TRIPLE_CROCHE),
    "gruppetto": ("HPB", Fraction(1, 16)),
}

# Le trille alterne jusqu'au bout de la valeur ; sa note de départ dépend de
# l'époque : la voisine du dessus au XVIIIe siècle, la note ensuite.
TRILLES = {"trille": "voisine", "trille sur la note": "note"}

# Ce que désigne chaque signe. Depuis le XIXe siècle, le signe sans trait se
# lit comme un mordant supérieur, et le trille commence sur la note ; chez
# Bach, le signe sans trait est un trille court, et le trille commence sur la
# voisine.
LECTURE = {"mordent": "mordant inférieur", "prall": "mordant supérieur",
           "prallmordent": "mordant long", "trill": "trille sur la note",
           "turn": "gruppetto"}
LECTURE_BACH = dict(LECTURE, prall="trille court", trill="trille")


def cote(ornement):
    """
    Côté de la voisine qu'emploie l'ornement : −1 au-dessous, 1 au-dessus. Une
    altération écrite près du signe modifie cette voisine-là ; elle s'écrit
    sous le signe pour la voisine inférieure, au-dessus pour la supérieure.
    """
    motif = "H" if ornement in TRILLES else ORNEMENTS[ornement][0]
    return -1 if "H" not in motif else 1


def alt_armure(lettre, armure):
    """Altération qu'impose l'armure à une lettre."""
    if lettre not in armure_notes(armure):
        return 0
    return 1 if armure > 0 else -1


def voisine(note, sens, armure, alt=None):
    """
    La note voisine, une lettre plus haut (sens = 1) ou plus bas (sens = −1).

    Sa lettre est imposée ; son altération vient de l'armure, sauf altération
    écrite près du signe (`alt`).
    """
    i = note.idx + sens
    lettre = LETTRES[i % 7]
    return Note(lettre, alt_armure(lettre, armure) if alt is None else alt,
                note.octave + i // 7)


def trille(note, valeur, haut, bas, depart, terminaison):
    """
    L'alternance de la note et de sa voisine du dessus, en triples croches,
    jusqu'au bout de la valeur ; elle s'achève toujours sur la note.

    Commencé sur la voisine, le trille compte un nombre pair de notes et finit
    de lui-même sur la note ; la terminaison remplace les deux dernières par la
    voisine du dessous et la note. Commencé sur la note, il s'arrête sur elle,
    tenue deux triples croches ; la terminaison s'insère juste avant.
    """
    k = int(valeur / TRIPLE_CROCHE)
    if depart == "voisine":
        motif = [haut if i % 2 == 0 else note for i in range(k)]
        if terminaison:
            motif[-2:] = [bas, note]
        return [(x, TRIPLE_CROCHE, False) for x in motif]
    m = k - 3 if terminaison else k - 2
    motif = [note if i % 2 == 0 else haut for i in range(m)] + ([bas] if terminaison else [])
    return [(x, TRIPLE_CROCHE, False) for x in motif] + [(note, 2 * TRIPLE_CROCHE, False)]


def realiser(note, valeur, ornement, armure, alt=None, terminaison=False):
    """
    Les notes jouées : liste de (note, valeur, liée à la suivante).

    Le motif commence avec la note écrite, sur le temps ; la note principale
    garde le reste de la valeur. Si le motif s'achève déjà sur elle, elle y est
    liée au lieu d'être rejouée. Le trille, lui, alterne jusqu'au bout de la
    valeur, avec ou sans terminaison.
    """
    sens = cote(ornement)
    haut = voisine(note, 1, armure, alt if sens == 1 else None)
    bas = voisine(note, -1, armure, alt if sens == -1 else None)
    if ornement in TRILLES:
        return trille(note, valeur, haut, bas, TRILLES[ornement], terminaison)
    motif, rapide = ORNEMENTS[ornement]
    jouees = [({"P": note, "H": haut, "B": bas}[c], rapide, False) for c in motif]
    reste = valeur - rapide * len(motif)
    assert reste > 0, (note, valeur, ornement)
    if motif[-1] == "P":
        jouees[-1] = (note, rapide, True)
    return jouees + [(note, reste, False)]


def taille(a, b):
    """« ton » ou « demi-ton » : l'écart entre une note et sa voisine."""
    grave, aigu = sorted((a, b), key=lambda n: n.hauteur)
    numero, qualite = analyser(grave, aigu)
    assert numero == 2, (a, b)
    return {"majeure": "ton", "mineure": "demi-ton"}[qualite]


# ---------------------------------------------------------------------------
# Les exemples
# ---------------------------------------------------------------------------
# Une note écrite : hauteur, valeur (fraction de ronde), signe éventuel (nom
# LilyPond), altération écrite près du signe, texte sous la note, terminaison
# du trille écrite en petites notes.
Ecrite = namedtuple("Ecrite", "note valeur signe alt sous fin",
                    defaults=(None, None, None, False))
# Un exemple : chiffrage, mesures — chacune une armure et des notes écrites —,
# portées jouées (titre, lecture des signes), écart à noter sous les voisines.
Exemple = namedtuple("Exemple", "temps mesures lectures tailles", defaults=(False,))

N = Fraction
JOUE = (("joué", LECTURE),)


def n(txt):
    """« C5 », « F#4 » -> Note, octaves du modèle (4 : celle du do central)."""
    lettre, alt, octave = txt[0], txt[1:-1].count("#") - txt[1:-1].count("b"), int(txt[-1])
    return Note(lettre, alt, octave)


def suite(signe, notes, valeur):
    return [Ecrite(n(x), valeur, signe) for x in notes]


EPOQUES = (("XVIIIe s.", LECTURE_BACH), ("XIXe s.", LECTURE))

EXEMPLES = {
    # Les deux mordants sur la même note : la voisine du dessous, puis du dessus.
    "m-deux": Exemple((2, 4), [(0, [Ecrite(n("C5"), N(1, 4), "mordent", sous="inférieur"),
                                    Ecrite(n("C5"), N(1, 4), "prall", sous="supérieur")])],
                      JOUE),
    # Do, ré, mi, fa : une voisine à un demi-ton, deux à un ton, une à un demi-ton.
    "m-inferieur": Exemple((4, 4), [(0, suite("mordent", ["C5", "D5", "E5", "F5"], N(1, 4)))],
                           JOUE, tailles=True),
    "m-superieur": Exemple((4, 4), [(0, suite("prall", ["C5", "D5", "E5", "F5"], N(1, 4)))],
                           JOUE, tailles=True),
    # Le même ornement sur une blanche, une noire, une croche.
    "m-valeurs": Exemple((4, 4), [(0, [Ecrite(n("C5"), N(1, 2), "mordent"),
                                       Ecrite(n("D5"), N(1, 4), "mordent"),
                                       Ecrite(n("E5"), N(1, 8), "mordent"),
                                       Ecrite(n("F5"), N(1, 8))])], JOUE),
    # La voisine de sol : par la gamme de do, par une altération, par l'armure.
    "m-alterations": Exemple((2, 4), [(0, [Ecrite(n("G4"), N(1, 2), "mordent")]),
                                      (0, [Ecrite(n("G4"), N(1, 2), "mordent", 1)]),
                                      (1, [Ecrite(n("G4"), N(1, 2), "mordent")])],
                             JOUE, tailles=True),
    "m-long": Exemple((2, 4), [(0, [Ecrite(n("C5"), N(1, 4), "mordent"),
                                    Ecrite(n("C5"), N(1, 4), "prallmordent")])], JOUE),
    # Le signe sans trait, lu à deux époques.
    "m-epoques": Exemple((2, 4), [(0, [Ecrite(n("C5"), N(1, 4), "prall"),
                                       Ecrite(n("B4"), N(1, 4))])],
                         (("chez Bach", LECTURE_BACH), ("plus tard", LECTURE))),
    # Le mordant supérieur, puis le trille commencé sur la note : les mêmes trois
    # premières notes. Sur ré, la voisine mi, puis mi bémol par le bémol écrit.
    "m-trille-debut": Exemple((4, 4), [(0, [Ecrite(n("C5"), N(1, 4), "prall", sous="mordant sup."),
                                            Ecrite(n("C5"), N(1, 4), "trill", sous="trille"),
                                            Ecrite(n("D5"), N(1, 4), "trill"),
                                            Ecrite(n("D5"), N(1, 4), "trill", -1)])],
                              JOUE, tailles=True),
    # Un trille long sur ré, avec la ligne ondulée et la terminaison, lu aux deux
    # époques, puis do.
    "m-trille": Exemple((4, 4), [(0, [Ecrite(n("D5"), N(1, 2), "trill", fin=True),
                                      Ecrite(n("C5"), N(1, 2))])], EPOQUES),
    "m-voisins": Exemple((3, 4), [(0, [Ecrite(n("C5"), N(1, 4), "mordent", sous="mordant inf."),
                                       Ecrite(n("C5"), N(1, 4), "trill", sous="trille"),
                                       Ecrite(n("C5"), N(1, 4), "turn", sous="gruppetto")])],
                         JOUE),
}

# L'exercice : une mélodie en sol majeur, ses ornements numérotés sous la portée.
EXERCICE = Exemple((4, 4), [
    (1, [Ecrite(n("G4"), N(1, 4), "mordent"), Ecrite(n("A4"), N(1, 8)), Ecrite(n("B4"), N(1, 8)),
         Ecrite(n("C5"), N(1, 4)), Ecrite(n("B4"), N(1, 4), "mordent")]),
    (1, [Ecrite(n("A4"), N(1, 4)), Ecrite(n("D5"), N(1, 4), "prall"),
         Ecrite(n("C5"), N(1, 4), "mordent"), Ecrite(n("B4"), N(1, 4))]),
    (1, [Ecrite(n("E5"), N(1, 4), "prall"), Ecrite(n("D5"), N(1, 8)), Ecrite(n("C5"), N(1, 8)),
         Ecrite(n("A4"), N(1, 4), "mordent", 1), Ecrite(n("B4"), N(1, 4), "prall")]),
    (1, [Ecrite(n("A4"), N(1, 4)), Ecrite(n("F#4"), N(1, 4), "trill"),
         Ecrite(n("G4"), N(1, 2), "prallmordent")]),
], JOUE)


def jouer(e, armure, lecture):
    """Les notes jouées pour une note écrite."""
    if e.signe is None:
        return [(e.note, e.valeur, False)]
    return realiser(e.note, e.valeur, lecture[e.signe], armure, e.alt, e.fin)


def ornees(exemple):
    """Les notes ornées d'un exemple, dans l'ordre, avec leur armure."""
    return [(armure, e) for armure, notes in exemple.mesures for e in notes if e.signe]


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def verifier():
    do_majeur = [n(x) for x in ("C5", "D5", "E5", "F5")]
    # En do majeur, la voisine inférieure de do et de fa est à un demi-ton,
    # celle de ré et de mi à un ton ; la supérieure de mi seule à un demi-ton.
    assert [taille(x, voisine(x, -1, 0)) for x in do_majeur] == ["demi-ton", "ton", "ton", "demi-ton"]
    assert [taille(x, voisine(x, 1, 0)) for x in do_majeur] == ["ton", "ton", "demi-ton", "ton"]

    # Chaque mesure écrite est complète.
    for exemple in list(EXEMPLES.values()) + [EXERCICE]:
        for _, notes in exemple.mesures:
            assert sum(e.valeur for e in notes) == Fraction(*exemple.temps)

    # Partout, la voisine est une seconde et la valeur écrite est respectée ;
    # un mordant commence et finit sur la note écrite ; un trille alterne la
    # note et sa voisine du dessus, à un ton ou à un demi-ton, et finit sur la
    # note, par la voisine du dessous s'il a sa terminaison.
    for exemple in list(EXEMPLES.values()) + [EXERCICE]:
        for _, lecture in exemple.lectures:
            for armure, e in ornees(exemple):
                jouees = jouer(e, armure, lecture)
                assert sum(v for _, v, _ in jouees) == e.valeur
                if lecture[e.signe].startswith("mordant"):
                    assert jouees[0][0] is e.note and jouees[-1][0] is e.note
                    taille(e.note, jouees[1][0])
                if lecture[e.signe] in TRILLES:
                    haut = voisine(e.note, 1, armure, e.alt)
                    bas = voisine(e.note, -1, armure)
                    alternance = jouees[:-2] if e.fin else jouees
                    assert {repr(x) for x, _, _ in alternance} == {repr(e.note), repr(haut)}
                    assert all(repr(a) != repr(b) for (a, _, _), (b, _, _)
                               in zip(alternance, alternance[1:]))
                    taille(e.note, haut)
                    assert jouees[-1][0] is e.note
                    if e.fin:
                        assert repr(jouees[-2][0]) == repr(bas)

    # Trois notes pour le mordant, cinq pour le mordant long.
    do = n("C5")
    assert len(realiser(do, N(1, 4), "mordant inférieur", 0)) == 3
    assert len(realiser(do, N(1, 4), "mordant long", 0)) == 5

    # Sur une blanche, une noire, une croche : le même ornement, deux triples
    # croches ; la note principale garde le reste.
    for e in EXEMPLES["m-valeurs"].mesures[0][1][:3]:
        jouees = realiser(e.note, e.valeur, "mordant inférieur", 0)
        assert sum(v for _, v, _ in jouees[:2]) == 2 * TRIPLE_CROCHE
    # À la noire 80, une triple croche dure un peu moins d'un dixième de seconde.
    assert 0.09 < 60 / TEMPO / 8 < 0.1

    # Sol : fa en do majeur (un ton), fa dièse avec le dièse sous le signe ou
    # en sol majeur (un demi-ton).
    sol = n("G4")
    assert realiser(sol, N(1, 2), "mordant inférieur", 0)[1][0].nom_fr() == "fa"
    assert realiser(sol, N(1, 2), "mordant inférieur", 0, alt=1)[1][0].nom_fr() == "fa dièse"
    assert realiser(sol, N(1, 2), "mordant inférieur", 1)[1][0].nom_fr() == "fa dièse"

    # Le signe sans trait : chez Bach, ré do ré do ; plus tard, do ré do.
    assert [x.nom_fr() for x, _, _ in realiser(do, N(1, 4), "trille court", 0)] == ["ré", "do", "ré", "do", "do"]
    assert [x.nom_fr() for x, _, _ in realiser(do, N(1, 4), "mordant supérieur", 0)] == ["do", "ré", "do"]
    # Le gruppetto tourne autour de la note : ré, do, si, do.
    assert [x.nom_fr() for x, _, _ in realiser(do, N(1, 4), "gruppetto", 0)] == ["ré", "do", "si", "do"]

    # Les deux mordants sur do : si en dessous, ré au-dessus.
    assert [noms(jouer(e, 0, LECTURE)) for e in EXEMPLES["m-deux"].mesures[0][1]] == \
        [["do", "si", "do"], ["do", "ré", "do"]]

    # Le trille : au XVIIIe siècle, il commence sur la voisine ; ensuite, sur
    # la note. Sur une noire, huit triples croches depuis la voisine ; depuis la
    # note, six, puis la note tenue deux triples croches.
    assert noms(realiser(do, N(1, 4), "trille", 0)) == ["ré", "do"] * 4
    assert noms(realiser(do, N(1, 4), "trille sur la note", 0)) == ["do", "ré"] * 3 + ["do"]
    # Le mordant supérieur sonne comme le début d'un trille commencé sur la note.
    assert noms(realiser(do, N(1, 4), "mordant supérieur", 0)) == \
        noms(realiser(do, N(1, 4), "trille sur la note", 0))[:3]
    # Sur ré, la voisine mi est à un ton ; un bémol près du signe donne mi
    # bémol, à un demi-ton.
    re_ = n("D5")
    assert taille(re_, realiser(re_, N(1, 4), "trille sur la note", 0)[1][0]) == "ton"
    avec_bemol = realiser(re_, N(1, 4), "trille sur la note", 0, alt=-1)[1][0]
    assert avec_bemol.nom_fr() == "mi bémol" and taille(re_, avec_bemol) == "demi-ton"
    # La terminaison : do, puis ré, à la fin du trille sur ré, aux deux époques.
    for depart in TRILLES:
        assert noms(realiser(re_, N(1, 2), depart, 0, terminaison=True))[-2:] == ["do", "ré"]

    # L'exercice : la voisine du sixième ornement est haussée par le dièse
    # écrit, le septième est à un demi-ton par la gamme, le dernier fait cinq notes.
    # Le trille, sur fa dièse, alterne avec sol, à un demi-ton.
    rep = reponses_exercice()
    assert rep[5] == ["la", "sol dièse", "la"]
    assert rep[6] == ["si", "do", "si"]
    assert rep[7] == ["fa dièse", "sol"] * 3 + ["fa dièse"]
    assert rep[0] == ["sol", "fa dièse", "sol"] and len(rep[-1]) == 5


def noms(jouees):
    return [x.nom_fr() for x, _, _ in jouees]


# Le nom de chaque ornement dans les réponses.
NOMS = {"mordant inférieur": "mordant inférieur", "mordant supérieur": "mordant supérieur",
        "mordant long": "mordant long", "trille sur la note": "trille"}


def noms_exercice():
    _, lecture = EXERCICE.lectures[0]
    return [NOMS[lecture[e.signe]] for _, e in ornees(EXERCICE)]


def reponses_exercice():
    _, lecture = EXERCICE.lectures[0]
    res = []
    for armure, e in ornees(EXERCICE):
        jouees = jouer(e, armure, lecture)
        # Une note liée à la suivante ne se rejoue pas : on ne la nomme qu'une fois.
        res.append([x.nom_fr() for i, (x, _, _) in enumerate(jouees)
                    if i == 0 or not jouees[i - 1][2]])
    return res


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
DUREES_LILY = {Fraction(1): "1", Fraction(1, 2): "2", Fraction(1, 4): "4",
               Fraction(1, 8): "8", Fraction(1, 16): "16", Fraction(1, 32): "32"}
ALT_MARKUP = {-2: r"\doubleflat", -1: r"\flat", 0: r"\natural", 1: r"\sharp", 2: r"\doublesharp"}


def lily_duree(valeur):
    for base, txt in DUREES_LILY.items():
        for points in range(3):
            if base * (2 - Fraction(1, 2 ** points)) == valeur:
                return txt + "." * points
    raise ValueError(valeur)


def signe_lily(e):
    """Le signe, et l'altération qui l'accompagne, du côté de la voisine qu'elle modifie."""
    if e.alt is None:
        return "\\" + e.signe
    glyphe = rf'\musicglyph "scripts.{e.signe}"'
    alt = rf"\teeny {ALT_MARKUP[e.alt]}"
    pile = [glyphe, alt] if cote(LECTURE[e.signe]) < 0 else [alt, glyphe]
    return (r"-\tweak self-alignment-X #CENTER ^\markup \override #'(baseline-skip . 1.9) "
            r"\center-column { %s }" % " ".join(pile))


def cle_armure(armure):
    return r"\key %s \major" % _lily_tonique(armure, "major")


def portee_ecrite(exemple, numeros=False):
    corps, armure, k = [], None, 0
    for a, notes in exemple.mesures:
        if a != armure:
            corps.append(cle_armure(a))
            armure = a
        for e in notes:
            txt = e.note.lily() + lily_duree(e.valeur)
            etiquette = ""
            if e.signe:
                k += 1
                if numeros:
                    etiquette += r"_\markup \small %d" % k
            if e.sous:
                etiquette += r'_\markup \small \italic "%s"' % e.sous
            if e.fin:
                # Le trille long : la ligne ondulée, puis la terminaison en
                # petites notes, la voisine du dessous et la note.
                bas = voisine(e.note, -1, a)
                txt = r"\afterGrace %s\startTrillSpan%s { %s16[ %s16\stopTrillSpan] }" % (
                    txt, etiquette, bas.lily(), e.note.lily())
            elif e.signe:
                txt += signe_lily(e) + etiquette
            else:
                txt += etiquette
            corps.append(txt)
        corps.append("|")
    return corps


def groupes(jouees):
    """
    Les notes jouées pour une note écrite, en groupes réunis par des poutres :
    les notes brèves consécutives d'un même temps (la noire), la note tenue
    avec elles si elle a un crochet. Une note ornée commence sur un temps.
    """
    res, pos, courant = [], Fraction(0), None
    for j in jouees:
        v = j[1]
        temps = pos // NOIRE
        breve = v < NOIRE and pos + v <= (temps + 1) * NOIRE
        if breve and temps == courant:
            res[-1].append(j)
        else:
            res.append([j])
            courant = temps if breve else None
        pos += v
    return res


def mesures_jouees(exemple, lecture):
    """Les mesures jouées : pour chacune, son armure et ses groupes de notes."""
    return [(a, [g for e in notes for g in groupes(jouer(e, a, lecture))])
            for a, notes in exemple.mesures]


def portee_jouee(exemple, lecture):
    """La portée jouée ; si l'exemple le demande, l'écart à la voisine noté sous elle."""
    corps, armure = [], None
    for a, notes in exemple.mesures:
        if a != armure:
            corps.append(cle_armure(a))
            armure = a
        for e in notes:
            jouees = jouer(e, a, lecture)
            i = 0
            for g in groupes(jouees):
                for k, (note, valeur, liee) in enumerate(g):
                    txt = note.lily() + lily_duree(valeur)
                    if len(g) > 1 and k == 0:
                        txt += "["
                    if len(g) > 1 and k == len(g) - 1:
                        txt += "]"
                    if liee:
                        txt += "~"
                    if exemple.tailles and e.signe and i == 1:
                        txt += r'_\markup \tiny \italic "%s"' % taille(e.note, note)
                    corps.append(txt)
                    i += 1
        corps.append("|")
    return corps


def nom_portee(titre):
    """Le nom d'une portée ; « XVIIIe s. » s'écrit avec un e en exposant."""
    morceaux = re.split(r"([XVI]+)e", titre)
    if len(morceaux) == 1:
        return r'\markup \small \italic "%s"' % titre
    elements = []
    for i, m in enumerate(morceaux):
        if i % 2:
            elements.append(r'"%s" \super "e"' % m)
        elif m:
            elements.append('"%s"' % m)
    return r"\markup \small \italic \concat { %s }" % " ".join(elements)


def figure(nom_figure, exemple, numeros=False):
    temps = r"\time %d/%d" % exemple.temps
    portees = [("écrit", portee_ecrite(exemple, numeros))]
    if not numeros:
        portees += [(titre, portee_jouee(exemple, lecture))
                    for titre, lecture in exemple.lectures]
    blocs = []
    for i, (titre, corps) in enumerate(portees):
        nom = (r"\with { instrumentName = %s }" % nom_portee(titre)
               if len(portees) > 1 else "")
        # Les portées jouées posent leurs poutres elles-mêmes, groupe par groupe ;
        # les numéros de l'exercice s'alignent à distance fixe de la portée.
        poutres = r" \autoBeamOff" if i > 0 else ""
        if numeros:
            poutres += r" \override TextScript.staff-padding = #4"
        blocs.append(r"""    \new Staff %s {
      \clef treble %s%s
      %s
      \bar "|."
    }""" % (nom, temps, poutres, " ".join(corps[:-1])))
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
    produits = [ecrire(nom_figure, figure(nom_figure, ex), preambule=PREAMBULE_MORDANTS)
                for nom_figure, ex in EXEMPLES.items()]
    produits.append(ecrire("m-exercice", figure("m-exercice", EXERCICE, numeros=True),
                           preambule=PREAMBULE_MORDANTS))
    return produits


# ---------------------------------------------------------------------------
# Réponses et MusicXML
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_mordants.py — ne pas modifier à la main.\n"


FOIS = {3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit"}


def decrire(noms_notes):
    """Une suite de noms ; l'alternance d'un trille se dit en une fois."""
    a = noms_notes[:2]
    k = 0
    while noms_notes[2 * k:2 * k + 2] == a:
        k += 1
    if len(a) == 2 and k >= 3:
        reste = noms_notes[2 * k:]
        return f"{a[0]} et {a[1]} {FOIS[k]} fois" + (", puis " + ", ".join(reste) if reste else "")
    return ", ".join(noms_notes)


def ecrire_reponses():
    items = "~; ".join(f"{i}~:~\\emph{{{nom}}}, {decrire(r)}" for i, (nom, r)
                       in enumerate(zip(noms_exercice(), reponses_exercice()), 1))
    chemin = os.path.join(DIR_LY, "mordants-reponses.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + items + ".\n")
    return chemin


# Les entrées du fichier MusicXML : chaque exemple, sous chacune de ses lectures.
LIBELLES = {
    "m-deux": "mordant inférieur, puis mordant supérieur, sur do",
    "m-inferieur": "mordant inférieur sur do, ré, mi, fa",
    "m-superieur": "mordant supérieur sur do, ré, mi, fa",
    "m-valeurs": "sur une blanche, une noire, une croche",
    "m-alterations": "sol : en do majeur, avec un dièse, en sol majeur",
    "m-long": "mordant inférieur, puis mordant long",
    "m-epoques": "le signe sans trait",
    "m-trille-debut": "mordant supérieur, puis trille, sur do ; trille sur ré, puis avec un bémol",
    "m-trille": "trille avec terminaison sur ré",
    "m-voisins": "mordant inférieur, trille, gruppetto",
}
SUFFIXES = {"XVIIIe s.": "au XVIIIe siècle", "XIXe s.": "au XIXe siècle"}


def ecrire_musicxml():
    entrees = []
    for nom_figure, ex in list(EXEMPLES.items()) + [("m-exercice", EXERCICE)]:
        for titre, lecture in ex.lectures:
            libelle = LIBELLES.get(nom_figure, "l'exercice, joué")
            if len(ex.lectures) > 1:
                libelle += f", {SUFFIXES.get(titre, titre)}"
            mesures = mesures_jouees(ex, lecture)
            # Une entrée MusicXML garde une armure : on la coupe à chaque changement.
            debut = 0
            for i in range(1, len(mesures) + 1):
                if i == len(mesures) or mesures[i][0] != mesures[debut][0]:
                    entrees.append((libelle if debut == 0 else "", mesures[debut][0], "major",
                                    ex.temps, [grps for _, grps in mesures[debut:i]]))
                    debut = i
    chemin = os.path.join(RACINE, "mordants.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_rythmee(
            "Les mordants",
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
