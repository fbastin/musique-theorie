#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, les réponses des exercices et le fichier MusicXML du
guide « Les cadences ».

    python3 outils/generer_cadences.py

Un enchaînement y est une suite de chiffres dans une tonalité : I, IV, V7, I.
Il se réalise dans deux dispositions courantes au clavier.

- Quatre voix, deux par main — soprano et alto à la main droite, ténor et
  basse à la main gauche —, l'écriture des traités d'harmonie. Le soprano
  reste près de la tonique ; les trois autres voix bougent le moins possible ;
  le ténor peut rejoindre la basse à l'unisson ; sous la quarte et sixte, la
  basse descend à l'octave pour la dominante. C'est la disposition des
  exemples du guide.
- Le style clavier : la basse seule à la main gauche, trois sons serrés à la
  main droite, dans trois positions selon la note du soprano. Dans I–V7–I, la
  dominante reste en place, la tierce de I monte à la septième de V7, sa
  fondamentale descend à la sensible : V7 perd sa quinte, et sa fondamentale
  est doublée par la basse.

Dans les deux cas, parmi les réalisations sans faute — ni quintes ni octaves
parallèles, la sensible montant, la septième et la quarte et sixte se
résolvant en descendant —, le générateur retient celle où les voix parcourent
le moins de chemin.

Chaque enchaînement réalisé est ensuite relu à partir de ses seules notes,
comme le ferait un lecteur : les accords et leurs chiffres (analyse du guide
« Les accords »), les fautes de conduite des voix, et le nom de la cadence qui
le termine. Les affirmations du texte sont vérifiées ainsi sur les quinze
tonalités majeures et les quinze mineures, avant toute écriture.
"""

import os
import sys
from collections import namedtuple
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import TONALITES, Note, note_de
from generer import DIR_LY, PREAMBULE, RACINE, ecrire
from generer_accords import (Ton, ROMAINS, analyser_accord, chiffre, chiffre_markup,
                             degre_dans, echelle, n, nom_ton, sur_degre, tex_chiffre,
                             toutes_les_tonalites)
from intervalles import analyser
import musicxml

PREAMBULE_CADENCES = PREAMBULE.replace("outils/generer.py", "outils/generer_cadences.py")

# Dans le fichier MusicXML, chaque accord dure une blanche, à la noire 80.
TEMPO = 80
BLANCHE = Fraction(1, 2)

DO_MAJEUR = Ton(n("C4"), "majeur")
LA_MINEUR = Ton(n("A3"), "mineur")
LA_MAJEUR = Ton(n("A3"), "majeur")

# ---------------------------------------------------------------------------
# Chiffres : « V7 », « II6 », « I64 »
# ---------------------------------------------------------------------------
# Le suffixe d'un chiffre donne le nombre de sons et la position : rien pour
# un accord de trois sons à l'état fondamental, 6 et 64 pour ses renversements,
# 7, 65, 43 et 2 pour la septième et les siens.
SUFFIXES = {"": (3, 0), "6": (3, 1), "64": (3, 2),
            "7": (4, 0), "65": (4, 1), "43": (4, 2), "2": (4, 3)}
# Le chiffrage tel que l'écrit l'analyse du guide « Les accords ».
CHIFFRAGES = {(3, 0): "", (3, 1): "6", (3, 2): "6/4",
              (4, 0): "7", (4, 1): "6/5", (4, 2): "4/3", (4, 3): "2"}

Chiffre = namedtuple("Chiffre", "degre sons position")
TONIQUE = Chiffre(1, 3, 0)


def lire_chiffre(txt):
    """« II6 » -> Chiffre(2, 3, 1)."""
    i = len(txt.rstrip("0123456789"))
    romain, suffixe = txt[:i], txt[i:]
    sons, position = SUFFIXES[suffixe]
    return Chiffre(ROMAINS.index(romain) + 1, sons, position)


def lire(enchainement):
    return [lire_chiffre(x) for x in enchainement.split()]


def quarte_et_sixte(c):
    return (c.degre, c.sons, c.position) == (1, 3, 2)


def membres(ton, c):
    """Les membres de l'accord, de la fondamentale à la septième."""
    return sur_degre(ton, c.degre, c.sons)


def meme_nom(a, b):
    return a.lettre == b.lettre and a.alt == b.alt


def compte(voix, y):
    """Le nombre de voix qui portent le nom de la note `y`, à toute octave."""
    return sum(meme_nom(x, y) for x in voix)


def sensible(ton):
    return echelle(ton)[6]


def tonique(ton):
    return echelle(ton)[0]


def octaves_de(note, bas, haut):
    """La note à chaque octave comprise entre `bas` et `haut` (demi-tons, inclus)."""
    res = []
    for o in range(0, 8):
        x = Note(note.lettre, note.alt, o)
        if bas <= x.hauteur <= haut:
            res.append(x)
    return res


def pres_de(note, cible):
    """La note, à l'octave la plus proche de `cible` (demi-tons) ; plus haut si égalité."""
    return min((Note(note.lettre, note.alt, o) for o in range(0, 8)),
               key=lambda x: (abs(x.hauteur - cible), -x.hauteur))


# ---------------------------------------------------------------------------
# Conduite des voix : les fautes
# ---------------------------------------------------------------------------
def melodique(a, b):
    """(numéro, qualité) du mouvement d'une voix, ou None s'il dépasse l'octave."""
    grave, aigu = (a, b) if a.hauteur <= b.hauteur else (b, a)
    try:
        return analyser(grave, aigu)
    except ValueError:
        return None


def paralleles(avant, apres):
    """
    Les quintes et les octaves parallèles entre deux accords : deux voix qui
    bougent toutes deux et forment la même quinte juste, ou la même octave (ou
    le même unisson), avant et après. Les voix vont de la basse au soprano.
    """
    fautes = []
    for i, j in combinations(range(len(avant)), 2):
        x1, y1, x2, y2 = avant[i], avant[j], apres[i], apres[j]
        if x1.hauteur == x2.hauteur or y1.hauteur == y2.hauteur:
            continue
        d1, d2 = (y1.hauteur - x1.hauteur) % 12, (y2.hauteur - x2.hauteur) % 12
        if d1 == d2 and d1 in (0, 7):
            fautes.append(("octaves" if d1 == 0 else "quintes", i, j))
    return fautes


def fautes_enchainement(ton, c1, v1, c2, v2, sixte_vers_septieme=False):
    """
    Ce qu'un correcteur relèverait entre deux accords réalisés (basse
    comprise) : quintes ou octaves parallèles, mouvement augmenté, sensible
    qui ne monte pas à la tonique, septième qui ne descend pas, quarte et sixte
    qui ne se résout pas — la quarte et la sixte descendent d'un degré ; avec
    `sixte_vers_septieme`, la sixte peut aussi monter sur la septième d'un V7.
    """
    fautes = [f"{nom} parallèles" for nom, _, _ in paralleles(v1, v2)]
    for x, y in zip(v1, v2):
        if x.hauteur != y.hauteur:
            mvt = melodique(x, y)
            if mvt is None or mvt[1] == "augmentée":
                fautes.append(f"mouvement {x!r}–{y!r}")
    if c1.degre == 5 and c2.degre in (1, 6):
        for x, y in zip(v1, v2):
            if meme_nom(x, sensible(ton)) and not (meme_nom(y, tonique(ton))
                                                  and y.hauteur == x.hauteur + 1):
                fautes.append("sensible non résolue")
            if c1.sons == 4 and meme_nom(x, membres(ton, c1)[3]) \
                    and not 1 <= x.hauteur - y.hauteur <= 2:
                fautes.append("septième non résolue")
    if quarte_et_sixte(c1) and c2.degre == 5:
        quarte, sixte = membres(ton, c1)[0], membres(ton, c1)[1]
        septieme = membres(ton, c2)[3] if c2.sons == 4 else None
        for x, y in zip(v1, v2):
            descend = 1 <= x.hauteur - y.hauteur <= 2
            if meme_nom(x, quarte) and not descend:
                fautes.append("quarte et sixte non résolue")
            monte = (sixte_vers_septieme and septieme is not None and meme_nom(y, septieme)
                     and 1 <= y.hauteur - x.hauteur <= 2)
            if meme_nom(x, sixte) and not (descend or monte):
                fautes.append("quarte et sixte non résolue")
    return fautes


