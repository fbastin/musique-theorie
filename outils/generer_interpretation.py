#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les tableaux, les gravures, les réponses des exercices et le fichier
MusicXML du guide « L'interprétation ».

    python3 outils/generer_interpretation.py

Les termes — mouvements, nuances, articulations, caractère — et leurs données
vivent ici : les tableaux du guide, les réponses des exercices et le fichier
MusicXML en dérivent, si bien que le texte et ce qu'on entend ne peuvent pas
se contredire. Les affirmations du texte — des fourchettes de mouvement
ordonnées, des nuances graduées, une articulation plus ou moins brève, l'ordre
dans lequel se jouent des mesures reprises — sont vérifiées avant toute
écriture.
"""

import os
import sys
from collections import namedtuple
from fractions import Fraction
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import Note
from generer import DIR_LY, PREAMBULE, RACINE, ecrire
import musicxml

PREAMBULE_INTERPRETATION = PREAMBULE.replace("outils/generer.py",
                                             "outils/generer_interpretation.py")
N = Fraction
TEMPO = 80

# ---------------------------------------------------------------------------
# Les termes
# ---------------------------------------------------------------------------
# Les mouvements, du plus lent au plus vif : terme, sens littéral, fourchette
# indicative en pulsations par minute (None : pas de borne). Les fourchettes se
# chevauchent et varient d'une source à l'autre ; seul leur ordre est sûr.
Mouvement = namedtuple("Mouvement", "terme sens fourchette")
MOUVEMENTS = [
    Mouvement("grave", "grave, pesant", (25, 45)),
    Mouvement("largo", "large", (40, 60)),
    Mouvement("lento", "lent", (45, 60)),
    Mouvement("larghetto", "un peu large", (60, 66)),
    Mouvement("adagio", "à l'aise", (66, 76)),
    Mouvement("andante", "en allant", (76, 108)),
    Mouvement("moderato", "modéré", (108, 120)),
    Mouvement("allegretto", "un peu allègre", (112, 120)),
    Mouvement("allegro", "allègre, gai", (120, 168)),
    Mouvement("vivace", "vif", (156, 176)),
    Mouvement("presto", "prompt, rapide", (168, 200)),
    Mouvement("prestissimo", "très rapide", (200, None)),
]
RANG = {m.terme: i for i, m in enumerate(MOUVEMENTS)}

# Les changements de mouvement : terme, abréviation, sens, effet (−1 plus
# lent, 1 plus vif, 0 retour ou souplesse), progressif ou immédiat.
Changement = namedtuple("Changement", "terme abrege sens effet progressif")
CHANGEMENTS_MOUVEMENT = [
    Changement("accelerando", "accel.", "en accélérant", 1, True),
    Changement("stringendo", "string.", "en pressant", 1, True),
    Changement("rallentando", "rall.", "en ralentissant", -1, True),
    Changement("ritardando", "rit., ritard.", "en retardant", -1, True),
    Changement("allargando", "allarg.", "en élargissant : plus lent, souvent plus fort", -1, True),
    Changement("ritenuto", "riten.", "retenu : plus lent aussitôt", -1, False),
    Changement("più mosso", "", "plus animé", 1, False),
    Changement("meno mosso", "", "moins animé", -1, False),
    Changement("a tempo", "", "au mouvement : celui d'avant le changement", 0, False),
    Changement("tempo primo", "Tempo I", "le premier mouvement", 0, False),
    Changement("l'istesso tempo", "", "le même mouvement : la pulsation ne change pas avec la mesure",
               0, False),
    Changement("tempo rubato", "rubato", "temps dérobé : pressé ici, rendu là", 0, False),
    Changement("ad libitum", "ad lib.", "à volonté : le mouvement laissé à l'interprète", 0, False),
    Changement("a piacere", "", "à plaisir : librement", 0, False),
]

# Les nuances, du plus doux au plus fort : signe, terme, sens, et vélocité MIDI
# par défaut de MuseScore, que reprend Sodor Piano (sur 127).
Nuance = namedtuple("Nuance", "signe terme sens velocite")
NUANCES = [
    Nuance("pp", "pianissimo", "très doux", 33),
    Nuance("p", "piano", "doux", 49),
    Nuance("mp", "mezzo piano", "moyennement doux", 64),
    Nuance("mf", "mezzo forte", "moyennement fort", 80),
    Nuance("f", "forte", "fort", 96),
    Nuance("ff", "fortissimo", "très fort", 112),
]
NUANCE = {x.signe: x for x in NUANCES}

# Les changements de nuance : terme, abréviation ou signe (LaTeX), sens.
CHANGEMENTS_NUANCE = [
    ("crescendo", r"\emph{cresc.}, $<$", "en croissant"),
    ("decrescendo", r"\emph{decresc.}, $>$", "en décroissant"),
    ("diminuendo", r"\emph{dim.}, $>$", "en diminuant"),
    ("morendo", "", "en mourant : en s'éteignant"),
    ("smorzando", r"\emph{smorz.}", "en étouffant : en s'éteignant"),
    ("perdendosi", r"\emph{perd.}", "en se perdant : en s'éteignant peu à peu"),
    ("subito", r"\emph{sub.}", "soudain : \\emph{p subito}, aussitôt doux"),
    ("sforzando", r"\textbf{\emph{sf}}, \textbf{\emph{sfz}}", "en forçant : une note soudain appuyée"),
    ("rinforzando", r"\textbf{\emph{rf}}, \textbf{\emph{rfz}}", "en renforçant : quelques notes soudain appuyées"),
    ("forte-piano", r"\textbf{\emph{fp}}", "fort, puis aussitôt doux"),
]

# Les articulations : nom, signe (en mots), écriture LilyPond, marque
# MusicXML, part de la valeur à peu près jouée, effet. Le legato et le portato
# s'écrivent sur plusieurs notes, sous une liaison ; le MusicXML écrit le
# portato par son autre signe, le trait surmonté d'un point, d'une note à
# l'autre.
Articulation = namedtuple("Articulation", "nom signe lily xml part effet")
ARTICULATIONS = [
    Articulation("legato", "une liaison sur plusieurs notes", "", None, N(1),
                 "lié : sans coupure entre les notes"),
    Articulation("staccato", "un point", "-.", "staccato", N(1, 2),
                 "détaché : la note écourtée"),
    Articulation("staccatissimo", "un petit triangle", "-!", "staccatissimo", N(1, 4),
                 "très détaché : la note très brève"),
    Articulation("portato", "des points sous une liaison", "-.", "detached-legato", N(3, 4),
                 "porté : à peine détaché"),
    Articulation("tenuto", "un trait", "--", "tenuto", N(1),
                 "tenu : toute la valeur, un peu appuyée"),
    Articulation("accent", "un chevron couché", "->", "accent", N(1),
                 "attaque renforcée"),
    Articulation("marcato", "un chevron dressé", "-^", "strong-accent", N(1),
                 "marqué : attaque plus forte encore"),
]
ARTICULATION = {a.nom: a for a in ARTICULATIONS}

# Les signes qui se cumulent sur une note : l'un dit l'attaque, l'autre la
# durée. Le trait et le point réunis font le louré, ou portato.
Combinaison = namedtuple("Combinaison", "signes lily effet")
COMBINAISONS = [
    Combinaison(("accent", "staccato"), "->-.", "appuyée et brève"),
    Combinaison(("accent", "tenuto"), "->--", "appuyée et tenue"),
    Combinaison(("tenuto", "staccato"), "-_", "le louré : à peine détachée"),
    Combinaison(("marcato", "staccato"), "-^-.", "marquée et brève"),
]


def part_combinee(signes):
    """La part de la valeur que laissent des signes cumulés."""
    if set(signes) == {"tenuto", "staccato"}:
        return ARTICULATION["portato"].part
    return min(ARTICULATION[x].part for x in signes)

# Le caractère, et les mots qui modifient les autres.
CARACTERE = [
    ("agitato", "agité"), ("animato", "animé"), ("cantabile", "chantant"),
    ("con brio", "avec éclat"), ("con moto", "avec mouvement"),
    ("dolce", "doux"), ("espressivo", "expressif"), ("giocoso", "joyeux"),
    ("grazioso", "gracieux"), ("leggiero", "léger"), ("maestoso", "majestueux"),
    ("pesante", "lourd"), ("scherzando", "en badinant"), ("sostenuto", "soutenu"),
    ("tranquillo", "tranquille"),
]
MODIFICATEURS = [
    ("molto", "beaucoup, très"), ("assai", "très"), ("poco", "peu, un peu"),
    ("poco a poco", "peu à peu"), ("più", "plus"), ("meno", "moins"),
    ("non troppo", "pas trop"), ("sempre", "toujours"), ("simile", "de même"),
    ("quasi", "presque, comme"), ("con", "avec"), ("senza", "sans"),
    ("ma", "mais"), ("e, ed", "et"),
]


def vocabulaire():
    """Tous les mots des tableaux, en minuscules."""
    termes = ([m.terme for m in MOUVEMENTS] + [c.terme for c in CHANGEMENTS_MOUVEMENT]
              + [x.terme for x in NUANCES] + [c[0] for c in CHANGEMENTS_NUANCE]
              + [a.nom for a in ARTICULATIONS] + [t for t, _ in CARACTERE + MODIFICATEURS])
    return {mot.strip(",").lower() for t in termes for mot in t.replace("-", " ").split()}


# ---------------------------------------------------------------------------
# Notes, indications et mesures
# ---------------------------------------------------------------------------
# Une note : hauteur (« C5 », None pour un silence), valeur, indications. Une
# indication est une articulation, une nuance (« p », « sfz »…), un soufflet
# (« < », « > », « ! » pour sa fin), une liaison (« ( », « ) »), un texte
# au-dessus (« t:rit. ») ou un numéro d'exercice (« n:3 »).
J = namedtuple("J", "hauteur valeur marques", defaults=((),))
# Une mesure : notes, et ce qui l'entoure : reprises, volta, segno, Fine, saut.
M = namedtuple("M", "notes debut_reprise fin_reprise volta segno fine saut",
               defaults=(False, False, None, False, False, None))


def note(txt):
    """« C5 », « F#4 » -> Note, octaves du modèle (4 : celle du do central)."""
    lettre, alt, octave = txt[0], txt[1:-1].count("#") - txt[1:-1].count("b"), int(txt[-1])
    return Note(lettre, alt, octave)


