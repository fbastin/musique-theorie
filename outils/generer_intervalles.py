#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, le tableau et les fichiers MusicXML du guide des
intervalles.

    python3 outils/generer_intervalles.py

Comme pour les gammes, tout dérive d'un seul modèle (`intervalles.py`, sur les
hauteurs de `gammes.py`) : le guide et les fichiers MusicXML ne peuvent pas se
contredire.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import Note, gamme, note_de
from generer import DIR_LY, ENTETE_PORTEE, PIED_PORTEE, RACINE, ecrire, groupe
from intervalles import (SIMPLES, abrege, analyser, au_dessus, demi_tons, nom,
                         renverser, verifier)
import musicxml

DO = note_de("C", 4)


# ---------------------------------------------------------------------------
# Suites d'intervalles
# ---------------------------------------------------------------------------
def sur_do():
    """Les intervalles simples, tous au-dessus du do central."""
    return [((n, q), DO, au_dessus(DO, n, q)) for n, q in SIMPLES]


def de_la_gamme_majeure():
    """De la tonique de do majeur à chacun de ses degrés."""
    g = gamme(DO, "majeure")
    return [(analyser(DO, n), DO, n) for n in g[1:]]


def renversements():
    """Quelques intervalles et leur renversement : la note grave monte d'une octave."""
    paires = []
    for n, q in [(2, "majeure"), (3, "majeure"), (3, "mineure"), (4, "juste"), (4, "augmentée")]:
        haut = au_dessus(DO, n, q)
        octave = Note(DO.lettre, DO.alt, DO.octave + 1)
        paires.append(((n, q), DO, haut))
        paires.append((renverser(n, q), haut, octave))
    return paires


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
def entrees(suite):
    """Chaque intervalle joué note après note, puis ensemble, puis un silence."""
    return [(nom(*iv), 0, "major", [grave, aigu, [grave, aigu], None]) for iv, grave, aigu in suite]


def ecrire_musicxml():
    fichiers = [
        ("intervalles", "Les intervalles",
         "Les quatorze intervalles simples au-dessus de do, de l'unisson à "
         "l'octave : chacun joué note après note, puis les deux notes ensemble.",
         sur_do()),
        ("intervalles-gamme-majeure", "Les intervalles de la gamme majeure",
         "De la tonique de do majeur à chacun de ses degrés : tous majeurs "
         "ou justes.", de_la_gamme_majeure()),
        ("intervalles-renversements", "Renversements",
         "Chaque intervalle suivi de son renversement, la note grave passée à "
         "l'octave : les numéros se complètent à neuf, les qualités s'échangent.",
         renversements()),
    ]
    produits = []
    for nom_fichier, titre, description, suite in fichiers:
        chemin = os.path.join(RACINE, nom_fichier + ".musicxml")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(musicxml.partition(titre, description, entrees(suite), partie="Intervalles"))
        produits.append(chemin)
    return produits


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def accord(grave, aigu):
    return f"<{grave.lily()} {aigu.lily()}>"


def paroles(textes):
    # Une syllabe par accord ; les libellés à espaces entre guillemets.
    return " ".join(f'"{t}"' for t in textes)


def portee_avec_libelles(accords, libelles, coupure=None):
    """Des intervalles harmoniques, chacun nommé en dessous."""
    corps = []
    for i, a in enumerate(accords):
        corps.append(a)
        if coupure and i == coupure - 1:
            corps.append('\\bar "" \\break')
    return r"""\score {
  <<
    \new Staff {
      \accidentalStyle forget
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      %s
      \bar "|."
    }
    \addlyrics { %s }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.6
    }
    \context { \Lyrics \override LyricText.font-size = #-2.5 }
  }
}
""" % (" ".join(corps), paroles(libelles))


def figure_compter():
    """Le numéro se compte en lettres, la qualité en demi-tons."""
    paires = [(DO, note_de("E", 4)), (DO, note_de("Eb", 4)),
              (DO, note_de("D#", 4)), (note_de("C#", 4), note_de("Eb", 4))]
    corps = "    \\key c \\major\n"
    for grave, aigu in paires:
        corps += groupe([grave, aigu], abrege(*analyser(grave, aigu)))
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_sur_do():
    suite = sur_do()
    return portee_avec_libelles([accord(g, a) for _, g, a in suite],
                                [abrege(*iv) for iv, _, _ in suite], coupure=7)


def figure_enharmonie():
    """Même son, deux noms : c'est l'écriture qui décide."""
    paires = [(note_de("F", 4), note_de("G#", 4)), (note_de("F", 4), note_de("Ab", 4)),
              (DO, note_de("F#", 4)), (DO, note_de("Gb", 4))]
    corps = "    \\key c \\major\n"
    for grave, aigu in paires:
        corps += groupe([grave, aigu], abrege(*analyser(grave, aigu)))
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_renversements():
    suite = renversements()
    return portee_avec_libelles([accord(g, a) for _, g, a in suite],
                                [abrege(*iv) for iv, _, _ in suite])


def figure_gamme_majeure():
    suite = de_la_gamme_majeure()
    return portee_avec_libelles([accord(g, a) for _, g, a in suite],
                                [abrege(*iv) for iv, _, _ in suite])


FIGURES = {
    "i-compter": figure_compter,
    "i-sur-do": figure_sur_do,
    "i-enharmonie": figure_enharmonie,
    "i-renversements": figure_renversements,
    "i-gamme-majeure": figure_gamme_majeure,
}


# ---------------------------------------------------------------------------
# Tableau
# ---------------------------------------------------------------------------
def ecrire_table():
    """Les intervalles simples : taille, exemple sur do, renversement."""
    l = ["%% Produit par outils/generer_intervalles.py — ne pas modifier à la main.", "",
         r"\begin{tabular}{@{}l l c l l@{}}", r"\toprule",
         r"\textbf{Intervalle} & \textbf{Abrégé} & \textbf{Demi-tons} & "
         r"\textbf{Sur do} & \textbf{Renversement} \\", r"\midrule"]
    for (n, q), grave, aigu in sur_do():
        rn, rq = renverser(n, q)
        l.append(f"{nom(n, q)} & {abrege(n, q)} & {demi_tons(n, q)} & "
                 f"{grave.nom_fr()} -- {aigu.nom_fr()} & {nom(rn, rq)} \\\\")
    l += [r"\bottomrule", r"\end{tabular}", ""]
    chemin = os.path.join(DIR_LY, "intervalles-table.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(l) + "\n")
    return chemin


if __name__ == "__main__":
    verifier()
    for c in ecrire_musicxml():
        print("MusicXML :", os.path.relpath(c, RACINE))
    print("Tableau :", os.path.relpath(ecrire_table(), RACINE))
    for nom_figure, fabrique in FIGURES.items():
        print("LilyPond :", os.path.relpath(ecrire(nom_figure, fabrique()), RACINE))
