#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, le tableau des figures, les exercices et leurs réponses,
et le fichier MusicXML du guide « Les valeurs ».

    python3 outils/generer_valeurs.py

Une valeur y est une fraction de ronde, et un rythme une suite de notes, de
silences et de groupes irréguliers dont la durée se calcule. Les gravures, le
tableau, les réponses des exercices et le fichier MusicXML en dérivent. Les
égalités qu'affirme le texte — chaque figure vaut deux fois la suivante, le
point ajoute la moitié de la valeur, un triolet de croches dure une noire —
sont vérifiées avant toute écriture, ainsi que l'égalité des deux portées de
chaque figure comparative.
"""

import os
import sys
from collections import namedtuple
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import Note
from generer import DIR_LY, PREAMBULE, RACINE, ecrire
import musicxml

PREAMBULE_VALEURS = PREAMBULE.replace("outils/generer.py", "outils/generer_valeurs.py")

# À la noire 60, une noire dure une seconde : les durées du tableau se lisent
# directement en secondes.
TEMPO = 60

# ---------------------------------------------------------------------------
# Les figures
# ---------------------------------------------------------------------------
N = Fraction
RONDE = N(1)

# Nom de la figure de note, sa valeur en fraction de ronde, le silence de même
# valeur. Chaque figure vaut la moitié de la précédente.
FIGURES = [
    ("ronde", N(1), "pause"),
    ("blanche", N(1, 2), "demi-pause"),
    ("noire", N(1, 4), "soupir"),
    ("croche", N(1, 8), "demi-soupir"),
    ("double croche", N(1, 16), "quart de soupir"),
    ("triple croche", N(1, 32), "huitième de soupir"),
    ("quadruple croche", N(1, 64), "seizième de soupir"),
]
VALEUR = {nom: v for nom, v, _ in FIGURES}
VALEUR.update({silence: v for _, v, silence in FIGURES})
# Plus longue que la ronde, rare aujourd'hui : la carrée, ou brève, et son
# silence, le bâton de pause.
CARREE = N(2)
VALEUR.update({"carrée": CARREE, "bâton de pause": CARREE})


def crochets(valeur):
    """Nombre de crochets d'une figure : un par moitié de noire retranchée."""
    k = 0
    while valeur < N(1, 4):
        valeur *= 2
        k += 1
    return k


def pointee(valeur, points=1):
    """Valeur pointée : chaque point ajoute la moitié de ce qu'ajoutait le précédent."""
    return valeur * (2 - N(1, 2 ** points))


def simple(valeur):
    """Vrai si la valeur s'écrit d'une seule figure, pointée ou non."""
    try:
        musicxml.type_et_points(valeur)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Rythmes : notes, silences, ligatures, groupes irréguliers
# ---------------------------------------------------------------------------
# Une note ou un silence (note None) : valeur écrite, pointée comprise ;
# `liee` si elle se prolonge dans la suivante ; `marques` parmi « fermata »,
# « ( » et « ) » (début et fin d'une liaison d'expression) ; `texte` à
# imprimer près de la note.
Ev = namedtuple("Ev", "note valeur liee marques texte", defaults=(False, (), None))
# Des notes réunies par une ligature.
Poutre = namedtuple("Poutre", "evs")
# Un groupe irrégulier : `reelles` notes écrites dans le temps de `normales`.
Irr = namedtuple("Irr", "reelles normales items")


def n(txt):
    """« C5 », « F#4 » -> Note, octaves du modèle (4 : celle du do central)."""
    lettre, alt, octave = txt[0], txt[1:-1].count("#") - txt[1:-1].count("b"), int(txt[-1])
    return Note(lettre, alt, octave)


# La3, le la du diapason, au deuxième interligne de la clé de sol : hampe
# montante, crochets à droite.
LA = n("A4")


def ev(valeur, note=LA, **kw):
    return Ev(note, valeur, **kw)


def pause(valeur, **kw):
    return Ev(None, valeur, **kw)