def j(txt, valeur, *marques):
    return J(txt, valeur, marques)


# « Au clair de la lune », la phrase que varient les exemples.
AU_CLAIR = [[j("C5", N(1, 4)), j("C5", N(1, 4)), j("C5", N(1, 4)), j("D5", N(1, 4))],
            [j("E5", N(1, 2)), j("D5", N(1, 2))],
            [j("C5", N(1, 4)), j("E5", N(1, 4)), j("D5", N(1, 4)), j("D5", N(1, 4))],
            [j("C5", N(1))]]


def varier(phrase, regle):
    """
    La phrase, chaque note recevant les indications que lui donne `regle`,
    fonction de (numéro de mesure, rang dans la mesure, dernière note ?).
    """
    nb = len(phrase)
    return [[J(x.hauteur, x.valeur, x.marques + tuple(regle(m, i, m == nb - 1 and i == len(mes) - 1)))
             for i, x in enumerate(mes)] for m, mes in enumerate(phrase)]


def partout(*marques):
    """Les mêmes indications sur chaque note, sauf la dernière, tenue."""
    return lambda m, i, derniere: () if derniere else marques


def liaisons_par_deux(m, i, derniere):
    """Une liaison sur chaque paire de mesures : 1-2, puis 3-4."""
    if m % 2 == 0 and i == 0:
        return ("(",)
    if m % 2 == 1 and (i == 1 or (m == 3 and i == 0)):
        return (")",)
    return ()


def portato(m, i, derniere):
    """Le portato : des points sous une liaison, sur chaque paire de mesures."""
    marques = () if derniere else ("portato",)
    return marques + liaisons_par_deux(m, i, derniere)


# Les variantes de la phrase : libellé, mouvement (terme ou None), tempo, règle.
Variante = namedtuple("Variante", "libelle mouvement tempo regle")
VARIANTES = [
    Variante("sans indication", None, TEMPO, lambda m, i, d: ()),
    Variante("legato", None, TEMPO, liaisons_par_deux),
    Variante("staccato", None, TEMPO, partout("staccato")),
    Variante("staccatissimo", None, TEMPO, partout("staccatissimo")),
    Variante("portato", None, TEMPO, portato),
    Variante("accent sur chaque premier temps", None, TEMPO,
             lambda m, i, d: ("accent",) if i == 0 else ()),
    Variante("accent et staccato", None, TEMPO, partout("accent", "staccato")),
    Variante("piano, crescendo, forte, decrescendo", None, TEMPO,
             lambda m, i, d: {(0, 0): ("p", "<"), (2, 0): ("f", ">"), (3, 0): ("p",)}.get((m, i), ())),
    Variante("forte, puis piano subito", None, TEMPO,
             lambda m, i, d: {(0, 0): ("f",), (2, 0): ("p", "t:subito")}.get((m, i), ())),
    Variante("sforzando", None, TEMPO,
             lambda m, i, d: {(0, 0): ("p",), (1, 0): ("sfz",)}.get((m, i), ())),
    Variante("adagio", "Adagio", 72, lambda m, i, d: ()),
    Variante("allegro", "Allegro", 144, lambda m, i, d: ()),
]