# ---------------------------------------------------------------------------
# Relecture : des notes aux chiffres, des chiffres à la cadence
# ---------------------------------------------------------------------------
Realisation = namedtuple("Realisation", "ton chiffres accords main_droite", defaults=(2,))
# `accords` : un tuple par accord, de la basse au soprano. `main_droite` : la
# première voix jouée par la main droite (2 pour deux voix par main, 1 pour le
# style clavier).


class Impasse(Exception):
    """Aucune réalisation sans faute n'existe pour cet enchaînement."""


def relire(ton, accord):
    """(degré, sons, position, chiffre romain, chiffrage) lus sur les notes seules."""
    a = analyser_accord(list(accord))
    romain, chiffrage = chiffre(ton, list(accord))
    return degre_dans(ton, a.fondamentale), a.sons, a.position, romain, chiffrage


NOMS = {"parfaite": "cadence parfaite", "imparfaite": "cadence imparfaite",
        "demi": "demi-cadence", "plagale": "cadence plagale",
        "rompue": "cadence rompue"}


def classer(ton, accords):
    """
    Le nom de la cadence qui termine l'enchaînement, d'après ses deux derniers
    accords et le tronc commun des définitions : l'arrêt sur V est une
    demi-cadence ; V–I, parfaite si les deux accords sont à l'état fondamental,
    imparfaite si l'un est renversé ; IV–I, plagale ; V–VI, rompue.
    """
    (d1, _, p1, _, _), (d2, _, p2, _, _) = (relire(ton, a) for a in accords[-2:])
    if d2 == 5:
        return "demi"
    if (d1, d2) == (5, 1):
        return "parfaite" if p1 == 0 and p2 == 0 else "imparfaite"
    if (d1, d2) == (4, 1):
        return "plagale"
    if (d1, d2) == (5, 6):
        return "rompue"
    return None


def soprano(accord):
    return accord[-1]


# ---------------------------------------------------------------------------
# Quatre voix, deux par main
# ---------------------------------------------------------------------------
# L'accord de départ est l'accord de tonique. En do majeur : do2 à la basse,
# sol2 au ténor, mi3 à l'alto, do4 au soprano (octaves à la française ; do2
# est C3 dans le modèle de hauteurs, do4 est C5). Les autres tonalités s'en
# déduisent par le plus petit transport, jusqu'à une quarte plus haut ou un
# triton plus bas, et chaque voix se tient près de sa note de départ, dans les
# fenêtres ci-dessous (en demi-tons).
FENETRES = [(-9, 9), (-8, 6), (-6, 5)]          # basse, ténor, alto
# Les mouvements permis à la basse : unisson, seconde, tierce, quarte, quinte
# et octave ; aux autres voix, une quinte au plus.
SAUTS_BASSE = {0, 1, 2, 3, 4, 5, 7, 12}


def decalage(ton):
    """Le transport de do majeur à `ton`, en demi-tons : de -6 à +5."""
    d = tonique(ton).hauteur % 12
    return d - 12 if d > 5 else d


def depart(ton):
    """L'accord de tonique de départ : basse, ténor, alto, soprano."""
    t, g = decalage(ton), echelle(ton)
    return (pres_de(g[0], -12 + t), pres_de(g[4], -5 + t),
            pres_de(g[2], 4 + t), pres_de(g[0], 12 + t))


def soprano_cible(ton, c):
    """Au soprano, le membre de l'accord le plus proche de la tonique de départ."""
    cible = depart(ton)[3].hauteur
    return min((pres_de(x, cible) for x in membres(ton, c)),
               key=lambda x: (abs(x.hauteur - cible), -x.hauteur))


def accord_permis(ton, c, voix, incomplet=False):
    """
    Les membres requis présents — tous ceux d'un accord de trois sons ; la
    fondamentale, la tierce et la septième d'un accord de septième — ; aucun
    triplé ; ni la sensible ni la septième doublées ; la quarte et sixte double
    sa basse. Avec `incomplet`, l'accord de résolution d'une septième complète
    peut perdre sa quinte et tripler sa fondamentale.
    """
    m = membres(ton, c)
    requis = m if c.sons == 3 else [m[0], m[1], m[3]]
    if incomplet:
        requis = [m[0], m[1]]
    if any(compte(voix, y) == 0 for y in requis):
        return False
    if any(compte(voix, y) > (3 if incomplet and k == 0 else 2) for k, y in enumerate(m)):
        return False
    if compte(voix, sensible(ton)) > 1:
        return False
    if c.sons == 4 and compte(voix, m[3]) > 1:
        return False
    if quarte_et_sixte(c) and compte(voix, m[2]) != 2:
        return False
    return True


def penalite_quatre(ton, c, voix, prec):
    """
    Ce que coûte le membre doublé. À l'état fondamental, la fondamentale se
    double, la quinte un peu moins bien, la tierce mal — sauf au VI qui suit
    le V, où la tierce doublée est la règle. Au premier renversement, sur I on
    double la fondamentale ; sur II, la basse, le quatrième degré, et
    nettement mieux que tout autre membre.
    """
    if c.sons == 4 or c.position == 2:
        return 0
    m = membres(ton, c)
    double = next((k for k, y in enumerate(m) if compte(voix, y) == 2), None)
    if double is None:
        return 0
    if c.degre == 6 and prec is not None and prec.degre == 5:
        return 0 if double == 1 else 2
    if c.position == 0 or c.degre == 1:
        return {0: 0, 2: 1, 1: 2}[double]
    return {1: 0, 0: 5, 2: 5}[double]


def candidats(ton, c, incomplet=False):
    """
    Les réalisations permises d'un accord, (basse, ténor, alto, soprano) : le
    soprano donné par la règle, chaque voix dans sa fenêtre, sans croisement
    (le ténor peut rejoindre la basse à l'unisson), la main droite dans une
    octave, la main gauche dans une dixième.
    """
    ref, m, s = depart(ton), membres(ton, c), soprano_cible(ton, c)
    fen = [(ref[k].hauteur + bas, ref[k].hauteur + haut) for k, (bas, haut) in enumerate(FENETRES)]
    basses = octaves_de(m[c.position], *fen[0])
    tenors = [x for y in m for x in octaves_de(y, *fen[1])]
    altos = [x for y in m for x in octaves_de(y, *fen[2])]
    res = []
    for b in basses:
        for t in tenors:
            for a in altos:
                if not b.hauteur <= t.hauteur < a.hauteur < s.hauteur:
                    continue
                if s.hauteur - a.hauteur > 12 or t.hauteur - b.hauteur > 16:
                    continue
                voix = (b, t, a, s)
                if accord_permis(ton, c, voix, incomplet):
                    res.append(voix)
    return res


def fautes_quatre(ton, c1, v1, c2, v2):
    """Les fautes d'un enchaînement à deux voix par main, sauts compris."""
    fautes = fautes_enchainement(ton, c1, v1, c2, v2)
    if abs(v2[0].hauteur - v1[0].hauteur) not in SAUTS_BASSE:
        fautes.append(f"saut de basse {v1[0]!r}–{v2[0]!r}")
    for x, y in zip(v1[1:], v2[1:]):
        if abs(y.hauteur - x.hauteur) > 7:
            fautes.append(f"saut {x!r}–{y!r}")
    return fautes