def poutre(valeur, notes, **kw):
    """Des notes de même valeur sous une ligature ; `notes` : liste ou nombre de la3."""
    if isinstance(notes, int):
        notes = [LA] * notes
    return Poutre([Ev(x, valeur, **(kw if i == 0 else {})) for i, x in enumerate(notes)])


def duree(item):
    """Durée réelle d'une note, d'un groupe ou d'une liste, en fraction de ronde."""
    if isinstance(item, Ev):
        return item.valeur
    if isinstance(item, Poutre):
        return sum(e.valeur for e in item.evs)
    if isinstance(item, Irr):
        return sum(duree(i) for i in item.items) * N(item.normales, item.reelles)
    return sum(duree(i) for i in item)


def evs(item):
    """Les notes et silences d'un élément, dans l'ordre."""
    if isinstance(item, Ev):
        return [item]
    if isinstance(item, Poutre):
        return list(item.evs)
    return [e for i in item.items for e in evs(i)]


# ---------------------------------------------------------------------------
# Les figures du guide
# ---------------------------------------------------------------------------
# Une figure : des portées (nom, segments), chaque segment une liste
# d'éléments ; une barre sépare les segments. Les segments de même rang ont la
# même durée sur toutes les portées : ils se correspondent.
Figure = namedtuple("Figure", "portees numeros arbre espacement ligne",
                    defaults=(False, False, 1.6, 300))


def une_portee(segments):
    return Figure([("", segments)])


FIG_NOTES = une_portee([[ev(v, texte=nom)] for nom, v, _ in FIGURES])
FIG_SILENCES = une_portee([[pause(v, texte=silence)] for _, v, silence in FIGURES])

# La tête, la hampe, le crochet, la ligature : une croche montante, une
# descendante, deux croches ligaturées.
FIG_ANATOMIE = Figure([("", [[ev(N(1, 8), texte="hampe montante")],
                              [ev(N(1, 8), n("E5"), texte="hampe descendante")],
                              [poutre(N(1, 8), [LA, n("C5")], texte="ligature")]])],
                      espacement=2.4)

# L'arbre des valeurs : une ronde, puis chaque étage double le nombre de notes.
ARBRE = [("1 ronde", N(1)), ("2 blanches", N(1, 2)), ("4 noires", N(1, 4)),
         ("8 croches", N(1, 8)), ("16 doubles", N(1, 16))]