# Les mouvements des figures : celui de la phrase, de l'exemple de
# ralentissement et de l'exercice.
MOUVEMENT_PHRASE = ("Andante", 76)
MOUVEMENT_RIT = ("Allegro", 132)
MOUVEMENT_EXERCICE = ("Moderato", 112)

# Le ritardando : la phrase deux fois, ralentie à partir de la troisième
# mesure, puis reprise a tempo. Les tempos, temps par temps, mesure par mesure.
RITARDANDO = (varier(AU_CLAIR, lambda m, i, d: ("t:rit.",) if (m, i) == (2, 0) else ())
              + varier(AU_CLAIR, lambda m, i, d: ("t:a tempo",) if (m, i) == (0, 0) else ()))
TEMPOS_RITARDANDO = {2: (76, 70, 64, 58), 3: (52,), 4: (TEMPO,)}

# La phrase du titre et de l'avant-propos : les quatre familles d'indications.
PHRASE = varier(AU_CLAIR, lambda m, i, d: {
    (0, 0): ("p", "t:dolce", "("), (1, 0): ("<",), (1, 1): (")",),
    (2, 0): ("mf", ">", "staccato"), (2, 1): ("staccato",), (2, 2): ("staccato",),
    (2, 3): ("staccato",), (3, 0): ("p", "tenuto")}.get((m, i), ()))

# Les reprises : 1 2 et la première fin, reprises ; puis 1 2 et la seconde fin.
REPRISES = [M([j("E5", N(1, 4)), j("D5", N(1, 4)), j("C5", N(1, 4)), j("D5", N(1, 4))],
              debut_reprise=True),
            M([j("E5", N(1, 4)), j("E5", N(1, 4)), j("E5", N(1, 2))]),
            M([j("D5", N(1, 4)), j("D5", N(1, 4)), j("D5", N(1, 2))], fin_reprise=True, volta=1),
            M([j("C5", N(1))], volta=2)]

# Les signes de répétition : un motif d'une ou deux mesures, puis le signe
# qui le répète, autant de fois qu'indiqué.
Repetition = namedtuple("Repetition", "motif fois")
REPETITIONS = [
    Repetition([[j("C5", N(1, 4)), j("E5", N(1, 4)), j("G5", N(1, 4)), j("E5", N(1, 4))]], 2),
    Repetition([[j("D5", N(1, 4)), j("F5", N(1, 4)), j("A5", N(1, 4)), j("F5", N(1, 4))],
                [j("G5", N(1, 2)), j("G4", N(1, 2))]], 2),
]


def deplier(repetitions):
    """Les mesures telles qu'elles se jouent : chaque motif autant de fois qu'indiqué."""
    return [mes for r in repetitions for _ in range(r.fois) for mes in r.motif]


# L'exercice des reprises : une reprise, un segno, Fine, et D.S. al Fine.
EXERCICE_REPRISES = [
    M([j("C5", N(1, 4)), j("E5", N(1, 4)), j("G5", N(1, 4)), j("E5", N(1, 4))], debut_reprise=True),
    M([j("F5", N(1, 4)), j("D5", N(1, 4)), j("B4", N(1, 2))], fin_reprise=True),
    M([j("C5", N(1, 4)), j("C5", N(1, 4)), j("E5", N(1, 4)), j("G5", N(1, 4))], segno=True),
    M([j("C6", N(1, 2)), j("G5", N(1, 2))], fine=True),
    M([j("A5", N(1, 4)), j("F5", N(1, 4)), j("D5", N(1, 4)), j("F5", N(1, 4))]),
    M([j("G5", N(1, 4)), j("F5", N(1, 4)), j("E5", N(1, 4)), j("D5", N(1, 4))], saut="D.S. al Fine"),
]

# L'exercice des signes : « Frère Jacques », chaque signe numéroté. Le numéro
# suit le signe qu'il désigne, sur la même note.
FRERE_JACQUES = [
    [j("C5", N(1, 4), "p", "n:1"), j("D5", N(1, 4)), j("E5", N(1, 4)), j("C5", N(1, 4))],
    [j("C5", N(1, 4), "staccato", "n:2"), j("D5", N(1, 4), "staccato"),
     j("E5", N(1, 4), "staccato"), j("C5", N(1, 4), "staccato")],
    [j("E5", N(1, 4), "<", "n:3"), j("F5", N(1, 4)), j("G5", N(1, 2), "f", "n:4")],
    [j("E5", N(1, 4), "(", "n:5"), j("F5", N(1, 4), ")"), j("G5", N(1, 2), "accent", "n:6")],
    [j("G5", N(1, 8), "marcato", "n:7"), j("A5", N(1, 8)), j("G5", N(1, 8)), j("F5", N(1, 8)),
     j("E5", N(1, 4)), j("C5", N(1, 4))],
    [j("G5", N(1, 8), ">", "n:8"), j("A5", N(1, 8)), j("G5", N(1, 8)), j("F5", N(1, 8)),
     j("E5", N(1, 4)), j("C5", N(1, 4), "tenuto", "n:9")],
    [j("C5", N(1, 4), "pp", "n:10"), j("G4", N(1, 4)), j("C5", N(1, 2))],
]

# Les autres exercices : ranger, traduire.
RANGER = [["allegro", "largo", "presto", "andante", "moderato"],
          ["vivace", "adagio", "prestissimo", "andante", "allegretto"]]
TRADUIRE = [
    ("Allegro ma non troppo", "allègre, mais pas trop"),
    ("Andante con moto", "en allant, avec mouvement"),
    ("Poco a poco crescendo", "en croissant peu à peu"),
    ("Più mosso", "plus animé"),
    ("Dolce e cantabile", "doux et chantant"),
    ("Sempre staccato", "toujours détaché"),
    ("Molto ritardando", "en retardant beaucoup"),
]