def octave_sous_la_quarte_et_sixte(c1, v1, c2, v2):
    """Sous la quarte et sixte, la basse descend à l'octave pour la dominante."""
    return not (quarte_et_sixte(c1) and c2.degre == 5) or v2[0].hauteur == v1[0].hauteur - 12


def cout_quatre(v1, v2):
    """
    Le chemin parcouru par les quatre voix, en demi-tons, et un peu pour
    l'écart de la main gauche : à chemin presque égal, la basse reste près du
    ténor.
    """
    return (sum(abs(y.hauteur - x.hauteur) for x, y in zip(v1, v2))
            + 0.1 * (v2[1].hauteur - v2[0].hauteur))


def realiser(ton, enchainement):
    """
    La réalisation de `enchainement` à quatre voix, deux par main. Le premier accord,
    s'il est un I, est l'accord de départ ; sinon, l'enchaînement part de cet
    accord de départ, qu'on retire ensuite. La suite est, parmi les
    réalisations sans faute, celle où les voix parcourent le moins de chemin.
    """
    chiffres = lire(enchainement)
    virtuel = chiffres[0] != TONIQUE
    suite = ([TONIQUE] if virtuel else []) + chiffres
    d = depart(ton)
    chemins = {d: (0, [d])}
    for c1, c2 in zip(suite, suite[1:]):
        suivants = {}
        # Après une septième de dominante, l'accord de résolution peut perdre
        # sa quinte, si la septième était complète.
        apres_septieme = c1.sons == 4 and c2.sons == 3
        for v2 in candidats(ton, c2, apres_septieme):
            sans_quinte = apres_septieme and compte(v2, membres(ton, c2)[2]) == 0
            meilleur = None
            for v1, (prix, chemin) in chemins.items():
                if not octave_sous_la_quarte_et_sixte(c1, v1, c2, v2):
                    continue
                if sans_quinte and compte(v1, membres(ton, c1)[2]) == 0:
                    continue
                if fautes_quatre(ton, c1, v1, c2, v2):
                    continue
                total = prix + cout_quatre(v1, v2) + penalite_quatre(ton, c2, v2, c1)
                if meilleur is None or total < meilleur[0] - 1e-9:
                    meilleur = (total, chemin + [v2])
            if meilleur:
                suivants[v2] = meilleur
        if not suivants:
            raise Impasse(nom_ton(ton), enchainement)
        chemins = suivants
    _, chemin = min(chemins.values(), key=lambda pc: pc[0])
    return Realisation(ton, chiffres, chemin[1:] if virtuel else chemin)


def fautes(r):
    """Toutes les fautes d'une réalisation à deux voix par main, accord par accord."""
    res = []
    for (c1, v1), (c2, v2) in zip(zip(r.chiffres, r.accords), zip(r.chiffres[1:], r.accords[1:])):
        res += fautes_quatre(r.ton, c1, v1, c2, v2)
    return res


def degres(r):
    """
    Le dessin d'une réalisation, indépendant de la tonalité : pour chaque voix
    de chaque accord, son degré (1 à 7) et son écart à la note de départ de la
    même voix, en octaves de la gamme.
    """
    ref = depart(r.ton)
    t = tonique(r.ton)
    res = []
    for a in r.accords:
        res.append(tuple(((x.idx - t.idx) % 7 + 1, (x.idx + 7 * x.octave - ref[k].idx - 7 * ref[k].octave))
                         for k, x in enumerate(a)))
    return res


# ---------------------------------------------------------------------------
# Le style clavier : trois sons à la main droite, la basse seule
# ---------------------------------------------------------------------------
# La basse seule à la main gauche ; à la main droite, trois sons serrés dont le
# premier accord fixe le soprano : sa fondamentale (position d'octave), sa
# tierce ou sa quinte. La tonique de la basse se place entre ré2 et do dièse 3
# du modèle de hauteurs ; chaque autre note de la basse, d'un ton sous cette
# tonique à une sixte majeure au-dessus.
RE2, DO_DIESE3 = Note("D", 0, 2).hauteur, Note("C", 1, 3).hauteur
MI3, SI5 = Note("E", 0, 3).hauteur, Note("B", 0, 5).hauteur
POSITIONS = ["position d'octave", "position de tierce", "position de quinte"]


def placer_a(note, bas, haut):
    """La note, à l'octave qui la met entre `bas` et `haut` (demi-tons, inclus)."""
    return octaves_de(note, bas, haut)[0]


def basse_clavier(ton, c):
    t = placer_a(tonique(ton), RE2, DO_DIESE3).hauteur
    return placer_a(membres(ton, c)[c.position], t - 2, t + 9)


def possibles_clavier(ton, c, apres_septieme=False):
    """
    Les réalisations de la main droite : trois sons différents, dans une
    octave, au-dessus de la basse ; avec la basse, tous les membres de
    l'accord — la quinte d'une septième peut manquer —, aucun doublé deux fois,
    ni la sensible ni la septième doublées. Après une septième complète,
    l'accord de résolution peut perdre sa quinte et tripler sa fondamentale.
    """
    m = membres(ton, c)
    b = basse_clavier(ton, c)
    notes = sorted((x for y in m for x in octaves_de(y, max(MI3, b.hauteur + 1), SI5)),
                   key=lambda x: x.hauteur)
    incomplet = apres_septieme and c.sons == 3
    requis = [m[0], m[1]] + ([m[3]] if c.sons == 4 else [] if incomplet else [m[2]])
    res = []
    for trio in combinations(notes, 3):
        h = [x.hauteur for x in trio]
        if not (h[0] < h[1] < h[2] and h[2] - h[0] <= 12):
            continue
        voix = (b,) + trio
        if any(compte(voix, y) == 0 for y in requis):
            continue
        if any(compte(voix, y) > (3 if incomplet and k == 0 else 2) for k, y in enumerate(m)):
            continue
        if compte(voix, sensible(ton)) > 1 or (c.sons == 4 and compte(voix, m[3]) > 1):
            continue
        res.append(trio)
    return res


def penalite_clavier(ton, c, trio):
    """La fondamentale ou la basse doublées ne coûtent rien, la quinte un peu, la tierce plus."""
    m = membres(ton, c)
    voix = (basse_clavier(ton, c),) + trio
    if c.sons == 3 and not any(meme_nom(x, m[2]) for x in voix):
        return 2
    for k, y in enumerate(m):
        if compte(voix, y) == 2:
            return 0 if k in (0, c.position) else 2 if k == 1 else 1
    return 0


def cout_clavier(ton, c2, v1, v2):
    """
    Le chemin parcouru par la main droite, plus une pénalité pour chaque note
    commune abandonnée et un rien pour chaque voix qui suit la basse.
    """
    total = 0
    m2 = membres(ton, c2)
    for x, y in zip(v1[1:], v2[1:]):
        d = y.hauteur - x.hauteur
        if abs(d) > 8:
            return None
        total += abs(d)
        if d and any(meme_nom(x, z) for z in m2):
            total += 3
        if d and v2[0].hauteur != v1[0].hauteur and (d > 0) == (v2[0].hauteur > v1[0].hauteur):
            total += 0.1
    return total