def etage(valeur):
    nombre = int(RONDE / valeur)
    if valeur >= N(1, 4):
        return [[ev(valeur) for _ in range(nombre)]]
    # Les notes à crochets se ligaturent par noire.
    par_noire = int(N(1, 4) / valeur)
    return [[poutre(valeur, par_noire) for _ in range(nombre // par_noire)]]


FIG_ARBRE = Figure([(nom, etage(v)) for nom, v in ARBRE], arbre=True)

# Le point : chaque valeur pointée, puis la même durée sans point.
FIG_POINT = Figure([
    ("avec point", [[ev(pointee(N(1, 2)), texte="blanche pointée")],
                    [ev(pointee(N(1, 4)), texte="noire pointée")],
                    [ev(pointee(N(1, 8)), texte="croche pointée")],
                    [ev(pointee(N(1, 2), 2), texte="blanche doublement pointée")],
                    [pause(pointee(N(1, 4)), texte="soupir pointé")]]),
    ("sans point", [[ev(N(1, 2), liee=True), ev(N(1, 4))],
                    [ev(N(1, 4), liee=True), ev(N(1, 8))],
                    [Poutre([ev(N(1, 8), liee=True), ev(N(1, 16))])],
                    [ev(N(1, 2), liee=True), ev(N(1, 4), liee=True), ev(N(1, 8))],
                    [pause(N(1, 4)), pause(N(1, 8))]]),
])

# Deux liaisons : la même note prolongée, puis des notes différentes enchaînées.
FIG_LIAISONS = une_portee([
    [ev(N(1, 2), liee=True, texte="liaison de prolongation"), ev(N(1, 8))],
    [ev(N(1, 4), n("C5"), marques=("(",), texte="liaison d'expression"),
     ev(N(1, 4), n("D5")), ev(N(1, 4), n("E5")), ev(N(1, 4), n("F5"), marques=(")",))],
])

FIG_POINT_ORGUE = une_portee([
    [ev(N(1, 4), n("C5")), ev(N(1, 4), n("B4")), ev(N(1, 2), n("C5"), marques=("fermata",),
                                                    texte="sur une note")],
    [ev(N(1, 4), n("E5")), pause(N(1, 4), marques=("fermata",), texte="sur un silence"),
     ev(N(1, 2), n("D5"))],
])

# Les groupes irréguliers, sous la division régulière qu'ils remplacent.
FIG_TRIOLETS = Figure([
    ("régulier", [[poutre(N(1, 8), 2)], [ev(N(1, 4)), ev(N(1, 4))],
                  [poutre(N(1, 16), 2)], [poutre(N(1, 16), 4)]]),
    ("irrégulier", [[Irr(3, 2, [poutre(N(1, 8), 3, texte="triolet de croches")])],
                    [Irr(3, 2, [ev(N(1, 4), texte="triolet de noires"), ev(N(1, 4)), ev(N(1, 4))])],
                    [Irr(3, 2, [poutre(N(1, 16), 3, texte="triolet de doubles")])],
                    [Irr(6, 4, [poutre(N(1, 16), 6, texte="sextolet")])]]),
])

FIG_GROUPES = Figure([
    ("régulier", [[poutre(N(1, 8), 3)], [poutre(N(1, 8), 3)],
                  [poutre(N(1, 16), 4)], [poutre(N(1, 16), 4)]]),
    ("irrégulier", [[Irr(2, 3, [poutre(N(1, 8), 2, texte="duolet")])],
                    [Irr(4, 3, [poutre(N(1, 8), 4, texte="quartolet")])],
                    [Irr(5, 4, [poutre(N(1, 16), 5, texte="quintolet")])],
                    [Irr(7, 4, [poutre(N(1, 16), 7, texte="septolet")])]]),
], espacement=1.4)


def melodie(valeur, noms):
    return poutre(valeur, [n(x) for x in noms.split()])


# L'exercice : des groupes numérotés, sans chiffres indicateurs ; la durée de
# chacun est à donner en noires.
EXERCICE = [
    [ev(pointee(N(1, 4)), n("C5")), ev(N(1, 8), n("D5")), ev(N(1, 2), n("E5"))],
    [ev(N(1, 2), n("E5"), liee=True), melodie(N(1, 8), "E5 D5")],
    [Irr(3, 2, [melodie(N(1, 8), "C5 D5 E5")]), ev(N(1, 4), n("F5"))],
    [Poutre([ev(pointee(N(1, 8)), n("G5")), ev(N(1, 16), n("F5"))]), pause(N(1, 4)),
     ev(N(1, 8), n("E5"))],
    [ev(pointee(N(1, 2), 2), n("E5"))],
    [Irr(6, 4, [melodie(N(1, 16), "D5 E5 F5 G5 F5 E5")]), pause(pointee(N(1, 4))),
     ev(N(1, 8), n("D5"))],
    [pause(N(1, 2)), ev(N(1, 4), n("B4"), liee=True), ev(N(1, 8), n("B4"))],
    [Irr(4, 3, [melodie(N(1, 8), "D5 C5 B4 A4")]), ev(N(1, 8), n("G4"))],
    [Irr(3, 2, [ev(N(1, 4), n("A4")), ev(N(1, 4), n("B4")), ev(N(1, 4), n("C5"))]),
     ev(N(1, 2), n("D5"))],
    [Irr(2, 3, [melodie(N(1, 8), "E5 D5")]), ev(pointee(N(1, 4)), n("C5"))],
]
FIG_EXERCICE = Figure([("", EXERCICE)], numeros=True, ligne=170)

FIGURES_GUIDE = {
    "v-notes": FIG_NOTES,
    "v-silences": FIG_SILENCES,
    "v-anatomie": FIG_ANATOMIE,
    "v-arbre": FIG_ARBRE,
    "v-point": FIG_POINT,
    "v-liaisons": FIG_LIAISONS,
    "v-point-orgue": FIG_POINT_ORGUE,
    "v-triolets": FIG_TRIOLETS,
    "v-groupes": FIG_GROUPES,
    "v-exercice": FIG_EXERCICE,
}

# Les questions : combien de la première valeur dans la seconde. « Croche de
# triolet » et « double de sextolet » sont les valeurs réelles de ces notes.
VALEUR.update({"croche de triolet": N(1, 8) * N(2, 3),
               "double croche de sextolet": N(1, 16) * N(4, 6)})
QUESTIONS = [
    ("doubles croches", "double croche", "une blanche pointée", pointee(N(1, 2))),
    ("croches", "croche", "une blanche doublement pointée", pointee(N(1, 2), 2)),
    ("triples croches", "triple croche", "une noire pointée", pointee(N(1, 4))),
    ("demi-soupirs", "demi-soupir", "un soupir pointé", pointee(N(1, 4))),
    ("quadruples croches", "quadruple croche", "une croche", N(1, 8)),
    ("croches de triolet", "croche de triolet", "une blanche", N(1, 2)),
    ("doubles croches de sextolet", "double croche de sextolet", "une blanche", N(1, 2)),
    ("soupirs", "soupir", "une pause", N(1)),
    ("noires", "noire", "une carrée", CARREE),
]


def combien(unite, total):
    q = total / VALEUR[unite]
    assert q.denominator == 1, (unite, total)
    return int(q)


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def verifier():
    # Chaque figure vaut la moitié de la précédente ; une ronde vaut 2, 4, 8…
    # 64 quadruples croches. Un crochet de plus à chaque division, à partir de
    # la croche.
    for (_, a, _), (_, b, _) in zip(FIGURES, FIGURES[1:]):
        assert a == 2 * b
    assert [int(RONDE / v) for _, v, _ in FIGURES] == [1, 2, 4, 8, 16, 32, 64]
    assert [crochets(v) for _, v, _ in FIGURES] == [0, 0, 0, 1, 2, 3, 4]

    # Le point ajoute la moitié de la valeur ; le second point, la moitié du
    # premier ajout.
    assert pointee(N(1, 2)) == 3 * N(1, 4)                  # blanche pointée : trois noires
    assert pointee(N(1, 4)) == 3 * N(1, 8)                  # noire pointée : trois croches
    assert pointee(N(1, 8)) == 3 * N(1, 16)                 # croche pointée : trois doubles
    assert pointee(N(1, 2), 2) == 7 * N(1, 8)               # blanche doublement pointée : sept croches
    assert pointee(N(1, 2), 2) == N(1, 2) + N(1, 4) + N(1, 8)
    for _, v, _ in FIGURES:
        assert pointee(v) == v + v / 2
        assert pointee(v, 2) == v + v / 2 + v / 4
        assert pointee(v, 3) == v + v / 2 + v / 4 + v / 8
    # Le triple point : une blanche triplement pointée vaut quinze doubles croches.
    assert pointee(N(1, 2), 3) == 15 * N(1, 16)

    # La carrée vaut deux rondes, le bâton de pause deux pauses ; une mesure à
    # 4/2 en contient une.
    assert CARREE == 2 * VALEUR["ronde"] and VALEUR["bâton de pause"] == 2 * VALEUR["pause"]
    assert CARREE == 4 * N(1, 2)

    # Cinq croches ne s'écrivent pas d'une seule figure : il faut une liaison.
    assert not simple(5 * N(1, 8)) and simple(6 * N(1, 8)) and simple(7 * N(1, 8))

    # Les groupes irréguliers : la durée de la division régulière qu'ils
    # remplacent, et la figure de cette division.
    assert duree(Irr(3, 2, [poutre(N(1, 8), 3)])) == N(1, 4)     # triolet de croches : une noire
    assert duree(Irr(3, 2, [ev(N(1, 4))] * 3)) == N(1, 2)        # triolet de noires : une blanche
    assert duree(Irr(6, 4, [poutre(N(1, 16), 6)])) == N(1, 4)    # sextolet de doubles : une noire
    assert duree(Irr(2, 3, [poutre(N(1, 8), 2)])) == pointee(N(1, 4))  # duolet : une noire pointée
    assert duree(Irr(4, 3, [poutre(N(1, 8), 4)])) == pointee(N(1, 4))  # quartolet : idem
    # Le duolet s'écrit aussi en deux croches pointées.
    assert 2 * pointee(N(1, 8)) == pointee(N(1, 4))
    # Une croche de triolet dure les deux tiers d'une croche.
    assert VALEUR["croche de triolet"] == N(1, 12)

    # Les portées d'une figure se correspondent, segment par segment ; dans un
    # groupe irrégulier, la figure écrite est celle de la division régulière.
    for nom, fig in FIGURES_GUIDE.items():
        if len(fig.portees) > 1:
            longueurs = {len(segs) for _, segs in fig.portees}
            assert len(longueurs) == 1, nom
            for segments in zip(*(segs for _, segs in fig.portees)):
                assert len({duree(s) for s in segments}) == 1, (nom, segments)
    for fig in (FIG_TRIOLETS, FIG_GROUPES):
        (_, regulier), (_, irregulier) = fig.portees
        for reg, (irr,) in zip(regulier, irregulier):
            ecrite = {e.valeur for e in evs(irr)}
            assert ecrite == {e.valeur for r in reg for e in evs(r)}, irr
            assert len(evs(irr)) == irr.reelles
            assert sum(len(evs(r)) for r in reg) == irr.normales

    # L'arbre : chaque étage dure une ronde.
    for _, segs in FIG_ARBRE.portees:
        assert duree(segs[0]) == RONDE

    # À la noire 60, une noire dure une seconde, une croche une demi-seconde.
    assert secondes(N(1, 4)) == 1 and secondes(N(1, 8)) == N(1, 2) and secondes(RONDE) == 4

    # L'exercice : les réponses attendues.
    assert [duree(g) / N(1, 4) for g in EXERCICE] == [4, 3, 2, N(5, 2), N(7, 2), 3, N(7, 2), 2, 4, 3]
    assert [combien(u, t) for _, u, _, t in QUESTIONS] == [12, 7, 12, 3, 8, 6, 12, 4, 8]


def secondes(valeur):
    """Durée en secondes au tempo du fichier MusicXML."""
    return valeur / N(1, 4) * N(60, TEMPO)


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
DUREES_LILY = {CARREE: r"\breve", N(1): "1", N(1, 2): "2", N(1, 4): "4", N(1, 8): "8",
               N(1, 16): "16", N(1, 32): "32", N(1, 64): "64"}
MARQUES_LILY = {"fermata": r"\fermata", "(": "(", ")": ")"}


def lily_duree(valeur):
    for base, txt in DUREES_LILY.items():
        for points in range(3):
            if base * (2 - N(1, 2 ** points)) == valeur:
                return txt + "." * points
    raise ValueError(valeur)


def ly_ev(e, cote, debut="", fin=""):
    txt = ("r" if e.note is None else e.note.lily()) + lily_duree(e.valeur) + debut + fin
    if e.liee:
        txt += "~"
    for m in e.marques:
        # Un numéro d'exercice : sous la portée, en romain.
        txt += r"_\markup \small %s" % m[4:] if m.startswith("num:") else MARQUES_LILY[m]
    if e.texte and cote:
        # Sous une note seule, le nom tient sur deux lignes : « double / croche ».
        mots = e.texte.rsplit(" ", 1)
        txt += r"%s\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { %s }" % (
            cote, " ".join(f'"{m}"' for m in mots))
    return txt


def ly_item(item, cote):
    if isinstance(item, Ev):
        return ly_ev(item, cote)
    if isinstance(item, Poutre):
        k = len(item.evs)
        return " ".join(ly_ev(e, cote, "[" if i == 0 and k > 1 else "",
                              "]" if i == k - 1 and k > 1 else "")
                        for i, e in enumerate(item.evs))
    return r"\tuplet %d/%d { %s }" % (item.reelles, item.normales,
                                      " ".join(ly_item(i, cote) for i in item.items))


def numeroter(item, k):
    """L'élément, sa première note portant le numéro `k`."""
    if isinstance(item, Ev):
        return item._replace(marques=item.marques + (f"num:{k}",))
    if isinstance(item, Poutre):
        return Poutre([numeroter(item.evs[0], k)] + list(item.evs[1:]))
    return item._replace(items=[numeroter(item.items[0], k)] + list(item.items[1:]))


def figure(fig):
    blocs = []
    nb = len(fig.portees)
    textes = any(e.texte for _, segs in fig.portees for s in segs for i in s for e in evs(i))
    # Une note par segment : le texte se place sous elle, et les notes
    # s'écartent pour lui. Sinon, le texte se place en tête du segment,
    # au-dessus du système, et les segments s'élargissent pour qu'aucun texte
    # ne chevauche le suivant.
    une_note = all(len(evs(i)) == 1 and len(s) == 1 for _, segs in fig.portees for s in segs for i in s)
    marques = []
    if textes and not une_note:
        for segs in zip(*(segs for _, segs in fig.portees)):
            t = [e.texte for s in segs for i in s for e in evs(i) if e.texte]
            marques.append(r'\textMark \markup \small \italic "%s" ' % t[0] if t else "")
    for i, (nom, segments) in enumerate(fig.portees):
        if fig.numeros:
            segments = [[numeroter(s[0], k)] + s[1:] for k, s in enumerate(segments, 1)]
        cote = None if marques else "_"
        corps = [" ".join(ly_item(it, cote) for it in s) for s in segments]
        if marques and i == 0:
            corps = [m + c for m, c in zip(marques, corps)]
        nom_portee = (r'\with { instrumentName = \markup \small \italic "%s" }' % nom
                      if nb > 1 else "")
        contexte = "RhythmicStaff" if fig.arbre else "Staff"
        reglages = [] if fig.arbre else [r"\clef treble"]
        reglages += [r"\omit Staff.TimeSignature", r"\cadenzaOn", r"\autoBeamOff", r"\tupletUp"]
        if textes and une_note:
            reglages += [r"\textLengthOn", r"\override TextScript.staff-padding = #2.5"]
        if fig.numeros:
            reglages.append(r"\override TextScript.staff-padding = #3")
        blocs.append(r"""    \new %s %s {
      %s
      %s
      \bar "|."
    }""" % (contexte, nom_portee, " ".join(reglages), r' \bar "|" '.join(corps)))
    if nb == 1:
        musique = blocs[0].strip()
    else:
        groupe = (r" \with { \override StaffGrouper.staff-staff-spacing = "
                  r"#'((basic-distance . 7) (minimum-distance . 6) (padding . 1)) }"
                  if fig.arbre else "")
        musique = "\\new StaffGroup%s <<\n" % groupe + "\n".join(blocs) + "\n  >>"
    reglages_score = [r"\override SpacingSpanner.spacing-increment = #%s" % fig.espacement,
                      r"\markLengthOn", r"\override TextMark.self-alignment-X = #LEFT"]
    if fig.arbre:
        # L'arbre se lit en colonnes : l'espace suit exactement la durée.
        reglages_score = [r"proportionalNotationDuration = #(ly:make-moment 1/24)",
                          r"\markLengthOn",
                          r"\override SpacingSpanner.uniform-stretching = ##t"]
    # Une ligne très longue : chaque figure tient sur une ligne, à sa largeur
    # naturelle, et le guide les met toutes à la même échelle.
    retrait = ("indent = 18\\mm" if nb > 1 else "") + " line-width = %d\\mm" % fig.ligne
    return r"""\score {
  %s
  \layout {
    %s
    \context { \Score %s }
  }
}
""" % (musique, retrait, " ".join(reglages_score))


# Les valeurs les plus longues : la carrée et le bâton de pause, chacun dans
# une mesure à 4/2, puis huit mesures de silence à 4/4, réunies en mesures à
# compter, avant que la musique reprenne.
MESURES_A_COMPTER = 8


def figure_longues():
    def nom(texte):
        mots = texte.rsplit(" ", 1) if " " in texte else [texte]
        return r"\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { %s }" % (
            " ".join(f'"{m}"' for m in mots))
    return r"""\score {
  \new Staff {
    \clef treble \numericTimeSignature \autoBeamOff \textLengthOn
    \override TextScript.staff-padding = #2.5
    \override MultiMeasureRestText.staff-padding = #2.5
    \time 4/2
    %s_%s | r%s_%s \bar "||"
    \time 4/4
    \compressMMRests { R1*%d_%s } | c''4 d'' e'' f'' \bar "|."
  }
  \layout { \context { \Score \override SpacingSpanner.spacing-increment = #1.6 } }
}
""" % (LA.lily() + lily_duree(CARREE), nom("carrée"), lily_duree(CARREE), nom("bâton de pause"),
       MESURES_A_COMPTER, nom("mesures à compter"))


def ecrire_gravures():
    return ([ecrire(nom, figure(fig), preambule=PREAMBULE_VALEURS)
             for nom, fig in FIGURES_GUIDE.items()]
            + [ecrire("v-longues", figure_longues(), preambule=PREAMBULE_VALEURS)])


# ---------------------------------------------------------------------------
# Tableau, questions, réponses
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_valeurs.py — ne pas modifier à la main.\n"


def frac_tex(q):
    """Une fraction positive en LaTeX : 2, 1/2 en fraction, 1 1/2 en nombre mixte."""
    q = Fraction(q)
    if q.denominator == 1:
        return str(q.numerator)
    entier, reste = divmod(q.numerator, q.denominator)
    f = r"$\frac{%d}{%d}$" % (reste, q.denominator)
    return f"{entier}\\,{f}" if entier else f


def ecrire_tableau():
    l = [ENTETE_TEX,
         r"\begin{tabular}{@{}l l c r r@{}}", r"\toprule",
         r"\textbf{Note} & \textbf{Silence} & \textbf{Crochets} & "
         r"\textbf{Dans une ronde} & \textbf{À la noire 60} \\",
         r"\midrule"]
    for nom, v, silence in FIGURES:
        l.append(f"{nom} & {silence} & {crochets(v) or '--'} & {int(RONDE / v)} & "
                 f"{frac_tex(secondes(v))}~s \\\\")
    l += [r"\bottomrule", r"\end{tabular}", ""]
    chemin = os.path.join(DIR_LY, "valeurs-tableau.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(l))
    return chemin


def en_noires(valeur):
    """Une durée en noires, en toutes lettres pour la demie : « 3 noires et demie »."""
    q = valeur / N(1, 4)
    entier, demi = divmod(q, 1)
    assert demi in (0, N(1, 2)), valeur
    txt = f"{int(entier)}~noire" + ("s" if entier > 1 else "")
    return txt + (" et demie" if demi else "")


def ecrire_questions():
    l = [ENTETE_TEX, r"\begin{multicols}{2}", r"\raggedright",
         r"\begin{enumerate}[label=\alph*)]"]
    for k, (pluriel, _, total, _) in enumerate(QUESTIONS):
        fin = "." if k == len(QUESTIONS) - 1 else "~;"
        l.append(rf"  \item {pluriel} dans {total}{fin}")
    l += [r"\end{enumerate}", r"\end{multicols}", ""]
    chemin = os.path.join(DIR_LY, "valeurs-questions.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(l))
    return chemin


def ecrire_reponses():
    groupes = "~; ".join(f"{i}~:~{en_noires(duree(g))}" for i, g in enumerate(EXERCICE, 1))
    lettres = "abcdefghij"
    questions = "~; ".join(f"{lettres[i]})~{combien(u, t)}"
                           for i, (_, u, _, t) in enumerate(QUESTIONS))
    chemin = os.path.join(DIR_LY, "valeurs-reponses.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + r"\emph{Groupes.} " + groupes + ".\n\n"
                + r"\emph{Questions.} " + questions + ".\n")
    return chemin


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
MARQUES_XML = {"fermata"}


def xml_ev(e):
    return (e.note, e.valeur, e.liee, tuple(m for m in e.marques if m in MARQUES_XML))


def xml_groupes(items):
    """Les groupes MusicXML d'une liste d'éléments : une ligature ou un groupe irrégulier par groupe."""
    res = []
    for item in items:
        if isinstance(item, Ev):
            res.append([xml_ev(item)])
        elif isinstance(item, Poutre):
            res.append([xml_ev(e) for e in item.evs])
        else:
            res.append(musicxml.Nolet(item.reelles, item.normales, [xml_ev(e) for e in evs(item)]))
    return res


def chiffrage(valeur):
    """Chiffres indicateurs d'une mesure qui dure `valeur` : 4/4, 3/8, 7/8…"""
    for unite in (4, 8, 16):
        temps = valeur * unite
        if temps.denominator == 1:
            return (int(temps), unite)
    raise ValueError(valeur)


def entree(libelle, mesures, temps=None):
    """Une entrée MusicXML, en do majeur, ses mesures toutes de même durée."""
    durees = {duree(m) for m in mesures}
    assert len(durees) == 1, libelle
    valeur = durees.pop()
    temps = temps or chiffrage(valeur)
    assert N(*temps) == valeur, libelle
    return (libelle, 0, "major", temps, [xml_groupes(m) for m in mesures])


def ecrire_musicxml():
    entrees = []
    # De la ronde à la quadruple croche, une mesure par figure.
    toutes = []
    for _, v, _ in FIGURES:
        if v >= N(1, 4):
            toutes.append([ev(v) for _ in range(int(RONDE / v))])
        else:
            toutes.append([poutre(v, int(N(1, 4) / v)) for _ in range(4)])
    entrees.append(entree("de la ronde à la quadruple croche", toutes))
    # Le point : la valeur pointée, puis la même durée sans point.
    (_, avec), (_, sans) = FIG_POINT.portees
    for a, s in zip(avec, sans):
        if all(e.note is not None for i in a for e in evs(i)):
            entrees.append(entree(f"{evs(a[0])[0].texte}, puis sans point", [a, s]))
    entrees.append(entree("liaison de prolongation, puis cinq croches",
                          [FIG_LIAISONS.portees[0][1][0], [poutre(N(1, 8), 2), poutre(N(1, 8), 3)]]))
    entrees.append(entree("point d'orgue", FIG_POINT_ORGUE.portees[0][1]))
    # Chaque division régulière, puis le groupe irrégulier qui la remplace.
    (_, reg), (_, irr) = FIG_TRIOLETS.portees
    entrees.append(entree("croches, puis triolet de croches", [reg[0] + irr[0]] * 2, (2, 4)))
    entrees.append(entree("noires, puis triolet de noires", [reg[1] + irr[1]]))
    entrees.append(entree("doubles, puis triolet de doubles",
                          [reg[2] + irr[2] + reg[2] + irr[2]], (2, 4)))
    entrees.append(entree("doubles, puis sextolet", [reg[3] + irr[3]] * 2, (2, 4)))
    (_, reg), (_, irr) = FIG_GROUPES.portees
    entrees.append(entree("croches, puis duolet", [reg[0] + irr[0]] * 2, (6, 8)))
    entrees.append(entree("croches, puis quartolet", [reg[1] + irr[1]] * 2, (6, 8)))
    entrees.append(entree("doubles, puis quintolet", [reg[2] + irr[2]] * 2, (2, 4)))
    entrees.append(entree("doubles, puis septolet", [reg[3] + irr[3]] * 2, (2, 4)))
    for k, groupe in enumerate(EXERCICE, 1):
        entrees.append(entree("l'exercice" if k == 1 else "", [groupe]))
    chemin = os.path.join(RACINE, "valeurs.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_rythmee(
            "Les valeurs",
            f"Les exemples du guide et les groupes de l'exercice, à la noire {TEMPO} : "
            "une noire par seconde.", entrees, "Piano", TEMPO))
    return chemin


if __name__ == "__main__":
    verifier()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, RACINE))
    for c in (ecrire_tableau(), ecrire_questions(), ecrire_reponses()):
        print("LaTeX :", os.path.relpath(c, RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