# ---------------------------------------------------------------------------
# L'ordre de jeu
# ---------------------------------------------------------------------------
def ordre_joue(mesures):
    """
    Les numéros des mesures dans l'ordre où elles se jouent. Une reprise se
    joue deux fois ; une mesure sous volta ne se joue qu'au passage de son
    numéro ; après un D.C. ou un D.S., on ne refait pas les reprises et l'on
    s'arrête à Fine.
    """
    res, i, passage, debut, reprises, saute = [], 0, 1, 0, set(), False
    while i < len(mesures):
        m = mesures[i]
        if m.debut_reprise and i != debut:
            debut, passage = i, 1
        if m.volta is not None:
            assert not saute, "volta après un saut : non prévu"
            if m.volta != passage:
                i += 1
                continue
        res.append(i + 1)
        if saute and m.fine:
            break
        if m.fin_reprise and not saute and i not in reprises:
            reprises.add(i)
            passage, i = 2, debut
            continue
        if m.saut and not saute:
            saute = True
            if m.saut.startswith("D.S."):
                i = max(k for k in range(i) if mesures[k].segno)
            else:
                i = 0
            continue
        i += 1
    return res


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def verifier():
    # Les fourchettes de mouvement sont ordonnées : chaque borne au moins égale
    # à celle du terme plus lent, chaque fourchette dans le bon sens.
    for lent, vif in zip(MOUVEMENTS, MOUVEMENTS[1:]):
        assert lent.fourchette[0] <= vif.fourchette[0], (lent, vif)
        assert vif.fourchette[1] is None or lent.fourchette[1] <= vif.fourchette[1], (lent, vif)
    for m in MOUVEMENTS:
        assert m.fourchette[1] is None or m.fourchette[0] < m.fourchette[1], m

    # Les nuances sont graduées, du plus doux au plus fort.
    velocites = [x.velocite for x in NUANCES]
    assert velocites == sorted(set(velocites))

    # Le staccatissimo est plus bref que le staccato, lui-même plus bref que
    # le portato ; legato, tenuto et accents gardent toute la valeur.
    part = {a.nom: a.part for a in ARTICULATIONS}
    assert part["staccatissimo"] < part["staccato"] < part["portato"] < 1
    assert part["legato"] == part["tenuto"] == part["accent"] == 1

    # Les exercices de rangement : chaque terme est au tableau, et deux termes
    # voisins dans la réponse ne se chevauchent pas — l'ordre est sans appel.
    for serie in RANGER:
        rep = sorted(serie, key=RANG.__getitem__)
        for lent, vif in zip(rep, rep[1:]):
            assert MOUVEMENTS[RANG[lent]].fourchette[1] <= MOUVEMENTS[RANG[vif]].fourchette[0]
    # Chaque mot à traduire figure dans les tableaux.
    mots = vocabulaire()
    for indication, _ in TRADUIRE:
        for mot in indication.lower().split():
            assert mot in mots, mot

    # Les tempos des variantes tombent dans la fourchette de leur terme ; le
    # ritardando ralentit à chaque temps.
    exemples = ([(v.mouvement, v.tempo) for v in VARIANTES if v.mouvement]
                + [MOUVEMENT_PHRASE, MOUVEMENT_RIT, MOUVEMENT_EXERCICE])
    for terme, tempo in exemples:
        bas, haut = MOUVEMENTS[RANG[terme.lower()]].fourchette
        assert bas <= tempo and (haut is None or tempo <= haut), (terme, tempo)
    ralenti = TEMPOS_RITARDANDO[2] + TEMPOS_RITARDANDO[3]
    assert list(ralenti) == sorted(set(ralenti), reverse=True) and ralenti[0] < TEMPO
    assert TEMPOS_RITARDANDO[4] == (TEMPO,)

    # Les diminutifs et le superlatif du texte : larghetto moins lent que
    # largo, allegretto moins vif qu'allegro, prestissimo plus vif que presto.
    assert RANG["largo"] < RANG["larghetto"] and RANG["allegretto"] < RANG["allegro"]
    assert RANG["presto"] < RANG["prestissimo"]

    # Chaque mesure est complète, à 4/4 ; chaque texte au-dessus de la portée
    # est un terme ou une abréviation des tableaux.
    phrases = [AU_CLAIR, PHRASE, FRERE_JACQUES, RITARDANDO, deplier(REPETITIONS)]
    phrases += [[m.notes for m in r] for r in (REPRISES, EXERCICE_REPRISES)]
    abreges = {a.strip() for c in CHANGEMENTS_MOUVEMENT for a in c.abrege.split(",")}
    for mesures in phrases:
        for mes in mesures:
            assert sum(x.valeur for x in mes) == 1, mes
            for x in mes:
                for mq in x.marques:
                    if mq.startswith("t:"):
                        assert mq[2:] in abreges or set(mq[2:].split()) <= mots, mq

    # Les signes cumulés : l'accent garde la durée de l'autre signe, le
    # trait et le point réunis valent le portato, entre staccato et tenuto.
    for c in COMBINAISONS:
        assert all(x in ARTICULATION for x in c.signes)
    assert part_combinee(("accent", "staccato")) == part["staccato"]
    assert part_combinee(("accent", "tenuto")) == 1
    assert part["staccato"] < part_combinee(("tenuto", "staccato")) < part["tenuto"]

    # Les signes de répétition : chaque signe redonne exactement son motif, une
    # ou deux mesures.
    jouees = deplier(REPETITIONS)
    assert len(jouees) == sum(len(r.motif) * r.fois for r in REPETITIONS) == 6
    assert jouees[0] == jouees[1] and jouees[2:4] == jouees[4:6]
    assert {len(r.motif) for r in REPETITIONS} == {1, 2}

    # Les reprises : 1 2 3, puis 1 2 4 ; l'exercice : la reprise, puis le
    # retour au segno jusqu'à Fine.
    assert ordre_joue(REPRISES) == [1, 2, 3, 1, 2, 4]
    assert ordre_joue(EXERCICE_REPRISES) == [1, 2, 1, 2, 3, 4, 5, 6, 3, 4]

    # Chaque signe numéroté de l'exercice est au tableau, et les numéros se
    # suivent.
    nums = [numero_et_signe(x) for mes in FRERE_JACQUES for x in mes if numero_et_signe(x)]
    assert [k for k, _ in nums] == list(range(1, len(nums) + 1))
    for _, signe in nums:
        assert nom_du_signe(signe)