def realiser_clavier(ton, enchainement, position=0):
    """
    La réalisation en style clavier : chaque accord est un tuple (basse, voix 1,
    voix 2, voix 3). Le premier accord est complet et serré, avec au soprano sa
    fondamentale (position 0, d'octave), sa tierce (1) ou sa quinte (2), la
    voix la plus grave entre la3 et sol dièse 4 du modèle de hauteurs.
    """
    chiffres = lire(enchainement)
    c0, m0 = chiffres[0], membres(ton, chiffres[0])
    la3, la4 = Note("A", 0, 3).hauteur, Note("A", 0, 4).hauteur
    departs = [t for t in possibles_clavier(ton, c0)
               if meme_nom(t[2], m0[position]) and la3 <= t[0].hauteur < la4
               and all(any(meme_nom(x, y) for x in t) for y in m0[:3])]
    b0 = basse_clavier(ton, c0)
    chemins = {t: (penalite_clavier(ton, c0, t), [(b0,) + t]) for t in departs}
    for c1, c2 in zip(chiffres, chiffres[1:]):
        b2 = basse_clavier(ton, c2)
        suivants = {}
        for t2 in possibles_clavier(ton, c2, apres_septieme=c1.sons == 4):
            v2 = (b2,) + t2
            meilleur = None
            for prix, chemin in chemins.values():
                v1 = chemin[-1]
                if fautes_enchainement(ton, c1, v1, c2, v2):
                    continue
                c = cout_clavier(ton, c2, v1, v2)
                if c is None:
                    continue
                total = prix + c + penalite_clavier(ton, c2, t2)
                if meilleur is None or total < meilleur[0]:
                    meilleur = (total, chemin + [v2])
            if meilleur:
                suivants[t2] = meilleur
        if not suivants:
            raise Impasse(nom_ton(ton), enchainement, position)
        chemins = suivants
    _, chemin = min(chemins.values(), key=lambda pc: pc[0])
    return Realisation(ton, chiffres, chemin, 1)


def membre_au_soprano(ton, c, accord):
    """0 si le soprano porte la fondamentale, 1 la tierce, 2 la quinte."""
    return next(k for k, x in enumerate(membres(ton, c)) if meme_nom(x, soprano(accord)))


# ---------------------------------------------------------------------------
# Les enchaînements du guide
# ---------------------------------------------------------------------------
# Des enchaînements courants, avec la cadence qui termine chacun ; ceux des
# exemples et des exercices s'y ajoutent. Tous sont réalisés et relus dans les
# trente tonalités.
FORMULES_COURANTES = {
    "I IV V7 I": "parfaite",
    "II6 I64 V7 I": "parfaite",
    "I IV V VI": "rompue",
    "II6 I64 V VI": "rompue",
    "I IV II6 V": "demi",
    "I II6 V I6": "imparfaite",
}
AUTRES = {
    "I V": "demi",
    "I IV V": "demi",
    "I II6 V": "demi",
    "I II6 I64 V": "demi",
    "I IV V I": "parfaite",
    "I V7 I": "parfaite",
    "I II6 V I": "parfaite",
    "II6 I64 V I": "parfaite",
    "I V I6": "imparfaite",
    "I IV I": "plagale",
    "I IV V7 VI": "rompue",
    "IV V": "demi",
}

# Le style clavier : I–V7–I en position d'octave, en do majeur, en la majeur et
# en la mineur, et I–IV–V–I en do majeur dans les trois positions. La basse,
# puis la main droite, accord par accord : les exemples gravés, que la
# réalisation doit donner exactement.
CLAVIER_ATTENDU = {
    (DO_MAJEUR, "I V7 I", 0): ["C3 E4 G4 C5", "G3 F4 G4 B4", "C3 E4 G4 C5"],
    (LA_MAJEUR, "I V7 I", 0): ["A2 C#4 E4 A4", "E3 D4 E4 G#4", "A2 C#4 E4 A4"],
    (LA_MINEUR, "I V7 I", 0): ["A2 C4 E4 A4", "E3 D4 E4 G#4", "A2 C4 E4 A4"],
    (DO_MAJEUR, "I IV V I", 0): ["C3 E4 G4 C5", "F3 F4 A4 C5", "G3 D4 G4 B4", "C3 E4 G4 C5"],
    (DO_MAJEUR, "I IV V I", 1): ["C3 G4 C5 E5", "F3 A4 C5 F5", "G3 G4 B4 D5", "C3 G4 C5 E5"],
    (DO_MAJEUR, "I IV V I", 2): ["C3 C4 E4 G4", "F3 C4 F4 A4", "G3 B3 D4 G4", "C3 C4 E4 G4"],
}

Exemple = namedtuple("Exemple", "ton enchainement titre", defaults=("",))


def ton(txt, mode):
    return Ton(n(txt), mode)


SOL_MAJEUR, RE_MAJEUR, FA_MAJEUR = ton("G4", "majeur"), ton("D4", "majeur"), ton("F4", "majeur")
SIB_MAJEUR, RE_MINEUR, MI_MINEUR = ton("Bb4", "majeur"), ton("D4", "mineur"), ton("E4", "mineur")
DO_MINEUR = ton("C4", "mineur")

PHRASE = [Exemple(DO_MAJEUR, "I IV V", "demi-cadence"),
          Exemple(DO_MAJEUR, "I IV V7 I", "cadence parfaite")]
PARFAITE = [Exemple(DO_MAJEUR, "I IV V I", "avec V"),
            Exemple(DO_MAJEUR, "I IV V7 I", "avec V7")]
IMPARFAITE = [Exemple(DO_MAJEUR, "I V I6", "depuis I"),
              Exemple(DO_MAJEUR, "I II6 V I6", "depuis II6")]
PLAGALE = [Exemple(DO_MAJEUR, "I IV I", "plagale")]
DEMI = [Exemple(DO_MAJEUR, "I V", "depuis I"),
        Exemple(DO_MAJEUR, "I IV V", "depuis IV"),
        Exemple(DO_MAJEUR, "I IV II6 V", "depuis II6")]
ROMPUE = [Exemple(DO_MAJEUR, "I IV V VI", "depuis IV"),
          Exemple(DO_MAJEUR, "II6 I64 V VI", "depuis la quarte et sixte")]
MINEUR = [Exemple(LA_MINEUR, "I IV V7 I", "parfaite"),
          Exemple(LA_MINEUR, "I IV V VI", "rompue")]
PREPARER = [Exemple(DO_MAJEUR, "I II6 V I", "")]
QUARTE_SIXTE = [Exemple(DO_MAJEUR, "II6 I64 V I", "vers V"),
                Exemple(DO_MAJEUR, "II6 I64 V7 I", "vers V7")]
COURANTES_RE = [Exemple(RE_MAJEUR, f) for f in FORMULES_COURANTES]
DISPOSITION = [Exemple(DO_MAJEUR, "I IV V7 I", "do majeur"),
               Exemple(SIB_MAJEUR, "I IV V7 I", "si bémol majeur"),
               Exemple(RE_MINEUR, "I IV V7 I", "ré mineur")]

# IV–V réalisé en suivant la basse : les trois voix du dessus montent avec
# elle, quintes et octaves parallèles.
FAUTIF = Realisation(DO_MAJEUR, lire("IV V"),
                     [tuple(n(x) for x in "F3 A3 F4 C5".split()),
                      tuple(n(x) for x in "G3 B3 G4 D5".split())])

# Exercice 1 : reconnaître la cadence.
RECONNAITRE = [
    Exemple(RE_MAJEUR, "I IV V7 I"),
    Exemple(FA_MAJEUR, "I V I6"),
    Exemple(SOL_MAJEUR, "I IV I"),
    Exemple(MI_MINEUR, "I IV V VI"),
    Exemple(SIB_MAJEUR, "I II6 V"),
    Exemple(DO_MINEUR, "II6 I64 V7 I"),
]
# Exercice 2 : réaliser. La première basse en style clavier, en position de
# tierce ; les deux autres à quatre voix, deux par main.
REALISER_CLAVIER = (SOL_MAJEUR, "I V7 I", 1)
REALISER = [
    Exemple(RE_MINEUR, "II6 I64 V VI"),
    Exemple(FA_MAJEUR, "I II6 V I6"),
]
# Exercice 3 : à l'oreille, dans le fichier MusicXML.
ECOUTER = [
    Exemple(SOL_MAJEUR, "II6 I64 V7 I"),
    Exemple(RE_MINEUR, "I IV V VI"),
    Exemple(FA_MAJEUR, "I II6 V I6"),
    Exemple(MI_MINEUR, "I IV II6 V"),
    Exemple(SIB_MAJEUR, "I IV I"),
    Exemple(LA_MINEUR, "I IV V7 I"),
]


