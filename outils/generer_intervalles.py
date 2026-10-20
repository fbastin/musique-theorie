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


def verifier_redoublement():
    """
    Redoubler un intervalle, c'est l'élargir d'une octave : la note aiguë monte
    d'une octave. Le numéro gagne sept (la seconde devient neuvième, la tierce
    dixième), la taille douze demi-tons, et la qualité ne change pas.
    """
    from gammes import TONALITES
    toniques = {t for _, maj, mi in TONALITES for t in (maj, mi)}
    for txt in toniques:
        base = note_de(txt, 4)
        for n, q in SIMPLES:
            if n == 1:
                continue        # l'unisson redoublé est l'octave
            haut = au_dessus(base, n, q)
            redouble = Note(haut.lettre, haut.alt, haut.octave + 1)
            lettres = 7 * (redouble.octave - base.octave) + redouble.idx - base.idx + 1
            assert lettres == n + 7
            # Sept lettres et douze demi-tons de plus : l'écart à la référence,
            # donc la qualité, est celui de l'intervalle simple.
            assert redouble.hauteur - base.hauteur == demi_tons(n, q) + 12
    # Les exemples du texte : la 9e est une 2de redoublée, la 10e une 3ce ;
    # do–ré de l'octave suivante, une neuvième majeure.
    assert 2 + 7 == 9 and 3 + 7 == 10 and 8 + 2 - 1 == 9
    re_suivant = Note("D", 0, DO.octave + 1)
    assert re_suivant.hauteur - DO.hauteur == demi_tons(2, "majeure") + 12


# Qualités au-delà des formes usuelles : un demi-ton de plus que l'augmentée,
# un de moins que la diminuée.
ETENDUES_JUSTE = {-2: "sous-diminuée", -1: "diminuée", 0: "juste", 1: "augmentée",
                  2: "sur-augmentée"}
ETENDUES_MAJEUR = {-3: "sous-diminuée", -2: "diminuée", -1: "mineure", 0: "majeure",
                   1: "augmentée", 2: "sur-augmentée"}


def qualite_etendue(grave, aigu):
    """Numéro et qualité d'un intervalle simple, sur-augmenté et sous-diminué compris."""
    from intervalles import JUSTES, REFERENCE
    numero = (aigu.idx - grave.idx) % 7 + 1
    ecart = aigu.hauteur - grave.hauteur - REFERENCE[numero]
    return numero, (ETENDUES_JUSTE if numero in JUSTES else ETENDUES_MAJEUR)[ecart]


DEMI_TONS = [(DO, note_de("C#", 4), "chromatique"), (note_de("C#", 4), note_de("D", 4), "diatonique"),
             (DO, note_de("Db", 4), "diatonique"), (note_de("Db", 4), note_de("D", 4), "chromatique")]


def verifier_complements():
    """
    Les deux demi-tons : sur une même lettre, un unisson augmenté, le demi-ton
    chromatique ; entre deux lettres voisines, une seconde mineure, le demi-ton
    diatonique. Un ton en réunit un de chaque sorte, dans un ordre ou dans
    l'autre. Puis les formes sur-augmentée et sous-diminuée du texte.
    """
    for grave, aigu, sorte in DEMI_TONS:
        assert aigu.hauteur - grave.hauteur == 1
        attendu = (1, "augmentée") if sorte == "chromatique" else (2, "mineure")
        assert analyser(grave, aigu) == attendu, (grave, aigu)
        assert (grave.lettre == aigu.lettre) == (sorte == "chromatique")
    assert analyser(note_de("E", 4), note_de("F", 4)) == (2, "mineure")
    assert analyser(DO, note_de("D", 4)) == (2, "majeure")
    # Do bémol–fa dièse, sept demi-tons : une quarte sur-augmentée ; do
    # dièse–sol bémol, cinq : une quinte sous-diminuée. Les formes usuelles
    # restent celles du modèle commun.
    assert qualite_etendue(note_de("Cb", 4), note_de("F#", 4)) == (4, "sur-augmentée")
    assert note_de("F#", 4).hauteur - note_de("Cb", 4).hauteur == 7
    assert qualite_etendue(note_de("C#", 4), note_de("Gb", 4)) == (5, "sous-diminuée")
    assert note_de("Gb", 4).hauteur - note_de("C#", 4).hauteur == 5
    for n, q in SIMPLES:
        if n < 8:
            assert qualite_etendue(DO, au_dessus(DO, n, q)) == (n, q)


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


def figure_demi_tons():
    """Un ton, coupé en deux demi-tons de deux sortes, dans un ordre puis dans l'autre."""
    corps = "    \\key c \\major\n"
    for grave, aigu, sorte in DEMI_TONS:
        corps += groupe([grave, aigu], sorte)
    # Les libellés sont plus larges que les crochets : on écarte les notes.
    return ENTETE_PORTEE + corps + PIED_PORTEE.replace("spacing-increment = #2.2",
                                                         "spacing-increment = #5")


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
    "i-demi-tons": figure_demi_tons,
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
    verifier_redoublement()
    verifier_complements()
    for c in ecrire_musicxml():
        print("MusicXML :", os.path.relpath(c, RACINE))
    print("Tableau :", os.path.relpath(ecrire_table(), RACINE))
    for nom_figure, fabrique in FIGURES.items():
        print("LilyPond :", os.path.relpath(ecrire(nom_figure, fabrique()), RACINE))