# ---------------------------------------------------------------------------
# Tableaux et réponses
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_interpretation.py — ne pas modifier à la main.\n"


def fourchette_tex(f):
    bas, haut = f
    return f"{bas} et plus" if haut is None else f"{bas} à {haut}"


def fr(texte):
    """Espaces insécables devant les deux-points et les points-virgules."""
    return texte.replace(" : ", "~: ").replace(" ; ", "~; ")


def tableau(colonnes, titres, lignes):
    lignes = [[fr(c) for c in l] for l in lignes]
    return "\n".join([r"\begin{tabular}{@{}%s@{}}" % colonnes, r"\toprule",
                      " & ".join(r"\textbf{%s}" % t for t in titres) + r" \\", r"\midrule"]
                     + [" & ".join(l) + r" \\" for l in lignes]
                     + [r"\bottomrule", r"\end{tabular}"])


def deux_colonnes(paires):
    """Une liste de (terme, sens) sur deux colonnes de paires."""
    moitie = (len(paires) + 1) // 2
    gauche, droite = paires[:moitie], paires[moitie:] + [("", "")] * (2 * moitie - len(paires))
    return [[r"\emph{%s}" % a if a else "", b, r"\emph{%s}" % c if c else "", d]
            for (a, b), (c, d) in zip(gauche, droite)]


def tableaux():
    return {
        "mouvements": tableau("l l r", ["Mouvement", "Sens littéral", "Pulsations par minute"],
                              [[r"\emph{%s}" % m.terme, m.sens, fourchette_tex(m.fourchette)]
                               for m in MOUVEMENTS]),
        "changements": tableau("l l l", ["Terme", "Abrégé", "Sens"],
                               [[r"\emph{%s}" % c.terme, r"\emph{%s}" % c.abrege if c.abrege else "",
                                 c.sens] for c in CHANGEMENTS_MOUVEMENT]),
        "nuances": tableau("c l l", ["Signe", "Terme", "Sens"],
                           [[r"\textbf{\emph{%s}}" % x.signe, r"\emph{%s}" % x.terme, x.sens]
                            for x in NUANCES]),
        "changements-nuance": tableau("l l l", ["Terme", "Abrégé ou signe", "Sens"],
                                      [[r"\emph{%s}" % t, s, sens] for t, s, sens in CHANGEMENTS_NUANCE]),
        "articulations": tableau("l l l", ["Articulation", "Signe", "Effet"],
                                 [[r"\emph{%s}" % a.nom if a.nom != "accent" else a.nom, a.signe, a.effet]
                                  for a in ARTICULATIONS]),
        "caractere": tableau("l l l l", ["Terme", "Sens", "Terme", "Sens"], deux_colonnes(CARACTERE)),
        "modificateurs": tableau("l l l l", ["Terme", "Sens", "Terme", "Sens"],
                                 deux_colonnes(MODIFICATEURS)),
    }


def numero_et_signe(x):
    """(numéro, signe désigné) d'une note de l'exercice, ou None."""
    marques = list(x.marques)
    for k, mq in enumerate(marques):
        if mq.startswith("n:"):
            return int(mq[2:]), marques[k - 1]
    return None


def nom_du_signe(signe):
    """Le nom d'un signe et ce qu'il demande, tirés des tableaux."""
    if signe in NUANCE:
        x = NUANCE[signe]
        return r"\textbf{\emph{%s}}, \emph{%s} (%s)" % (x.signe, x.terme, x.sens)
    if signe in ARTICULATION:
        a = ARTICULATION[signe]
        nom = a.nom if a.nom == "accent" else r"\emph{%s}" % a.nom
        return f"{nom} ({a.effet.split(' : ')[0]})"
    if signe == "(":
        return r"liaison, \emph{legato} (%s)" % ARTICULATION["legato"].effet.split(" : ")[0]
    soufflets = {"<": ("soufflet ouvrant", "crescendo"), ">": ("soufflet fermant", "decrescendo")}
    if signe in soufflets:
        nom, terme = soufflets[signe]
        sens = next(s for t, _, s in CHANGEMENTS_NUANCE if t == terme)
        return rf"{nom}, \emph{{{terme}}} ({sens})"
    return None


def reponses():
    lignes = []
    for k, serie in enumerate(RANGER):
        lignes.append(f"{'AB'[k]}~: " + ", ".join(r"\emph{%s}" % t for t in sorted(serie, key=RANG.__getitem__)))
    ranger = r"\textbf{1.} " + "~; ".join(lignes) + "."
    traduire = r"\textbf{2.} " + "~; ".join(
        r"\emph{%s}~: %s" % (i, t) for i, t in TRADUIRE) + "."
    signes = r"\textbf{3.} " + "~; ".join(
        f"{k}~:~{nom_du_signe(s)}" for k, s in
        (numero_et_signe(x) for mes in FRERE_JACQUES for x in mes if numero_et_signe(x))) + "."
    ordre = r"\textbf{4.} " + ", ".join(str(k) for k in ordre_joue(EXERCICE_REPRISES)) + "."
    return "\n\n".join([ranger, traduire, signes, ordre])


def questions():
    """Les énoncés des exercices de rangement et de traduction."""
    ranger = "~; ".join(f"{'AB'[k]}~: " + ", ".join(r"\emph{%s}" % t for t in serie)
                        for k, serie in enumerate(RANGER)) + "."
    traduire = "~; ".join(r"\emph{%s}" % i for i, _ in TRADUIRE) + "."
    return ranger, traduire


def ecrire_tex():
    produits = []
    contenus = {f"interpretation-{nom}": t for nom, t in tableaux().items()}
    contenus["interpretation-ranger"], contenus["interpretation-traduire"] = questions()
    contenus["interpretation-reponses"] = reponses()
    for nom, contenu in contenus.items():
        chemin = os.path.join(DIR_LY, nom + ".tex")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(ENTETE_TEX + contenu + "\n")
        produits.append(chemin)
    return produits


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
DUREES_LILY = {N(1): "1", N(1, 2): "2", N(1, 4): "4", N(1, 8): "8", N(1, 16): "16"}


def lily_duree(valeur):
    for base, txt in DUREES_LILY.items():
        for points in range(3):
            if base * (2 - N(1, 2 ** points)) == valeur:
                return txt + "." * points
    raise ValueError(valeur)


LILY_SIGNES = {"<": r"\<", ">": r"\>", "!": r"\!", "(": "(", ")": ")",
               "sfz": r"\sfz", "fp": r"\fp"}