def realisation(e):
    return realiser(e.ton, e.enchainement)


# ---------------------------------------------------------------------------
# Vérifications
# ---------------------------------------------------------------------------
def verifier_realisation(r, attendu):
    """Ce que le texte affirme de toute réalisation à quatre voix, deux par main."""
    ton = r.ton
    assert not fautes(r), (nom_ton(ton), r.chiffres, fautes(r))
    assert classer(ton, r.accords) == attendu, (nom_ton(ton), r.chiffres)
    for c, a in zip(r.chiffres, r.accords):
        # Relu sur ses notes, chaque accord redonne son chiffre.
        d, sons, pos, _, chiffrage = relire(ton, a)
        assert (d, sons, pos) == tuple(c), (nom_ton(ton), r.chiffres, c)
        assert chiffrage == CHIFFRAGES[(c.sons, c.position)]
        b, t, al, s = a
        # Deux voix par main : la droite dans une octave, la gauche dans une
        # dixième ; le ténor peut rejoindre la basse, jamais la croiser.
        assert b.hauteur <= t.hauteur < al.hauteur < s.hauteur
        assert s.hauteur - al.hauteur <= 12 and t.hauteur - b.hauteur <= 16
        # Le soprano reste près de la tonique : la tonique sur I, IV et VI, le
        # deuxième degré sur II, la sensible sur V.
        attendu_soprano = {1: 0, 4: 0, 6: 0, 2: 1, 5: 6}[c.degre]
        assert meme_nom(s, echelle(ton)[attendu_soprano]), (nom_ton(ton), r.chiffres, c)
    for (c1, v1), (c2, v2) in zip(zip(r.chiffres, r.accords), zip(r.chiffres[1:], r.accords[1:])):
        if c1.degre == 5 and c2.degre in (1, 6):
            for x, y in zip(v1, v2):
                # La sensible monte à la tonique, la septième descend d'un degré.
                if meme_nom(x, sensible(ton)):
                    assert meme_nom(y, tonique(ton)) and y.hauteur == x.hauteur + 1
                if c1.sons == 4 and meme_nom(x, membres(ton, c1)[3]):
                    assert 1 <= x.hauteur - y.hauteur <= 2 and (y.idx - x.idx) % 7 == 6
        if quarte_et_sixte(c1):
            # La quarte et sixte se résout sur V : la quarte descend sur la
            # tierce de V, la sixte sur sa quinte ; la basse descend à
            # l'octave ; avant V7, la basse doublée descend sur la septième.
            assert c2.degre == 5 and v2[0].hauteur == v1[0].hauteur - 12
            m1, m2 = membres(ton, c1), membres(ton, c2)
            for x, y in zip(v1[1:], v2[1:]):
                if meme_nom(x, m1[0]):
                    assert meme_nom(y, m2[1]) and 1 <= x.hauteur - y.hauteur <= 2
                if meme_nom(x, m1[1]):
                    assert meme_nom(y, m2[2]) and 1 <= x.hauteur - y.hauteur <= 2
                if c2.sons == 4 and meme_nom(x, m1[2]) and not meme_nom(y, m2[0]):
                    assert meme_nom(y, m2[3]) and 1 <= x.hauteur - y.hauteur <= 2
        # La quarte et sixte double sa basse.
        if quarte_et_sixte(c2):
            assert compte(v2, v2[0]) == 2
        # VI après V : la tierce est doublée.
        if c1.degre == 5 and c2.degre == 6:
            assert compte(v2, membres(ton, c2)[1]) == 2
        # IV ou II6 avant V : la basse monte d'un ton.
        if c2.degre == 5 and (c1.degre, c1.position) in ((4, 0), (2, 1)):
            assert v2[0].hauteur - v1[0].hauteur == 2


def verifier_clavier(r, p):
    """Ce que le texte affirme du style clavier, en position `p`."""
    ton_ = r.ton
    for (c1, v1), (c2, v2) in zip(zip(r.chiffres, r.accords), zip(r.chiffres[1:], r.accords[1:])):
        assert not fautes_enchainement(ton_, c1, v1, c2, v2), (nom_ton(ton_), r.chiffres, p)
        # La note commune reste en place.
        communes = [x for x in membres(ton_, c1) if any(meme_nom(x, y) for y in membres(ton_, c2))]
        for x, y in zip(v1[1:], v2[1:]):
            if any(meme_nom(x, z) for z in communes):
                assert x.hauteur == y.hauteur, (nom_ton(ton_), r.chiffres, p)
        # De IV à V, sans note commune, les trois voix descendent quand la
        # basse monte.
        if (c1.degre, c2.degre) == (4, 5):
            assert not communes and v2[0].hauteur > v1[0].hauteur
            assert all(y.hauteur < x.hauteur for x, y in zip(v1[1:], v2[1:]))
    for c, a in zip(r.chiffres, r.accords):
        m = membres(ton_, c)
        # La main droite serrée, au-dessus de la basse, qui porte la fondamentale.
        assert a[3].hauteur - a[1].hauteur <= 12 and a[0].hauteur < a[1].hauteur
        assert meme_nom(a[0], m[0])
        if c.sons == 4:
            # V7 : la quinte omise, la fondamentale doublée par la basse.
            assert compte(a, m[2]) == 0 and compte(a, m[0]) == 2
    # L'accord final est complet, et la cadence revient à sa position de départ.
    assert all(compte(r.accords[-1], y) >= 1 for y in membres(ton_, r.chiffres[-1]))
    assert membre_au_soprano(ton_, r.chiffres[0], r.accords[0]) == p
    assert membre_au_soprano(ton_, r.chiffres[-1], r.accords[-1]) == p
    assert classer(ton_, r.accords) == "parfaite"


