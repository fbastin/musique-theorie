#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, les tableaux, les exercices, leurs réponses et le fichier
MusicXML du guide « La mesure ».

    python3 outils/generer_mesure.py

Une mesure y est un chiffre indicateur, dont tout le reste se déduit : simple,
composée ou irrégulière, le nombre de temps, l'unité de temps et l'unité de
mesure, la mesure correspondante, la force de chaque temps et de chaque partie
de temps. Les tableaux du guide, les noms placés sous les temps, la
reconnaissance des syncopes et des contretemps et les réponses des exercices en
dérivent ; les affirmations du texte sont vérifiées avant toute écriture.
"""

import os
import re
import sys
from collections import namedtuple
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import Note
from generer import DIR_LY, PREAMBULE, RACINE, ecrire
import musicxml
from musicxml import Nolet

# Une ligne de 150 mm : à l'échelle commune des gravures du guide (1,1), elle
# tient dans la colonne ; un exercice plus long passe à la ligne. Largeur de page,
# marges et ligne doivent s'accorder, sans quoi LilyPond revient à ses valeurs
# par défaut.
PREAMBULE_MESURE = (PREAMBULE.replace("outils/generer.py", "outils/generer_mesure.py")
                    .replace("  indent = 0\n", "  indent = 0\n  paper-width = 152\\mm\n"
                             "  line-width = 150\\mm\n"))
TEMPO = 80
N = Fraction

# ---------------------------------------------------------------------------
# Les figures
# ---------------------------------------------------------------------------
FIGURES = {N(1): "ronde", N(1, 2): "blanche", N(1, 4): "noire", N(1, 8): "croche",
           N(1, 16): "double croche", N(1, 32): "triple croche"}
NOMBRES = {1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six",
           7: "sept", 8: "huit", 9: "neuf", 12: "douze"}


def figure(valeur):
    """Nom de la figure qui vaut `valeur` (en fraction de ronde), pointée au besoin, ou None."""
    for base, nom in FIGURES.items():
        if base == valeur:
            return nom
        if base * N(3, 2) == valeur:
            return nom + " pointée"
    return None


# ---------------------------------------------------------------------------
# Modèle : le chiffre indicateur
# ---------------------------------------------------------------------------
class Chiffre(namedtuple("Chiffre", "haut bas")):
    """
    Un chiffre indicateur. Dans une mesure simple, le chiffre du haut compte les
    temps et celui du bas nomme la figure qui vaut un temps ; dans une mesure
    composée, ils comptent et nomment les divisions du temps, trois par temps.
    """
    __slots__ = ()

    def __str__(self):
        return f"{self.haut}/{self.bas}"

    @property
    def duree(self):
        return N(self.haut, self.bas)

    @property
    def genre(self):
        if self.haut in (2, 3, 4):
            return "simple"
        if self.haut % 3 == 0:
            return "composée"
        return "irrégulière"

    @property
    def temps(self):
        return {"simple": self.haut, "composée": self.haut // 3}[self.genre]

    @property
    def unite_temps(self):
        """Ce que dure un temps : la figure du bas, ou trois d'entre elles."""
        return N(1, self.bas) * (3 if self.genre == "composée" else 1)

    @property
    def division(self):
        """La figure qui divise le temps : en deux s'il est binaire, en trois s'il est ternaire."""
        return self.unite_temps / (3 if self.genre == "composée" else 2)

    @property
    def unite_mesure(self):
        """
        La figure qui remplit la mesure à elle seule ; à défaut, deux figures
        liées, chacune d'un nombre entier de temps.
        """
        if figure(self.duree):
            return figure(self.duree)
        for k in range(self.temps - 1, 0, -1):
            a, b = self.unite_temps * k, self.duree - self.unite_temps * k
            if figure(a) and figure(b):
                return f"{figure(a)} liée à une {figure(b)}"
        raise ValueError(self)

    def correspondante(self):
        """La mesure de même nombre de temps et de l'autre division."""
        if self.genre == "simple":
            return Chiffre(self.haut * 3, self.bas * 2)
        return Chiffre(self.haut // 3, self.bas // 2)

    def niveaux(self):
        """
        Les grilles de la mesure, de la plus forte à la plus faible : la mesure,
        la demi-mesure dans une mesure à quatre temps, le temps, puis ses
        divisions et leurs moitiés.
        """
        l = [self.duree]
        if self.temps == 4:
            l.append(self.duree / 2)
        l.append(self.unite_temps)
        d = self.division
        while d >= N(1, 64):
            l.append(d)
            d /= 2
        return l

    def force(self, position):
        """0 pour le temps fort, plus grand pour plus faible : la première grille qui porte la position."""
        for k, grille in enumerate(self.niveaux()):
            if position % grille == 0:
                return k
        return len(self.niveaux())

    def nom_temps(self, i):
        """« fort », « mi-fort » ou « faible », pour le temps i (compté de 0)."""
        k = self.force(i * self.unite_temps)
        if k == 0:
            return "fort"
        return "mi-fort" if self.temps == 4 and k == 1 else "faible"


C = Chiffre

# ---------------------------------------------------------------------------
# Les notes : une petite écriture, lue par `lire`
# ---------------------------------------------------------------------------
# « C5/4 » : do5 noire (octaves du modèle, 4 pour celle du do central, le do3
# des noms français) ; « r/8 » : un demi-soupir ; un point après la valeur la
# pointe. Suffixes : « ~ » lie à la note suivante, « > » accentue, « * »
# numérote la note pour un exercice. Les crochets réunissent des notes sous une
# poutre ; « 3:2[ … ] » en fait un triolet (trois pour deux). « | » sépare les
# mesures, « || » finit la mesure sur une double barre.
E = namedtuple("E", "note valeur liee accent numerote")

JETON = re.compile(r"\d+:\d+\[|\[|\]|\|\||\||[^\s\[\]|]+")
NOTE = re.compile(r"^(?P<h>[A-G][#b]*\d|r)/(?P<v>\d+)(?P<p>\.?)(?P<s>[~>*]*)$")


def n(txt):
    """« C5 », « F#4 » -> Note, octaves du modèle (4 : celle du do central)."""
    lettre, alt, octave = txt[0], txt[1:-1].count("#") - txt[1:-1].count("b"), int(txt[-1])
    return Note(lettre, alt, octave)


def element(jeton):
    m = NOTE.match(jeton)
    assert m, jeton
    valeur = N(1, int(m["v"])) * (N(3, 2) if m["p"] else 1)
    note = None if m["h"] == "r" else n(m["h"])
    return E(note, valeur, "~" in m["s"], ">" in m["s"], "*" in m["s"])


Mesure = namedtuple("Mesure", "groupes double")


def lire(texte):
    """Le texte d'un exemple -> liste de Mesure (groupes, double barre à la fin)."""
    mesures, groupes, courant = [], [], None
    for jeton in JETON.findall(texte):
        if jeton in ("|", "||"):
            mesures.append(Mesure(groupes, jeton == "||"))
            groupes = []
        elif jeton.endswith("["):
            courant = (tuple(map(int, jeton[:-1].split(":"))) if ":" in jeton else None, [])
        elif jeton == "]":
            nolet, notes = courant
            groupes.append(Nolet(nolet[0], nolet[1], notes) if nolet else notes)
            courant = None
        elif courant is not None:
            courant[1].append(element(jeton))
        else:
            groupes.append([element(jeton)])
    if groupes:
        mesures.append(Mesure(groupes, False))
    return mesures


def notes_du(groupe):
    return groupe.notes if isinstance(groupe, Nolet) else groupe


def rapport(groupe):
    return N(groupe.normales, groupe.reelles) if isinstance(groupe, Nolet) else 1


def duree(mesure):
    """Durée réelle d'une mesure : un triolet de croches vaut une noire."""
    return sum(e.valeur * rapport(g) for g in mesure.groupes for e in notes_du(g))


def evenements(mesures, debut=0):
    """(attaque, durée réelle, élément) de chaque note et silence, depuis `debut`."""
    t, res = N(debut), []
    for mesure in mesures:
        for g in mesure.groupes:
            for e in notes_du(g):
                d = e.valeur * rapport(g)
                res.append((t, d, e))
                t += d
    return res


# ---------------------------------------------------------------------------
# Syncope et contretemps
# ---------------------------------------------------------------------------
def attaques(chiffre, mesures, debut=0):
    """
    Les sons attaqués, chacun avec la durée de ses notes liées, et ce qui les
    précède : liste de (attaque, durée, élément, précédent), le précédent
    étant (attaque, durée, élément) ou None.
    """
    ev = evenements(mesures, debut)
    res, i = [], 0
    while i < len(ev):
        t, d, e = ev[i]
        j = i
        while ev[j][2].liee:
            j += 1
            d += ev[j][1]
        res.append((t, d, e, ev[i - 1] if i else None))
        i = j + 1
    return res


def classer(chiffre, t, d, e, precedent):
    """
    « syncope » : un son attaqué sur un temps faible ou la partie faible d'un
    temps, et prolongé sur un temps ou une partie de temps plus fort.
    « contretemps » : un son attaqué sur un temps faible ou la partie faible
    d'un temps, après un silence placé sur le temps ou la partie plus forte.
    None sinon. Un silence n'est ni l'un ni l'autre.
    """
    if e.note is None:
        return None
    k = chiffre.force(t % chiffre.duree)
    if k == 0:
        return None
    plus_fort = chiffre.niveaux()[k - 1]
    # Le premier point plus fort après l'attaque tombe-t-il pendant le son ?
    suivant = (t // plus_fort + 1) * plus_fort
    if suivant < t + d:
        return "syncope"
    if precedent is not None:
        tp, dp, ep = precedent
        point = (t // plus_fort) * plus_fort
        if ep.note is None and tp <= point < tp + dp:
            return "contretemps"
    return None


def classement(chiffre, mesures, debut=0):
    """Le classement de chaque note attaquée (silences exclus) : liste de (élément, classe)."""
    return [(e, classer(chiffre, t, d, e, p)) for t, d, e, p in attaques(chiffre, mesures, debut)
            if e.note is not None]


# ---------------------------------------------------------------------------
# Une mesure sans chiffre : quels chiffres admet-elle ?
# ---------------------------------------------------------------------------
def admet(mesure, chiffre):
    """
    Vrai si la mesure s'écrit ainsi dans ce chiffre, selon l'usage : la durée
    juste ; chaque groupe sous une poutre tient dans un temps, ou commence et
    finit sur des temps ; une note ou un silence plus court qu'un temps n'en
    franchit pas le début ; plus long, il commence sur un temps.
    """
    if duree(mesure) != chiffre.duree:
        return False
    u = chiffre.unite_temps
    t = N(0)
    for g in mesure.groupes:
        notes = notes_du(g)
        fin = t + sum(e.valeur for e in notes) * rapport(g)
        if len(notes) > 1:
            dans_un_temps = t // u == (fin - N(1, 1024)) // u
            if not dans_un_temps and (t % u or fin % u):
                return False
        else:
            if fin - t <= u:
                if t // u != (fin - N(1, 1024)) // u:
                    return False
            elif t % u:
                return False
        t = fin
    return True


# ---------------------------------------------------------------------------
# Les exemples
# ---------------------------------------------------------------------------
# Une figure : le texte des notes, le chiffre de chaque mesure (un seul pour
# toutes, ou une liste), et ce qu'on écrit autour :
#   comptes   — le numéro de chaque temps sous la portée ;
#   forces    — « fort », « faible » ou « mi-fort » sous chaque temps ;
#   anacrouse — la première mesure est incomplète ;
#   classes   — « syncope » ou « contretemps » au-dessus des notes concernées ;
#   textes    — un texte au-dessus de la première note de certaines mesures ;
#   symbole   — les chiffres 4/4 et 2/2 en C et C barré ;
#   numeros   — « mesures » : chaque mesure numérotée, sans chiffre indicateur ;
#               « notes » : les notes marquées d'un « * », numérotées dessous.
Figure = namedtuple("Figure", "texte chiffres comptes forces anacrouse classes textes symbole numeros",
                    defaults=(False, False, False, False, None, False, None))

FIGURES_GUIDE = {
    # Le temps, la mesure, les barres : une mélodie à 4/4.
    "me-temps": Figure("C5/4 [E5/8 D5/8] C5/4 G4/4 | A4/4 B4/4 C5/2 || E5/4 D5/4 C5/2",
                       C(4, 4), comptes=True),
    "me-simples": Figure("C5/4 D5/4 | C5/4 D5/4 E5/4 | C5/4 D5/4 E5/4 F5/4 | C5/2 D5/2"
                         " | [C5/8 D5/8 E5/8]",
                         [C(2, 4), C(3, 4), C(4, 4), C(2, 2), C(3, 8)], comptes=True),
    "me-c": Figure("C5/4 D5/4 E5/4 F5/4 | G5/2 E5/2", [C(4, 4), C(2, 2)], symbole=True),
    "me-forts": Figure("C5/4 D5/4 | C5/4 D5/4 E5/4 | C5/4 D5/4 E5/4 F5/4",
                       [C(2, 4), C(3, 4), C(4, 4)], forces=True),
    "me-anacrouse": Figure("G4/4 | C5/4 C5/4 D5/4 | E5/2 D5/4 | C5/4 B4/4 A4/4 | G4/2",
                           C(3, 4), comptes=True, anacrouse=True),
    "me-composees": Figure("[C5/8 D5/8 E5/8] [F5/8 E5/8 D5/8]"
                           " | [C5/8 D5/8 E5/8] [F5/8 G5/8 A5/8] [G5/8 F5/8 E5/8]"
                           " | C5/4. D5/4. E5/4. C5/4.",
                           [C(6, 8), C(9, 8), C(12, 8)], comptes=True),
    # La sicilienne : croche pointée, double croche, croche, dans chaque temps.
    "me-sicilienne": Figure("[E5/8. F5/16 E5/8] [D5/8. E5/16 C5/8] | D5/4. r/4.",
                            C(6, 8), comptes=True),
    "me-correspondances": Figure("[C5/8 D5/8] [E5/8 F5/8] | [C5/8 D5/8 E5/8] [F5/8 E5/8 D5/8]"
                                 " | 3:2[C5/8 D5/8 E5/8] 3:2[F5/8 E5/8 D5/8]"
                                 " | 2:3[C5/8 D5/8] 2:3[E5/8 F5/8]",
                                 [C(2, 4), C(6, 8), C(2, 4), C(6, 8)], comptes=True),
    # L'hémiole : aux deuxième et troisième mesures, trois blanches accentuées.
    "me-hemiole": Figure("C5/4 E5/4 D5/4 | C5/2> D5/4~> | D5/4 B4/2> | C5/2.",
                         C(3, 4), comptes=True),
    "me-syncopes": Figure("C5/8 D5/4 E5/8 F5/4 G5/4~ | G5/4 A5/2 G5/4", C(4, 4), classes=True),
    "me-syncopettes": Figure("[C5/16 D5/8 C5/16] [E5/16 F5/8 E5/16] | G5/2", C(2, 4), classes=True),
    "me-contretemps": Figure("r/8 C5/8 r/8 D5/8 | r/4 E5/4 | r/8 F5/8 G5/4 | C5/2",
                             C(2, 4), classes=True),
    "me-irregulieres": Figure("C5/4> D5/4 E5/4 F5/4> G5/4"
                              " | [C5/8> D5/8] [E5/8> F5/8] [G5/8> F5/8 E5/8]"
                              " | [C5/8> D5/8 E5/8] [F5/8> E5/8] [D5/8> C5/8]",
                              [C(5, 4), C(7, 8), C(7, 8)],
                              textes={0: "3 + 2", 1: "2 + 2 + 3", 2: "3 + 2 + 2"}),
}

# Les syncopes et contretemps qu'affirment les légendes, dans l'ordre des notes.
CLASSES_ATTENDUES = {
    "me-syncopes": [None, "syncope", None, None, "syncope", "syncope", None],
    "me-syncopettes": [None, "syncope", None, None, "syncope", None, None],
    "me-contretemps": ["contretemps", "contretemps", "contretemps", "contretemps", None, None],
}

# Groupements des mesures irrégulières, en unités de la figure du bas.
GROUPEMENTS = {0: (3, 2), 1: (2, 2, 3), 2: (3, 2, 2)}

# ---------------------------------------------------------------------------
# Les exercices
# ---------------------------------------------------------------------------
# Premier exercice : des chiffres indicateurs à lire.
EXERCICE_CHIFFRES = [C(3, 4), C(6, 8), C(2, 2), C(12, 8), C(9, 8), C(4, 4), C(6, 4), C(2, 4)]

# Deuxième exercice : des mesures sans chiffre, à reconnaître parmi ceux-ci.
CANDIDATS = [C(2, 4), C(3, 4), C(4, 4), C(3, 8), C(6, 8), C(9, 8), C(12, 8)]
EXERCICE_MESURES = Figure(
    "[E5/8 D5/8 C5/8] D5/4."
    " | G4/4 [A4/8 B4/8] [C5/8 D5/8]"
    " | A4/4 [G4/8 F4/8]"
    " | G4/4. A4/4 G4/8 F4/4."
    " | C5/4 [D5/8 E5/8] F5/4 G5/4"
    " | [E5/8 F5/8 G5/8] A5/4. [G5/8 F5/8 E5/8] D5/4."
    " | r/4 C5/4 C5/4"
    " | [C5/8 D5/8 E5/8] F5/4 r/8"
    " | [G4/8 A4/8 B4/8]",
    [C(6, 8), C(3, 4), C(2, 4), C(9, 8), C(4, 4), C(12, 8), C(3, 4), C(6, 8), C(3, 8)],
    numeros="mesures")

# Troisième exercice : syncope, contretemps, ou ni l'un ni l'autre ?
EXERCICE_SYNCOPES = Figure(
    "C5/4 [D5/8* E5/8*~] [E5/8 D5/8] C5/4"
    " | r/8 G4/8* [A4/8 B4/8] C5/2*"
    " | E5/4 D5/2* C5/4"
    " | r/4 B4/4* r/8 D5/8* C5/4*~"
    " | C5/2 B4/4 C5/4"
    " | [E5/16 F5/8* E5/16] D5/4 C5/2",
    C(4, 4), numeros="notes")
REPONSES_SYNCOPES = [None, "syncope", "contretemps", None, "syncope", "contretemps",
                     "contretemps", "syncope", "syncope"]


def chiffres_de(fig, mesures):
    return fig.chiffres if isinstance(fig.chiffres, list) else [fig.chiffres] * len(mesures)


def debut_de(fig, mesures):
    """Attaque de la première note : avant le premier temps fort s'il y a une anacrouse."""
    if not fig.anacrouse:
        return 0
    return -duree(mesures[0])


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def verifier():
    # Le chiffre du bas nomme la figure par le nombre qu'il en faut pour une ronde.
    assert [figure(N(1, b)) for b in (1, 2, 4, 8, 16)] == \
        ["ronde", "blanche", "noire", "croche", "double croche"]

    # Les mesures simples : nombre de temps, unité de temps, unité de mesure.
    simples = {C(2, 4): (2, "noire", "blanche"), C(3, 4): (3, "noire", "blanche pointée"),
               C(4, 4): (4, "noire", "ronde"), C(2, 2): (2, "blanche", "ronde"),
               C(3, 8): (3, "croche", "noire pointée")}
    for c, attendu in simples.items():
        assert c.genre == "simple"
        assert (c.temps, figure(c.unite_temps), c.unite_mesure) == attendu, c
        # Le temps binaire se divise en deux.
        assert c.division * 2 == c.unite_temps
    # 4/4 et 2/2 durent autant ; les temps de 2/2 sont deux fois plus longs.
    assert C(4, 4).duree == C(2, 2).duree and C(2, 2).unite_temps == 2 * C(4, 4).unite_temps

    # Les mesures composées : le chiffre du haut compte les divisions, trois par temps.
    composees = {C(6, 8): (2, "noire pointée", "croche", "blanche pointée"),
                 C(9, 8): (3, "noire pointée", "croche", "blanche pointée liée à une noire pointée"),
                 C(12, 8): (4, "noire pointée", "croche", "ronde pointée"),
                 C(6, 4): (2, "blanche pointée", "noire", "ronde pointée")}
    for c, attendu in composees.items():
        assert c.genre == "composée"
        assert (c.temps, figure(c.unite_temps), figure(c.division), c.unite_mesure) == attendu, c
        assert c.haut == 3 * c.temps and c.division * 3 == c.unite_temps
    # Aucune figure seule ne remplit une mesure à 9/8.
    assert figure(C(9, 8).duree) is None

    # Les correspondances : même nombre de temps ; l'unité de temps composée est
    # l'unité simple pointée ; on multiplie le haut par 3, le bas par 2.
    for simple, composee in CORRESPONDANCES:
        assert simple.correspondante() == composee and composee.correspondante() == simple
        assert simple.temps == composee.temps
        assert composee.unite_temps == simple.unite_temps * N(3, 2)
        assert figure(composee.unite_temps) == figure(simple.unite_temps) + " pointée"
    # La mesure à 6/8 vaut une fois et demie la mesure à 2/4.
    assert C(6, 8).duree == N(3, 2) * C(2, 4).duree

    # Temps forts et faibles.
    noms = lambda c: [c.nom_temps(i) for i in range(c.temps)]
    assert noms(C(2, 4)) == ["fort", "faible"]
    assert noms(C(3, 4)) == ["fort", "faible", "faible"]
    assert noms(C(4, 4)) == ["fort", "faible", "mi-fort", "faible"]
    assert noms(C(6, 8)) == ["fort", "faible"] and noms(C(9, 8)) == ["fort", "faible", "faible"]
    assert noms(C(12, 8)) == ["fort", "faible", "mi-fort", "faible"]
    # La partie faible d'un temps est plus faible que le temps qui suit ; en
    # 6/8, les deux dernières croches d'un temps sont aussi faibles l'une que l'autre.
    deux = C(2, 4)
    assert deux.force(N(1, 8)) > deux.force(N(1, 4)) > deux.force(0)
    six = C(6, 8)
    assert six.force(N(1, 8)) == six.force(N(2, 8)) > six.force(N(3, 8)) > six.force(0)

    # Chaque mesure est complète ; l'anacrouse et la dernière mesure en font une à elles deux.
    for nom_figure, fig in list(FIGURES_GUIDE.items()) + [("me-exercice-mesures", EXERCICE_MESURES),
                                                           ("me-exercice-syncopes", EXERCICE_SYNCOPES)]:
        mesures = lire(fig.texte)
        chiffres = chiffres_de(fig, mesures)
        assert len(chiffres) == len(mesures), nom_figure
        for i, (m, c) in enumerate(zip(mesures, chiffres)):
            if fig.anacrouse and i in (0, len(mesures) - 1):
                continue
            assert duree(m) == c.duree, (nom_figure, i)
        if fig.anacrouse:
            assert duree(mesures[0]) + duree(mesures[-1]) == chiffres[0].duree
        # Chaque mesure d'exemple s'écrit selon l'usage dans son chiffre.
        if not fig.anacrouse and not fig.classes and fig.numeros != "notes":
            for m, c in zip(mesures, chiffres):
                if c.genre != "irrégulière":
                    assert admet(m, c), (nom_figure, c)

    # Les mesures irrégulières : les groupements remplissent la mesure, en temps inégaux.
    irr = lire(FIGURES_GUIDE["me-irregulieres"].texte)
    for i, groupement in GROUPEMENTS.items():
        c = FIGURES_GUIDE["me-irregulieres"].chiffres[i]
        assert c.genre == "irrégulière" and sum(groupement) == c.haut
        assert len(set(groupement)) == 2
        # Un accent au début de chaque groupe, et seulement là.
        ev = evenements([irr[i]])
        debuts = {sum(groupement[:k]) * N(1, c.bas) for k in range(len(groupement))}
        assert {t for t, _, e in ev if e.accent} == debuts, i

    # Triolet et duolet : un triolet de croches à 2/4 attaque ses notes aux mêmes
    # fractions du temps qu'une mesure à 6/8 ; un duolet à 6/8, qu'une mesure à 2/4.
    corr = lire(FIGURES_GUIDE["me-correspondances"].texte)
    proportions = lambda m: [t / duree(m) for t, _, _ in evenements([m])]
    assert proportions(corr[2]) == proportions(corr[1])
    assert proportions(corr[3]) == proportions(corr[0])

    # La sicilienne : croche pointée, double croche, croche, qui remplissent
    # un temps ternaire ; le temps binaire de 2/4 ne l'accueille pas.
    sic = lire(FIGURES_GUIDE["me-sicilienne"].texte)
    for g in sic[0].groupes:
        assert [e.valeur for e in notes_du(g)] == [N(3, 16), N(1, 16), N(1, 8)]
        assert sum(e.valeur for e in notes_du(g)) == C(6, 8).unite_temps
        assert sum(e.valeur for e in notes_du(g)) != C(2, 4).unite_temps

    # La syncopette : double croche, croche, double croche, dans un temps
    # binaire ; la croche est une syncope, prolongée sur le milieu du temps.
    for g in lire(FIGURES_GUIDE["me-syncopettes"].texte)[0].groupes:
        assert [e.valeur for e in notes_du(g)] == [N(1, 16), N(1, 8), N(1, 16)]
        assert sum(e.valeur for e in notes_du(g)) == C(2, 4).unite_temps

    # L'hémiole : aux mesures 2 et 3, trois appuis, une blanche chacun, comme
    # une seule mesure à 3/2 ; l'appui du milieu tombe sur le troisième temps,
    # faible, et se prolonge sur le premier de la mesure suivante : une syncope.
    hem = lire(FIGURES_GUIDE["me-hemiole"].texte)
    ev = evenements(hem[1:3])
    assert [t for t, _, e in ev if e.accent] == [0, N(1, 2), N(1)]
    assert duree(hem[1]) + duree(hem[2]) == C(3, 2).duree == 3 * N(1, 2)
    milieu = [(e, k) for e, k in classement(C(3, 4), hem[1:3]) if e.accent][1]
    assert milieu[1] == "syncope"
    assert C(3, 4).nom_temps(2) == "faible"

    # Syncopes et contretemps des exemples.
    for nom_figure, attendu in CLASSES_ATTENDUES.items():
        fig = FIGURES_GUIDE[nom_figure]
        mesures = lire(fig.texte)
        assert [k for _, k in classement(fig.chiffres, mesures)] == attendu, nom_figure

    # Les exercices : chaque mesure n'admet qu'un chiffre parmi les candidats.
    assert reponses_mesures() == [str(c) for c in EXERCICE_MESURES.chiffres]
    assert reponses_syncopes() == REPONSES_SYNCOPES
    # Aucune réponse n'est un silence, et les trois cas sont représentés.
    assert set(REPONSES_SYNCOPES) == {None, "syncope", "contretemps"}


CORRESPONDANCES = [(C(2, 4), C(6, 8)), (C(3, 4), C(9, 8)), (C(4, 4), C(12, 8)),
                   (C(2, 2), C(6, 4)), (C(3, 8), C(9, 16))]


def reponses_chiffres():
    res = []
    for c in EXERCICE_CHIFFRES:
        res.append((str(c), f"{c.genre}, {NOMBRES[c.temps]} temps, la {figure(c.unite_temps)}"))
    return res


def reponses_mesures():
    res = []
    for m in lire(EXERCICE_MESURES.texte):
        possibles = [c for c in CANDIDATS if admet(m, c)]
        assert len(possibles) == 1, (m, possibles)
        res.append(str(possibles[0]))
    return res


def reponses_syncopes():
    mesures = lire(EXERCICE_SYNCOPES.texte)
    return [k for e, k in classement(EXERCICE_SYNCOPES.chiffres, mesures) if e.numerote]


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def lily_duree(valeur):
    for base in FIGURES:
        for points in range(2):
            if base * (2 - N(1, 2 ** points)) == valeur:
                return str(base.denominator) + "." * points
    raise ValueError(valeur)


def ly_element(e, debut_poutre=False, fin_poutre=False, dessus=(), dessous=()):
    txt = ("r" if e.note is None else e.note.lily()) + lily_duree(e.valeur)
    if debut_poutre:
        txt += "["
    if fin_poutre:
        txt += "]"
    if e.accent:
        txt += "->"
    if e.liee:
        txt += "~"
    txt += "".join("^" + m for m in dessus) + "".join("_" + m for m in dessous)
    return txt


def italique(texte, taille="small"):
    return r'\markup \%s \italic "%s"' % (taille, texte)


def ly_mesure(mesure, marques):
    """Une mesure en LilyPond ; `marques` : élément -> (dessus, dessous)."""
    corps = []
    for g in mesure.groupes:
        notes = notes_du(g)
        poutre = len(notes) > 1 and all(e.valeur < N(1, 4) for e in notes)
        txt = " ".join(ly_element(e, poutre and i == 0, poutre and i == len(notes) - 1,
                                  *marques.get(id(e), ((), ())))
                       for i, e in enumerate(notes))
        if isinstance(g, Nolet):
            txt = r"\tuplet %d/%d { %s }" % (g.reelles, g.normales, txt)
        corps.append(txt)
    return " ".join(corps)


def temps_de(fig, mesures, chiffres):
    """Chaque temps des mesures : (chiffre, numéro du temps compté de 0)."""
    res = []
    for i, (m, c) in enumerate(zip(mesures, chiffres)):
        nombre = int(duree(m) / c.unite_temps)
        premier = c.temps - nombre if (fig.anacrouse and i == 0) else 0
        res += [(c, k) for k in range(premier, premier + nombre)]
    return res


def ligne_des_temps(fig, mesures, chiffres):
    """
    Les numéros ou les forces des temps, sous la portée. Ils s'accrochent aux
    notes d'une voix invisible, une par temps : centrés sous les temps, et
    espacés comme eux même sous une blanche.
    """
    temps = temps_de(fig, mesures, chiffres)
    voix = " ".join("b'" + lily_duree(c.unite_temps) for c, _ in temps)
    lignes = []
    for quoi in ("comptes", "forces"):
        if getattr(fig, quoi):
            syllabes = " ".join('"%s"' % (str(k + 1) if quoi == "comptes" else c.nom_temps(k))
                                for c, k in temps)
            forme = (r" \override LyricText.font-shape = #'italic"
                     r" \override LyricSpace.minimum-distance = #1.5" if quoi == "forces" else "")
            lignes.append(r'\new Lyrics \with { \override LyricText.font-size = #-1%s }'
                          r' \lyricsto "temps" { %s }' % (forme, syllabes))
    return voix, lignes


def figure_ly(fig, numerotees=None):
    mesures = lire(fig.texte)
    chiffres = chiffres_de(fig, mesures)
    marques = {}

    def ajouter(e, dessus=(), dessous=()):
        a, b = marques.get(id(e), ((), ()))
        marques[id(e)] = (a + tuple(dessus), b + tuple(dessous))

    if fig.classes:
        for e, k in classement(chiffres[0], mesures, debut_de(fig, mesures)):
            if k:
                ajouter(e, dessus=[italique(k, "tiny")])
    if fig.textes:
        for i, texte in fig.textes.items():
            ajouter(notes_du(mesures[i].groupes[0])[0], dessus=[italique(texte)])
    if fig.numeros == "mesures":
        for i, m in enumerate(mesures):
            ajouter(notes_du(m.groupes[0])[0], dessus=[r"\markup \small \bold %d" % (i + 1)])
    if fig.numeros == "notes":
        k = 0
        for m in mesures:
            for g in m.groupes:
                for e in notes_du(g):
                    if e.numerote:
                        k += 1
                        ajouter(e, dessous=[r"\markup \small %d" % k])

    corps, chiffre = [], None
    for i, (m, c) in enumerate(zip(mesures, chiffres)):
        if c != chiffre:
            corps.append(r"\time " + str(c))
            chiffre = c
        if fig.anacrouse and i == 0:
            corps.append(r"\partial %s" % lily_duree(duree(m)))
        corps.append(ly_mesure(m, marques))
        if i < len(mesures) - 1:
            corps.append(r'\bar "||"' if m.double else "|")

    reglages = [r"\autoBeamOff"]
    if not fig.symbole:
        reglages.append(r"\numericTimeSignature")
    if fig.numeros == "mesures":
        reglages += [r"\omit Staff.TimeSignature", r"\override TextScript.staff-padding = #2.5"]
    if fig.numeros == "notes":
        reglages.append(r"\override TextScript.staff-padding = #4")
    if fig.classes:
        # Les mots au-dessus des notes leur font de la place.
        reglages.append(r"\textLengthOn")
    melodie = r"""\new Voice {
        \clef treble %s
        %s
        \bar "|."
      }""" % (" ".join(reglages), " ".join(corps))

    if fig.comptes or fig.forces:
        voix, lignes = ligne_des_temps(fig, mesures, chiffres)
        musique = r"""<<
    \new Staff <<
      %s
      \new NullVoice = "temps" { %s }
    >>
    %s
  >>""" % (melodie, voix, "\n    ".join(lignes))
    else:
        musique = r"\new Staff { %s }" % melodie
    return r"""\score {
  %s
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
""" % musique


def ecrire_gravures():
    produits = [ecrire(nom_figure, figure_ly(fig), preambule=PREAMBULE_MESURE)
                for nom_figure, fig in FIGURES_GUIDE.items()]
    produits.append(ecrire("me-exercice-mesures", figure_ly(EXERCICE_MESURES),
                           preambule=PREAMBULE_MESURE))
    produits.append(ecrire("me-exercice-syncopes", figure_ly(EXERCICE_SYNCOPES),
                           preambule=PREAMBULE_MESURE))
    return produits


# ---------------------------------------------------------------------------
# Tableaux, exercices et réponses
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_mesure.py — ne pas modifier à la main.\n"
NI_L_UN = "ni l'un ni l'autre"


def ecrire_tex(nom, lignes):
    chemin = os.path.join(DIR_LY, nom + ".tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + "\n".join(lignes) + "\n")
    return chemin


def ecrire_tableaux():
    produits = []
    l = [r"\begin{tabular}{@{}l l l l@{}}", r"\toprule",
         r"\textbf{Chiffre} & \textbf{Temps} & \textbf{Unité de temps} & \textbf{Unité de mesure} \\",
         r"\midrule"]
    for c in (C(2, 4), C(3, 4), C(4, 4), C(2, 2), C(3, 8)):
        l.append(f"{c} & {NOMBRES[c.temps]} & {figure(c.unite_temps)} & {c.unite_mesure} \\\\")
    l += [r"\bottomrule", r"\end{tabular}"]
    produits.append(ecrire_tex("mesure-simples", l))

    l = [r"\begin{tabular}{@{}l l l l l@{}}", r"\toprule",
         r"\textbf{Chiffre} & \textbf{Temps} & \textbf{Unité de temps} & \textbf{Division}"
         r" & \textbf{Unité de mesure} \\",
         r"\midrule"]
    for c in (C(6, 8), C(9, 8), C(12, 8), C(6, 4)):
        l.append(f"{c} & {NOMBRES[c.temps]} & {figure(c.unite_temps)} & {figure(c.division)}"
                 f" & {c.unite_mesure} \\\\")
    l += [r"\bottomrule", r"\end{tabular}"]
    produits.append(ecrire_tex("mesure-composees", l))

    l = [r"\begin{tabular}{@{}l l l l l@{}}", r"\toprule",
         r"\textbf{Temps} & \textbf{Simple} & \textbf{Unité de temps} & \textbf{Composée}"
         r" & \textbf{Unité de temps} \\",
         r"\midrule"]
    for s, c in CORRESPONDANCES:
        l.append(f"{NOMBRES[s.temps]} & {s} & {figure(s.unite_temps)} & {c} & {figure(c.unite_temps)} \\\\")
    l += [r"\bottomrule", r"\end{tabular}"]
    produits.append(ecrire_tex("mesure-correspondances", l))
    return produits


def ecrire_exercices():
    produits = [ecrire_tex("mesure-exercice-chiffres",
                           [", ".join(str(c) for c in EXERCICE_CHIFFRES[:-1])
                            + f" et {EXERCICE_CHIFFRES[-1]}"]),
                ecrire_tex("mesure-exercice-candidats",
                           [", ".join(str(c) for c in CANDIDATS[:-1]) + f" et {CANDIDATS[-1]}"])]
    rep = [r"\textbf{Les chiffres.} "
           + "~; ".join(f"{c}~:~{r}" for c, r in reponses_chiffres()) + ".",
           "",
           r"\textbf{Les mesures.} "
           + "~; ".join(f"{i}~:~{r}" for i, r in enumerate(reponses_mesures(), 1)) + ".",
           "",
           r"\textbf{Syncopes et contretemps.} "
           + "~; ".join(f"{i}~:~{r or NI_L_UN}"
                        for i, r in enumerate(reponses_syncopes(), 1)) + "."]
    produits.append(ecrire_tex("mesure-reponses", rep))
    return produits


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
LIBELLES = {
    "me-temps": "une mélodie à 4/4",
    "me-simples": "mesures simples : 2/4, 3/4, 4/4, 2/2, 3/8",
    "me-forts": "temps forts et temps faibles",
    "me-anacrouse": "une anacrouse",
    "me-composees": "mesures composées : 6/8, 9/8, 12/8",
    "me-sicilienne": "la sicilienne",
    "me-correspondances": "2/4 et 6/8, triolets et duolets",
    "me-hemiole": "une hémiole",
    "me-syncopes": "syncopes",
    "me-syncopettes": "syncopettes",
    "me-contretemps": "contretemps",
    "me-irregulieres": "mesures irrégulières : 5/4, 7/8 de deux façons",
    "me-exercice-mesures": "exercice : les mesures sans chiffre",
    "me-exercice-syncopes": "exercice : syncopes et contretemps",
}


def xml_groupe(g):
    notes = [(e.note, e.valeur, e.liee, ("accent",) if e.accent else ()) for e in notes_du(g)]
    return Nolet(g.reelles, g.normales, notes) if isinstance(g, Nolet) else notes


def ecrire_musicxml():
    entrees, anacrouses, num = [], [], 0
    figures = list(FIGURES_GUIDE.items()) + [("me-exercice-mesures", EXERCICE_MESURES),
                                             ("me-exercice-syncopes", EXERCICE_SYNCOPES)]
    for nom_figure, fig in figures:
        if nom_figure == "me-c":
            continue  # les mêmes mesures que 4/4 et 2/2, écrites autrement
        mesures = lire(fig.texte)
        chiffres = chiffres_de(fig, mesures)
        if fig.anacrouse:
            anacrouses.append(num + 1)
        # Une entrée MusicXML garde un chiffre : on la coupe à chaque changement.
        debut = 0
        for i in range(1, len(mesures) + 1):
            if i == len(mesures) or chiffres[i] != chiffres[debut]:
                c = chiffres[debut]
                entrees.append((LIBELLES[nom_figure] if debut == 0 else "", 0, "major",
                                (c.haut, c.bas),
                                [[xml_groupe(g) for g in m.groupes] for m in mesures[debut:i]]))
                num += i - debut
                debut = i
    xml = musicxml.partition_rythmee(
        "La mesure",
        f"Les exemples et les exercices du guide, à la noire {TEMPO}.", entrees, "Piano", TEMPO)
    # L'anacrouse est une mesure incomplète, que les logiciels ne comptent pas.
    for k in anacrouses:
        xml = xml.replace(f'<measure number="{k}">', f'<measure number="{k}" implicit="yes">', 1)
    chemin = os.path.join(RACINE, "mesure.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(xml)
    return chemin


if __name__ == "__main__":
    verifier()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, RACINE))
    for c in ecrire_tableaux() + ecrire_exercices():
        print("LaTeX :", os.path.relpath(c, RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