def lily_note(x):
    txt = (note(x.hauteur).lily() if x.hauteur else "r") + lily_duree(x.valeur)
    for mq in x.marques:
        if mq in ARTICULATION:
            txt += ARTICULATION[mq].lily
        elif mq in NUANCE:
            txt += "\\" + mq
        elif mq in LILY_SIGNES:
            txt += LILY_SIGNES[mq]
        elif mq.startswith("t:"):
            txt += r'^\markup \italic "%s"' % mq[2:]
        elif mq.startswith("n:"):
            txt += r"_\markup \small \bold %s" % mq[2:]
        else:
            raise ValueError(mq)
    return txt


def score(musique, layout="", numeros=False):
    """Une partition ; les numéros de mesure n'y paraissent que sur demande."""
    sans_numeros = "" if numeros else r" \omit BarNumber"
    return r"""\score {
  %s
  \layout {
    %s
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6%s }
  }
}
""" % (musique, layout, sans_numeros)


def portee(corps, temps="4/4", avant="", nom=""):
    return r"""\new Staff %s {
      \clef treble \time %s %s
      %s
      \bar "|."
    }""" % (nom, temps, avant, corps)


def mesures_lily(mesures, coupure=None):
    """Les mesures, séparées par des barres ; une nouvelle ligne à la mesure `coupure`."""
    blocs = [" ".join(lily_note(x) for x in mes) for mes in mesures]
    if coupure:
        blocs[coupure] = r"\break " + blocs[coupure]
    return " |\n      ".join(blocs)


def figure_phrase():
    corps = mesures_lily(PHRASE)
    return score(portee(corps, avant=r'\tempo "%s" 4 = %d' % MOUVEMENT_PHRASE))


def figure_tempo():
    # Allegro, puis un ritardando signalé par un trait jusqu'au retour a tempo.
    corps = (r"""\override TextSpanner.bound-details.left.text = \markup \italic "rit."
      \override TextSpanner.staff-padding = #2.5
      g'4 c'' e'' g'' | e''4 c'' g'2 |
      c''4\startTextSpan d'' e'' f'' | g''2 g''2\stopTextSpan |
      c''4^\markup \italic "a tempo" e'' g'' c''' | c'''1""")
    return score(portee(corps, avant=r'\tempo "%s" 4 = %d' % MOUVEMENT_RIT))


def figure_nuances():
    corps = " | ".join(f"c''1\\{x.signe}" for x in NUANCES)
    return score(portee(corps))


# « p subito » : la nuance, suivie du mot en italique.
PSUBITO = (r'psubito = #(make-dynamic-script (markup #:dynamic "p" #:hspace 0.6 '
           r'#:normal-text #:italic "subito"))' + "\n")


def figure_changements():
    # Les soufflets, le sforzando et le forte-piano sont nommés sous la portée ;
    # « cresc. » et « subito » se nomment eux-mêmes.
    sous = lambda t: r'_\markup \small \italic "%s"' % t
    corps = (r"""c''4\p\<%s d'' e'' f'' | g''2\f\>%s e''2 | c''1\p |
      c''4\cresc d'' e'' f'' | \break g''1\f |
      c''4\p d'' e''\sfz%s f'' | g''2\fp%s g''2 | c''2\f g''2\psubito"""
             % (sous("crescendo"), sous("decrescendo"), sous("sforzando"), sous("forte-piano")))
    return PSUBITO + score(portee(corps, avant=r"\override TextScript.staff-padding = #5"))


def figure_articulations():
    motif = ["C5", "D5", "E5", "F5"]
    blocs = []
    for a in ARTICULATIONS:
        notes = [note(h).lily() + "4" + a.lily for h in motif]
        if a.nom in ("legato", "portato"):
            notes[0] += "("
            notes[-1] += ")"
        notes[0] += r'_\markup \small \italic "%s"' % a.nom
        blocs.append(" ".join(notes))
    # Sur deux lignes, pour garder l'échelle des autres figures.
    blocs[4] = r"\break " + blocs[4]
    corps = " |\n      ".join(blocs)
    return score(portee(corps, avant=r"\override TextScript.staff-padding = #3"))


def figure_combinaisons():
    blocs = []
    for c in COMBINAISONS:
        blocs.append(r"c''4%s_\markup \small \italic \center-column { %s }" % (
            c.lily, " ".join(f'"{x}"' for x in (c.signes[0], "et " + c.signes[1]))))
    corps = r' \bar "|" '.join(blocs)
    return score(portee(corps, avant=r"\omit Staff.TimeSignature \cadenzaOn "
                        r"\override TextScript.staff-padding = #3 \textLengthOn"))


def figure_repetitions():
    """Chaque motif, puis le signe qui le répète."""
    corps = []
    for r in REPETITIONS:
        motif = " | ".join(" ".join(lily_note(x) for x in mes) for mes in r.motif)
        corps.append(r"\repeat percent %d { %s }" % (r.fois, motif))
    return score(portee(" | ".join(corps)))


def joue(hauteur, valeur, part):
    """Une note écrite, telle qu'elle se joue à peu près : la note, puis des silences."""
    son = valeur * part
    reste = valeur - son
    notes = [(hauteur, son)]
    # Le silence se décompose en valeurs simples, de la plus brève à la plus longue.
    for base in (N(1, 16), N(1, 8), N(1, 4)):
        position = sum(v for _, v in notes)
        if reste and (position % (2 * base)):
            notes.append((None, base))
            reste -= base
    assert reste >= 0
    if reste:
        notes.append((None, reste))
    assert sum(v for _, v in notes) == valeur
    return notes


DUREES = ["staccato", "staccatissimo", "portato", "tenuto"]


def figure_durees():
    ecrit, jouees = [], []
    for nom in DUREES:
        a = ARTICULATION[nom]
        notes = [note(h).lily() + "4" + a.lily for h in ("C5", "E5")]
        if nom == "portato":
            notes[0] += "("
            notes[-1] += ")"
        notes[0] += r'_\markup \small \italic "%s"' % nom
        ecrit.append(" ".join(notes))
        mes = []
        for h in ("C5", "E5"):
            mes += [(note(x).lily() if x else "r") + lily_duree(v) for x, v in joue(h, N(1, 4), a.part)]
        jouees.append(" ".join(mes))
    blocs = [portee(" | ".join(ecrit), "2/4", nom=r'\with { instrumentName = \markup \small \italic "écrit" }'),
             portee(" | ".join(jouees), "2/4",
                    nom=r'\with { instrumentName = \markup \small \italic \center-column { "à peu près" "joué" } }')]
    return score("\\new StaffGroup <<\n" + "\n".join(blocs) + "\n  >>", "indent = 17\\mm")