def verifier():
    for ton_ in toutes_les_tonalites():
        dessins = {}
        for enchainement, attendu in list(FORMULES_COURANTES.items()) + list(AUTRES.items()):
            r = realiser(ton_, enchainement)
            verifier_realisation(r, attendu)
            dessins[enchainement] = degres(r)
        # Le même dessin dans toutes les tonalités du même mode : chaque voix
        # garde son degré et son octave relative. Transposer, c'est tout
        # déplacer d'un même intervalle.
        reference = DO_MAJEUR if ton_.mode == "majeur" else LA_MINEUR
        for enchainement in dessins:
            assert dessins[enchainement] == degres(realiser(reference, enchainement)), \
                (nom_ton(ton_), enchainement)
        # Le style clavier : I–V7–I et I–IV–V–I, dans les trois positions.
        for enchainement in ("I V7 I", "I IV V I"):
            for p in range(3):
                verifier_clavier(realiser_clavier(ton_, enchainement, p), p)

    # Les exemples du style clavier : exactement les accords gravés.
    for (ton_, enchainement, p), attendu in CLAVIER_ATTENDU.items():
        r = realiser_clavier(ton_, enchainement, p)
        assert [" ".join(repr(x) for x in a) for a in r.accords] == attendu, \
            (nom_ton(ton_), enchainement, p)
    # La majeur et la mineur, homonymes : le même V7 ; des accords de tonique
    # qui ne diffèrent que par leur tierce, do dièse ou do.
    majeur, mineur = (realiser_clavier(t, "I V7 I") for t in (LA_MAJEUR, LA_MINEUR))
    assert [repr(x) for x in majeur.accords[1]] == [repr(x) for x in mineur.accords[1]]
    for k in (0, 2):
        ecarts = [(x, y) for x, y in zip(majeur.accords[k], mineur.accords[k]) if repr(x) != repr(y)]
        assert ecarts and all(x.lettre == y.lettre == "C" and (x.alt, y.alt) == (1, 0)
                              for x, y in ecarts), k

    # Ce qu'en dit le texte, à quatre voix : venu de IV, V7 perd sa quinte, et
    # le ténor rejoint la basse ; sous la quarte et sixte, la basse descend à
    # l'octave, et avant V7 la basse doublée descend sur la septième.
    r = realiser(DO_MAJEUR, "I IV V7 I")
    assert r.accords[2][0].hauteur == r.accords[2][1].hauteur
    assert compte(r.accords[2], n("D4")) == 0 and compte(r.accords[2], n("G4")) == 2
    r = realiser(DO_MAJEUR, "II6 I64 V7 I")
    assert r.accords[2][0].hauteur == r.accords[1][0].hauteur - 12
    assert [repr(x) for x in r.accords[1][1:]] == ["G3", "E4", "C5"]
    assert [repr(x) for x in r.accords[2][1:]] == ["F3", "D4", "B4"]
    r = realiser(DO_MAJEUR, "II6 I64 V I")
    assert [repr(x) for x in r.accords[2]][2] == "D4"

    # IV–V en suivant la basse : quintes et octaves parallèles ; la
    # réalisation retenue n'en a aucune.
    assert {"quintes parallèles", "octaves parallèles"} <= set(fautes(FAUTIF))
    juste = realiser(DO_MAJEUR, "IV V")
    assert not fautes(juste)
    assert [repr(x) for x in juste.accords[1]] == ["G3", "G3", "D4", "B4"]

    # Les exemples et les exercices portent le nom attendu.
    groupes = ((PHRASE, ["demi", "parfaite"]), (PARFAITE, ["parfaite"] * 2),
               (IMPARFAITE, ["imparfaite"] * 2), (PLAGALE, ["plagale"]),
               (DEMI, ["demi"] * 3), (ROMPUE, ["rompue"] * 2),
               (MINEUR, ["parfaite", "rompue"]), (PREPARER, ["parfaite"]),
               (QUARTE_SIXTE, ["parfaite"] * 2), (DISPOSITION, ["parfaite"] * 3),
               (RECONNAITRE, ["parfaite", "imparfaite", "plagale", "rompue", "demi",
                              "parfaite"]),
               (REALISER, ["rompue", "imparfaite"]),
               (ECOUTER, ["parfaite", "rompue", "imparfaite", "demi", "plagale",
                          "parfaite"]))
    for groupe, noms in groupes:
        assert [classer(e.ton, realisation(e).accords) for e in groupe] == noms
    verifier_clavier(realiser_clavier(*REALISER_CLAVIER), REALISER_CLAVIER[2])

    # Les tableaux : chaque tonalité usuelle a sa case, une seule fois ; les
    # cases vides sont exactement les six tonalités dont l'armure dépasserait
    # sept altérations ; chaque case se réalise sans faute, dans les trois
    # positions, et revient à sa position de départ.
    cases, vides = [], []
    for tonique, majeur, mineur in lignes_tableau():
        for ton_, mode in ((majeur, "majeur"), (mineur, "mineur")):
            if ton_ is None:
                vides.append((tonique, mode))
                continue
            cases.append((tonique, mode))
            for enchainement in TABLEAUX.values():
                for p in range(3):
                    verifier_clavier(realiser_clavier(ton_, enchainement, p), p)
    usuelles = ({(maj, "majeur") for _, maj, _ in TONALITES}
                | {(mi, "mineur") for _, _, mi in TONALITES})
    assert len(cases) == len(set(cases)) == 30 and set(cases) == usuelles
    assert set(vides) == {("G#", "majeur"), ("D#", "majeur"), ("A#", "majeur"),
                          ("Db", "mineur"), ("Gb", "mineur"), ("Cb", "mineur")}


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def ly_cle(ton):
    """\\key do \\major : la tonique sans marque d'octave."""
    return r"\key %s \%s" % (tonique(ton).lily().rstrip("',"),
                             "major" if ton.mode == "majeur" else "minor")


def ly_accord(notes, duree):
    return "<" + " ".join(x.lily() for x in notes) + ">" + duree


def chiffres_markup(r):
    return [chiffre_markup(*relire(r.ton, a)[3:]) for a in r.accords]


def titre_markup(texte):
    """Un titre au-dessus d'un accord ; « V7 » ou « II6 » y prennent leur chiffre en exposant."""
    mots = []
    for mot in texte.split(" "):
        i = len(mot.rstrip("0123456789"))
        if i < len(mot) and mot[:i] in ROMAINS:
            mots.append(r'"%s" \super "%s"' % (mot[:i], mot[i:]))
        else:
            mots.append('"%s"' % mot)
    espaces = r' " " '.join(mots)
    return r"\markup \small \italic \concat { %s }" % espaces


def syllabe(texte):
    """Une légende sous un accord : un markup tel quel, sinon un texte entre guillemets."""
    return texte if texte.startswith("\\markup") else '"%s"' % texte


MISE_EN_PAGE = r"""  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
      \override SpacingSpanner.spacing-increment = #%.1f
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }"""

ENTETE_PORTEE = (r"\accidentalStyle forget \set Staff.printKeyCancellation = ##f "
                 r"\omit Staff.TimeSignature \cadenzaOn")


def systeme(groupes, dessus=None, sous=None, mains=True, chiffres=True, espacement=1.5):
    """
    Des enchaînements à deux voix par main, en blanches, deux accords par
    mesure, séparés par une double barre : soprano et alto en clé de sol, hampes
    opposées, ténor et basse en clé de fa. Sous la basse, les chiffres, sauf si
    `chiffres` est faux ; `sous` : une seconde ligne de légendes. `dessus` : un
    texte au-dessus du premier accord de chaque groupe. Sans `mains`, seule la
    basse est écrite : c'est l'énoncé d'un exercice à réaliser.
    """
    voix = [[], [], [], []]                     # soprano, alto, ténor, basse
    paroles = []
    for i, r in enumerate(groupes):
        cle = ly_cle(r.ton)
        for k in range(4):
            voix[k].append(cle)
        for j, a in enumerate(r.accords):
            b, t, al, s = a
            notes = [s, al, t, b]
            for k in range(4):
                visible = mains or k == 3
                voix[k].append(notes[k].lily() + "2" if visible else "s2")
            if j == 0 and dessus and dessus[i]:
                voix[0][-1] += "^" + titre_markup(dessus[i])
            if j % 2 == 1 and j < len(r.accords) - 1:
                for k in range(4):
                    voix[k].append(r'\bar "|"')
        paroles += chiffres_markup(r)
        if i < len(groupes) - 1:
            for k in range(4):
                voix[k].append(r'\bar "||"')
    lignes = []
    if chiffres:
        lignes.append(r'    \new Lyrics \lyricsto "basse" { %s }' % " ".join(paroles))
    if sous:
        lignes.append(r'    \new Lyrics \lyricsto "basse" { %s }' % " ".join(syllabe(t) for t in sous))
    s, al, t, b = (" ".join(v) for v in voix)
    return r"""\score {
  \new PianoStaff <<
    \new Staff <<
      \clef treble
      \new Voice { \voiceOne %s %s \bar "|." }
      \new Voice { \voiceTwo %s %s }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne %s %s }
      \new Voice = "basse" { \voiceTwo %s %s \bar "|." }
    >>
%s
  >>
%s
}
""" % (ENTETE_PORTEE, s, ENTETE_PORTEE, al, ENTETE_PORTEE, t, ENTETE_PORTEE, b,
       "\n".join(lignes), MISE_EN_PAGE % espacement)