NUMEROS_MESURES = (r"\set Score.barNumberVisibility = #all-bar-numbers-visible "
                   r"\override Score.BarNumber.break-visibility = #end-of-line-invisible "
                   r'\bar "" ')


def lily_reprises(mesures, coupure=None):
    """
    Les mesures, avec leurs barres de reprise, voltas, segno, Fine et saut ;
    une nouvelle ligne à la mesure `coupure`.
    """
    corps = [NUMEROS_MESURES]
    for k, m in enumerate(mesures):
        if k == coupure:
            corps.append(r"\break")
        # Une volta se ferme et la suivante s'ouvre au même instant : une seule
        # commande pour les deux, sinon la seconde efface la première.
        commandes = []
        if k > 0 and mesures[k - 1].volta is not None:
            commandes.append("(volta #f)")
        if m.volta is not None:
            commandes.append('(volta "%d.")' % m.volta)
        if commandes:
            corps.append(r"\set Score.repeatCommands = #'(%s)" % " ".join(commandes))
        if m.debut_reprise:
            corps.append(r'\bar ".|:"')
        if m.segno:
            corps.append(r'\textMark \markup \musicglyph "scripts.segno"')
        corps.append(" ".join(lily_note(x) for x in m.notes))
        if m.fin_reprise:
            corps.append(r'\bar ":|."')
        elif m.fine:
            corps.append(r'\textEndMark \markup \italic "Fine" \bar "||"')
        elif m.saut:
            corps.append(r'\textEndMark \markup \italic "%s"' % m.saut)
        elif k < len(mesures) - 1:
            corps.append("|")
    if mesures[-1].volta is not None:
        corps.append(r"\set Score.repeatCommands = #'((volta #f))")
    return "\n      ".join(corps)


def figure_reprises(mesures, coupure=None):
    return score(portee(lily_reprises(mesures, coupure)), numeros=True)


def figure_exercice():
    corps = mesures_lily(FRERE_JACQUES, coupure=4)
    return score(portee(corps, avant=r'\tempo "%s" \override TextScript.staff-padding = #5.5'
                        % MOUVEMENT_EXERCICE[0]))


def figure_glyphe(nom):
    return r"""\markup \musicglyph "scripts.%s"
""" % nom


def ecrire_gravures():
    figures = {
        "ip-phrase": figure_phrase(),
        "ip-tempo": figure_tempo(),
        "ip-nuances": figure_nuances(),
        "ip-changements": figure_changements(),
        "ip-articulations": figure_articulations(),
        "ip-durees": figure_durees(),
        "ip-combinaisons": figure_combinaisons(),
        "ip-reprises": figure_reprises(REPRISES),
        "ip-repetitions": figure_repetitions(),
        "ip-exercice": figure_exercice(),
        "ip-exercice-reprises": figure_reprises(EXERCICE_REPRISES, coupure=3),
        "ip-segno": figure_glyphe("segno"),
        "ip-coda": figure_glyphe("coda"),
    }
    return [ecrire(nom, contenu, preambule=PREAMBULE_INTERPRETATION)
            for nom, contenu in figures.items()]


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
# `musicxml.partition_rythmee` écrit des notes et leurs articulations ; il faut
# ici, en plus, les nuances, les soufflets, les changements de mouvement, les
# liaisons d'expression et les reprises. Les notes passent par
# `musicxml._note_xml`, les indications sont écrites autour.
XML_NUANCES = {"sfz": 112, "fp": 96}


def _direction(contenu, placement="above", son=""):
    return ([f'      <direction placement="{placement}">',
             f"        <direction-type>{contenu}</direction-type>"]
            + ([f"        {son}"] if son else []) + ["      </direction>"])


def _dynamique(signe):
    velocite = NUANCE[signe].velocite if signe in NUANCE else XML_NUANCES[signe]
    # <sound dynamics> : pourcentage de la vélocité MIDI 90.
    return _direction(f"<dynamics><{signe}/></dynamics>", "below",
                      f'<sound dynamics="{velocite / 0.9:.2f}"/>')


def _mots(texte, gras=False, son=""):
    style = 'font-weight="bold"' if gras else 'font-style="italic"'
    return _direction(f"<words {style}>{escape(texte)}</words>", "above", son)


def _avec_liaison(lignes, type_):
    """Ajoute une liaison d'expression aux notations d'une note."""
    slur = f'<slur type="{type_}"/>'
    for k, l in enumerate(lignes):
        if "<notations>" in l:
            lignes[k] = l.replace("<notations>", "<notations>" + slur)
            return lignes
    return lignes[:-1] + [" " * 8 + f"<notations>{slur}</notations>", lignes[-1]]


def _poutres_mesure(mes):
    """Poutres des notes plus brèves que la noire, réunies temps par temps."""
    res = [()] * len(mes)
    debuts, position = [], N(0)
    for x in mes:
        debuts.append(position)
        position += x.valeur
    k = 0
    while k < len(mes):
        groupe = [k]
        while (groupe[-1] + 1 < len(mes) and mes[groupe[-1]].valeur < N(1, 4)
               and mes[groupe[-1] + 1].valeur < N(1, 4)
               and debuts[groupe[-1] + 1] // N(1, 4) == debuts[k] // N(1, 4)):
            groupe.append(groupe[-1] + 1)
        if len(groupe) > 1:
            types = [musicxml.type_et_points(mes[i].valeur)[0] for i in groupe]
            for i, p in zip(groupe, musicxml._poutres(types)):
                res[i] = p
        k = groupe[-1] + 1
    return res


def _notes_xml(mes, etat, divisions, tempos=()):
    """
    Les notes d'une mesure, précédées de leurs indications. `tempos` : un
    tempo par temps, à partir du premier, pour un changement progressif.
    """
    out, position = [], N(0)
    for x, poutres in zip(mes, _poutres_mesure(mes)):
        temps = position / N(1, 4)
        if temps.denominator == 1 and temps < len(tempos):
            out.append(f'      <sound tempo="{tempos[int(temps)]}"/>')
        nuance = any(mq in NUANCE or mq in XML_NUANCES for mq in x.marques)
        soufflet = any(mq in ("<", ">") for mq in x.marques)
        # Un soufflet ouvert s'arrête à la nuance ou au soufflet suivants.
        if etat["soufflet"] and (nuance or soufflet or "!" in x.marques):
            out += _direction('<wedge type="stop"/>', "below")
            etat["soufflet"] = False
        for mq in x.marques:
            if mq in NUANCE or mq in XML_NUANCES:
                out += _dynamique(mq)
            elif mq in ("<", ">"):
                out += _direction('<wedge type="%s"/>' % ("crescendo" if mq == "<" else "diminuendo"),
                                  "below")
                etat["soufflet"] = True
            elif mq.startswith("t:"):
                out += _mots(mq[2:])
        type_, points = musicxml.type_et_points(x.valeur)
        marques = tuple(ARTICULATION[mq].xml for mq in x.marques
                        if mq in ARTICULATION and ARTICULATION[mq].xml)
        lignes = musicxml._note_xml(note(x.hauteur) if x.hauteur else None, etat["mesure"],
                                    duree=int(x.valeur * 4 * divisions), type_=type_,
                                    points=points, poutres=poutres, marques=marques)
        for mq, type_liaison in (("(", "start"), (")", "stop")):
            if mq in x.marques:
                lignes = _avec_liaison(lignes, type_liaison)
        out += lignes
        position += x.valeur
    return out


def _barre_gauche(m):
    # bar-style, ending, repeat : l'ordre du schéma MusicXML.
    style = "<bar-style>heavy-light</bar-style>" if m.debut_reprise else ""
    ending = (f'<ending number="{m.volta}" type="start">{m.volta}.</ending>'
              if m.volta is not None else "")
    repeat = '<repeat direction="forward"/>' if m.debut_reprise else ""
    contenu = style + ending + repeat
    return [f'      <barline location="left">{contenu}</barline>'] if contenu else []


def _barre_droite(m, derniere):
    style = ("light-heavy" if m.fin_reprise or (derniere and m.saut) else
             "light-light" if derniere or m.fine else None)
    contenu = (f"<bar-style>{style}</bar-style>" if style else "")
    if m.volta is not None:
        contenu += f'<ending number="{m.volta}" type="{"stop" if m.fin_reprise else "discontinue"}"/>'
    if m.fin_reprise:
        contenu += '<repeat direction="backward"/>'
    return [f'      <barline location="right">{contenu}</barline>'] if contenu else []


# Une entrée du fichier : libellé, mouvement (terme ou None), tempo, mesures,
# et les tempos d'un changement progressif, temps par temps, par mesure.
Entree = namedtuple("Entree", "libelle mouvement tempo mesures tempos", defaults=({},))


def entrees():
    """Les variantes de la phrase, la phrase, les reprises, les exercices."""
    res = [Entree(v.libelle, v.mouvement, v.tempo, [M(mes) for mes in varier(AU_CLAIR, v.regle)])
           for v in VARIANTES]
    res.append(Entree("ritardando, puis a tempo", None, TEMPO, [M(mes) for mes in RITARDANDO],
                      TEMPOS_RITARDANDO))
    res.append(Entree("les quatre familles", *MOUVEMENT_PHRASE, [M(mes) for mes in PHRASE]))
    res.append(Entree("reprises, première et seconde fois", None, TEMPO, REPRISES))
    res.append(Entree("signes de répétition, joués en toutes notes", None, TEMPO,
                      [M(mes) for mes in deplier(REPETITIONS)]))
    res.append(Entree("exercice : les signes", *MOUVEMENT_EXERCICE, [M(mes) for mes in FRERE_JACQUES]))
    # Le D.S. al Fine vient en dernier : à Fine, la lecture s'arrête.
    res.append(Entree("exercice : les reprises", None, TEMPO, EXERCICE_REPRISES))
    return res


def partition():
    toutes = entrees()
    valeurs = [x.valeur for e in toutes for m in e.mesures for x in m.notes]
    divisions = 1
    while any((v * 4 * divisions).denominator != 1 for v in valeurs):
        divisions += 1
    out = ["".join(musicxml._debut(
        "L'interprétation",
        "Une même phrase sous différentes indications de mouvement, de nuance et "
        "d'articulation, puis les reprises et les exercices du guide.", "Piano")).rstrip("\n")]
    num = 0
    for e in toutes:
        etat = {"mesure": musicxml.Mesure(0), "soufflet": False}
        for k, m in enumerate(e.mesures):
            num += 1
            etat["mesure"].reset()
            out.append(f'    <measure number="{num}">')
            out += _barre_gauche(m)
            if num == 1:
                out += ["      <attributes>", f"        <divisions>{divisions}</divisions>",
                        "        <key><fifths>0</fifths><mode>major</mode></key>",
                        "        <time><beats>4</beats><beat-type>4</beat-type></time>",
                        "        <clef><sign>G</sign><line>2</line></clef>", "      </attributes>"]
            if k == 0:
                # En tête de chaque entrée : son libellé, son mouvement, et une
                # nuance moyenne, pour que l'entrée précédente ne déteigne pas.
                out += _mots(e.libelle, gras=True)
                if e.mouvement:
                    out += _direction(
                        f'<words font-weight="bold">{e.mouvement}</words></direction-type>'
                        f"<direction-type><metronome><beat-unit>quarter</beat-unit>"
                        f"<per-minute>{e.tempo}</per-minute></metronome>",
                        "above", f'<sound tempo="{e.tempo}"/>')
                else:
                    out.append(f'      <sound tempo="{e.tempo}"/>')
                if not any(mq in NUANCE for mq in m.notes[0].marques):
                    out.append(f'      <sound dynamics="{NUANCE["mf"].velocite / 0.9:.2f}"/>')
            if m.segno:
                out += _direction("<segno/>", "above", '<sound segno="segno"/>')
            out += _notes_xml(m.notes, etat, divisions, e.tempos.get(k, ()))
            if m.fine:
                out += _mots("Fine", son='<sound fine="yes"/>')
            if m.saut:
                out += _mots(m.saut, son='<sound dalsegno="segno"/>')
            out += _barre_droite(m, k == len(e.mesures) - 1)
            out.append("    </measure>")
    out.append("  </part>\n</score-partwise>")
    return "\n".join(out) + "\n"


def ecrire_musicxml():
    chemin = os.path.join(RACINE, "interpretation.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(partition())
    return chemin


if __name__ == "__main__":
    verifier()
    print("Vérifications : toutes passées")
    for c in ecrire_tex():
        print("LaTeX :", os.path.relpath(c, RACINE))
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