def systeme_clavier(groupes, dessus, mains=True, espacement=1.9):
    """
    Le style clavier : trois sons à la main droite, la basse seule, en rondes.
    Sans `mains`, la main droite est laissée vide (énoncé d'exercice).
    """
    haut, bas, paroles = [], [], []
    for i, r in enumerate(groupes):
        cle = ly_cle(r.ton)
        haut.append(cle)
        bas.append(cle)
        for k, a in enumerate(r.accords):
            txt = ly_accord(a[1:], "1") if mains else "s1"
            if k == 0 and dessus[i]:
                txt += "^" + titre_markup(dessus[i])
            haut.append(txt)
            bas.append(a[0].lily() + "1")
        paroles += chiffres_markup(r)
        if i < len(groupes) - 1:
            haut.append(r'\bar "||"')
            bas.append(r'\bar "||"')
    return r"""\score {
  \new PianoStaff <<
    \new Staff { \clef treble %s %s \bar "|." }
    \new Staff = "bas" { \clef bass %s \new Voice = "basse" { %s \bar "|." } }
    \new Lyrics \lyricsto "basse" { %s }
  >>
%s
}
""" % (ENTETE_PORTEE, " ".join(haut), ENTETE_PORTEE, " ".join(bas), " ".join(paroles),
       (MISE_EN_PAGE % espacement).replace("1/4", "1/2"))


def figure(exemples, **kw):
    return systeme([realisation(e) for e in exemples],
                   dessus=[e.titre for e in exemples], **kw)


def figure_quarte_sixte():
    groupes = [realisation(e) for e in QUARTE_SIXTE]
    # Au-dessus de la basse, sol : la quarte et sixte, puis 5/3 ou 7/5/3.
    pile = lambda *c: (r"\markup \fontsize #-1 \override #'(baseline-skip . 1.7) "
                       r"\center-column { %s }" % " ".join('"%s"' % x for x in c))
    sous = [" ", pile("6", "4"), pile("5", "3"), " ", " ", pile("6", "4"), pile("7", "5", "3"), " "]
    return systeme(groupes, dessus=[e.titre for e in QUARTE_SIXTE], sous=sous)


def figure_exercice(items, debut, mains, chiffres):
    groupes = [realisation(e) for e in items]
    dessus = [f"{k} — {nom_ton(e.ton)}" for k, e in enumerate(items, start=debut)]
    return systeme(groupes, dessus=dessus, mains=mains, chiffres=chiffres, espacement=1.3)


def figure_clavier_exercice(mains):
    """La basse à réaliser en style clavier, puis sa réponse."""
    ton_, enchainement, p = REALISER_CLAVIER
    return systeme_clavier([realiser_clavier(ton_, enchainement, p)],
                           [f"1 — {nom_ton(ton_)}"], mains=mains, espacement=1.6)


FIGURES = {
    "ca-phrase": lambda: figure(PHRASE),
    "ca-parfaite": lambda: figure(PARFAITE),
    "ca-imparfaite": lambda: figure(IMPARFAITE),
    "ca-plagale": lambda: figure(PLAGALE),
    "ca-demi": lambda: figure(DEMI, espacement=1.3),
    "ca-rompue": lambda: figure(ROMPUE),
    "ca-mineur": lambda: figure(MINEUR),
    "ca-preparer": lambda: figure(PREPARER),
    "ca-quarte-sixte": figure_quarte_sixte,
    "ca-courantes-1": lambda: figure(COURANTES_RE[:3], espacement=1.3),
    "ca-courantes-2": lambda: figure(COURANTES_RE[3:], espacement=1.3),
    "ca-disposition": lambda: figure(DISPOSITION, espacement=1.3),
    "ca-paralleles": lambda: systeme([FAUTIF, realiser(DO_MAJEUR, "IV V")],
                                     dessus=["fautif", "correct"]),
    "ca-clavier-v7": lambda: systeme_clavier(
        [realiser_clavier(t, "I V7 I") for t in (DO_MAJEUR, LA_MAJEUR, LA_MINEUR)],
        [nom_ton(t) for t in (DO_MAJEUR, LA_MAJEUR, LA_MINEUR)]),
    "ca-clavier-positions": lambda: systeme_clavier(
        [realiser_clavier(DO_MAJEUR, "I IV V I", p) for p in range(3)], POSITIONS),
    "ca-exercice-1": lambda: figure_exercice(RECONNAITRE[:3], 1, True, False),
    "ca-exercice-2": lambda: figure_exercice(RECONNAITRE[3:], 4, True, False),
    "ca-exercice-realiser-1": lambda: figure_clavier_exercice(False),
    "ca-exercice-realiser-2": lambda: figure_exercice(REALISER, 2, False, True),
    "ca-reponse-realiser-1": lambda: figure_clavier_exercice(True),
    "ca-reponse-realiser-2": lambda: figure_exercice(REALISER, 2, True, True),
}


def ecrire_gravures():
    return [ecrire(nom, fabrique(), preambule=PREAMBULE_CADENCES)
            for nom, fabrique in FIGURES.items()]


ENTETE_TEX = "%% Produit par outils/generer_cadences.py — ne pas modifier à la main.\n"


# ---------------------------------------------------------------------------
# Les tableaux : le style clavier dans toutes les tonalités
# ---------------------------------------------------------------------------
# Une ligne par tonique, dans l'ordre du cycle des quintes, les dièses puis les
# bémols. Sur chaque ligne, le majeur dans ses trois positions, puis le mineur
# homonyme dans les siennes, quand leur armure compte au plus sept altérations.
TONIQUES = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#",
            "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]
TABLEAUX = {"iv": "I IV V I", "v7": "I V7 I"}


def lignes_tableau():
    """(tonique, ton majeur ou None, ton mineur ou None), ligne par ligne."""
    majeurs = {maj for _, maj, _ in TONALITES}
    mineurs = {mi for _, _, mi in TONALITES}
    for t in TONIQUES:
        yield (t, Ton(note_de(t, 4), "majeur") if t in majeurs else None,
               Ton(note_de(t, 4), "mineur") if t in mineurs else None)


def nom_fichier(tonique):
    """« F# » -> « fa-diese »."""
    return note_de(tonique, 4).nom_fr().replace("è", "e").replace("é", "e").replace(" ", "-")


# Une ligne de tableau : toute la largeur du texte du guide (166 mm), à une
# taille de portée réduite ; la ligne est justifiée, si bien que toutes les
# lignes ont la même largeur et la même échelle.
PREAMBULE_TABLEAU = r"""\version "2.24.3"
%% Fichier produit par outils/generer_cadences.py — ne pas modifier à la main.
#(set-global-staff-size 13)
\paper {
  indent = 0
  ragged-right = ##f
  paper-width = 168\mm
  line-width = 166\mm
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
"""


def ligne_tableau(enchainement, tonique, majeur, mineur):
    """
    Une ligne : le majeur dans ses trois positions, puis le mineur homonyme,
    en rondes, la main droite en clé de sol, la basse en clé de fa. Deux lignes
    de légendes au-dessus, alignées : la tonalité au début de chaque mode, la
    position au début de chaque groupe. Une tonalité absente garde sa place,
    occupée par des notes invisibles.
    """
    nombre = len(lire(enchainement))
    haut, bas, noms, positions = [], [], [], []
    texte = lambda t: r'\markup \tiny \italic "%s"' % t
    for k, (ton_, mode) in enumerate(((majeur, "majeur"), (mineur, "mineur"))):
        if k:
            haut.append(r'\bar "||"')
            bas.append(r'\bar "||"')
        for p in range(3):
            if p:
                haut.append(r'\bar "|"')
                bas.append(r'\bar "|"')
            noms += [texte(f"{note_de(tonique, 4).nom_fr()} {mode}") if p == 0 else "_"]
            noms += ["_"] * (nombre - 1)
            positions += [texte(("octave", "tierce", "quinte")[p]) if ton_
                          else texte("—") if p == 0 else "_"]
            positions += ["_"] * (nombre - 1)
            if ton_ is None:
                haut.append(r"\hideNotes " + " ".join(["c''1"] * nombre) + r" \unHideNotes")
                bas.append(r"\hideNotes " + " ".join(["c1"] * nombre) + r" \unHideNotes")
                continue
            r = realiser_clavier(ton_, enchainement, p)
            cle = ly_cle(ton_) if p == 0 else ""
            haut.append(cle + " " + " ".join(ly_accord(a[1:], "1") for a in r.accords))
            bas.append(cle + " " + " ".join(a[0].lily() + "1" for a in r.accords))
    return r"""\score {
  \new PianoStaff <<
    \new Lyrics = "noms"
    \new Lyrics = "positions"
    \new Staff = "haut" { \clef treble %s \new Voice = "md" { %s \bar "|." } }
    \new Staff { \clef bass %s %s \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { %s }
    \context Lyrics = "positions" \lyricsto "md" { %s }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #1.0
    }
    \context {
      \Lyrics
      \override LyricText.self-alignment-X = #LEFT
      \override LyricText.extra-spacing-width = #'(+inf.0 . -inf.0)
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #0.2
      \override VerticalAxisGroup.nonstaff-nonstaff-spacing.padding = #0.1
    }
  }
}
""" % (ENTETE_PORTEE, " ".join(haut), ENTETE_PORTEE, " ".join(bas), " ".join(noms),
       " ".join(positions))


def ecrire_tableaux():
    """Les lignes gravées des deux tableaux, et le fichier LaTeX de chacun."""
    chemins = []
    for code, enchainement in TABLEAUX.items():
        lignes = []
        for tonique, majeur, mineur in lignes_tableau():
            nom = f"ca-tab-{code}-{nom_fichier(tonique)}"
            chemins.append(ecrire(nom, ligne_tableau(enchainement, tonique, majeur, mineur),
                                  preambule=PREAMBULE_TABLEAU))
            lignes.append(r"\noindent\includegraphics[width=\linewidth]{%s.cropped.pdf}\par"
                          r"\medskip" % nom)
        chemin = os.path.join(DIR_LY, f"cadences-tableau-{code}.tex")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(ENTETE_TEX + "\n".join(lignes) + "\n")
        chemins.append(chemin)
    return chemins


# ---------------------------------------------------------------------------
# Réponses
# ---------------------------------------------------------------------------


def tex_enchainement(r):
    return "--".join(tex_chiffre(*relire(r.ton, a)[3:]) for a in r.accords)


def ecrire_reponses():
    l = [r"\textbf{Reconnaître.}"]
    l.append(r"\begin{enumerate}[leftmargin=*, itemsep=1pt]")
    for e in RECONNAITRE:
        r = realisation(e)
        l.append(rf"  \item {tex_enchainement(r)}~: {NOMS[classer(e.ton, r.accords)]}.")
    l.append(r"\end{enumerate}")
    l.append(r"\textbf{Écouter.} " + "~; ".join(
        rf"{k}~: {tex_enchainement(realisation(e))}, en {nom_ton(e.ton)}"
        rf" ({NOMS[classer(e.ton, realisation(e).accords)]})"
        for k, e in enumerate(ECOUTER, start=1)) + ".")
    chemin = os.path.join(DIR_LY, "cadences-reponses.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + "\n".join(l) + "\n")
    return chemin


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
def sans_doublon(notes):
    """Les notes d'une main, l'unisson compté une fois : le piano n'a qu'une touche."""
    res = []
    for x in notes:
        if all(x.hauteur != y.hauteur for y in res):
            res.append(x)
    return res


def mesures_piano(r):
    """Les accords en blanches, deux par mesure à 2/2 ; un dernier accord seul tient la mesure."""
    k = r.main_droite
    mains = [(sans_doublon(a[k:]), sans_doublon(a[:k])) for a in r.accords]
    mesures = []
    for i in range(0, len(mains), 2):
        paire = mains[i:i + 2]
        valeur = BLANCHE if len(paire) == 2 else 2 * BLANCHE
        mesures.append(([(d, valeur) for d, _ in paire], [(g, valeur) for _, g in paire]))
    return mesures


def armure(ton_):
    """L'armure de la tonalité, signée : dièses positifs, bémols négatifs."""
    for k, maj, mineur in TONALITES:
        t = note_de(maj if ton_.mode == "majeur" else mineur)
        if meme_nom(t, tonique(ton_)):
            return k
    raise ValueError(ton_)


def entree(libelle, r):
    return (libelle, armure(r.ton), "major" if r.ton.mode == "majeur" else "minor",
            (2, 2), mesures_piano(r))


def ecrire_musicxml():
    entrees = []
    for groupe in (PHRASE, PARFAITE, IMPARFAITE, PLAGALE, DEMI, ROMPUE, MINEUR,
                   PREPARER, QUARTE_SIXTE, COURANTES_RE, DISPOSITION):
        for e in groupe:
            r = realisation(e)
            libelle = f"{NOMS[classer(e.ton, r.accords)]}, {nom_ton(e.ton)} ({e.enchainement})"
            entrees.append(entree(libelle, r))
    for (ton_, enchainement, p) in CLAVIER_ATTENDU:
        r = realiser_clavier(ton_, enchainement, p)
        entrees.append(entree(f"style clavier, {nom_ton(ton_)} ({enchainement}), {POSITIONS[p]}", r))
    for k, e in enumerate(ECOUTER, start=1):
        entrees.append(entree(f"Écoute {k}", realisation(e)))
    chemin = os.path.join(RACINE, "cadences.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_piano(
            "Les cadences",
            "Les enchaînements du guide à quatre voix, deux par main ; les exemples du "
            "style clavier, trois sons à la main droite ; puis les six enchaînements de "
            f"l'exercice d'écoute ; un accord par blanche, à la noire {TEMPO}.",
            entrees, "Piano", TEMPO))
    return chemin


def ecrire_musicxml_tonalites():
    """
    I–IV–V–I et I–V7–I en style clavier, position d'octave, dans les trente
    tonalités, dans l'ordre des tableaux : le majeur, puis le mineur homonyme.
    """
    entrees = []
    for tonique, majeur, mineur in lignes_tableau():
        for ton_ in (majeur, mineur):
            if ton_ is None:
                continue
            for enchainement in TABLEAUX.values():
                r = realiser_clavier(ton_, enchainement)
                entrees.append(entree(f"{nom_ton(ton_)}, {enchainement.replace(' ', '–')}", r))
    chemin = os.path.join(RACINE, "cadences-tonalites.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_piano(
            "Les cadences dans toutes les tonalités",
            "I–IV–V–I et I–V7–I en style clavier, trois sons à la main droite et la "
            "basse seule, en position d'octave, dans les trente tonalités : chaque "
            f"majeur, puis son homonyme mineur ; un accord par blanche, à la noire {TEMPO}.",
            entrees, "Piano", TEMPO))
    return chemin


if __name__ == "__main__":
    verifier()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures() + ecrire_tableaux():
        print("LilyPond :" if c.endswith(".ly") else "LaTeX :", os.path.relpath(c, RACINE))
    print("LaTeX :", os.path.relpath(ecrire_reponses(), RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml_tonalites(), RACINE))
