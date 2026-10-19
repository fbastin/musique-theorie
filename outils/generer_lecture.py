#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures et les tableaux du guide « Lire les notes ».

    python3 outils/generer_lecture.py

Tout dérive du modèle de hauteurs des autres guides (`gammes.py`) et d'une seule
donnée par clé : la ligne qu'elle désigne et la note qu'elle y place. La note
de chaque position, les noms sous les gravures, le tableau des sept clés, celui
des repères et les réponses des exercices en découlent. Les affirmations chiffrées du texte sont
vérifiées avant toute écriture.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import LETTRES, Note
from generer import DIR_LY, PREAMBULE, ecrire

PREAMBULE_LECTURE = PREAMBULE.replace("outils/generer.py", "outils/generer_lecture.py")

# Position sur la portée : 0 pour la première ligne, 1 pour le premier
# interligne, 2 pour la deuxième ligne… 8 pour la cinquième. Au-delà, les
# positions continuent : −2 est la première ligne supplémentaire au-dessous,
# 10 la première au-dessus.
#
# Une clé : son nom LilyPond, la position qu'elle désigne et la note qu'elle y
# place (octaves du modèle : 4 est l'octave du do central). Les sept clés du
# solfège, rangées de la plus aiguë à la plus grave : d'une clé à la suivante,
# la même position descend d'une tierce.
CLES = {
    "sol": ("treble", 2, Note("G", 0, 4)),
    "ut1": ("soprano", 0, Note("C", 0, 4)),
    "ut2": ("mezzosoprano", 2, Note("C", 0, 4)),
    "ut3": ("alto", 4, Note("C", 0, 4)),
    "ut4": ("tenor", 6, Note("C", 0, 4)),
    "fa3": ("varbaritone", 4, Note("F", 0, 3)),
    "fa": ("bass", 6, Note("F", 0, 3)),
}

# Nom de chaque clé, dans le texte et les tableaux.
NOMS_CLES = {"sol": "clé de sol", "ut1": "clé d'ut", "ut2": "clé d'ut",
             "ut3": "clé d'ut", "ut4": "clé d'ut", "fa3": "clé de fa", "fa": "clé de fa"}

# La clé de sol octaviée : la clé de sol, un 8 dessous ; tout sonne une octave
# plus bas qu'écrit.
SOL_OCTAVIEE = "treble_8"

# Le signe d'octave : do5 à fa5, joués sous le signe, écrits do4 à fa4.
OTTAVA = [Note(L, 0, 6) for L in "CDEF"]

DO_CENTRAL = Note("C", 0, 4)


def rang(n):
    """Rang diatonique : une unité par position, sept par octave."""
    return 7 * n.octave + n.idx


def note_a(cle, position):
    """Note écrite à `position` dans `cle`."""
    _, p_ref, ref = CLES[cle]
    r = rang(ref) + position - p_ref
    return Note(LETTRES[r % 7], 0, r // 7)


def position_de(cle, n):
    _, p_ref, ref = CLES[cle]
    return p_ref + rang(n) - rang(ref)


def nom(n, octave=True):
    """Nom français ; numéro d'octave à la française (do central = do3)."""
    return n.nom_fr() + (str(n.octave - 1) if octave else "")


def ligne_de(cle):
    """« 2e ligne » : la ligne que désigne la clé."""
    return lieu(CLES[cle][1])


def nom_complet(cle):
    """« clé d'ut 1re ligne »."""
    return f"{NOMS_CLES[cle]} {ligne_de(cle)}"


def lieu(position):
    """« 2e ligne », « 3e interligne », « 1re ligne supplémentaire au-dessous »…"""
    def rangs(k, fem):
        return f"{k}{'re' if fem and k == 1 else 'er' if k == 1 else 'e'}"
    if 0 <= position <= 8:
        if position % 2 == 0:
            return f"{rangs(position // 2 + 1, True)} ligne"
        return f"{rangs(position // 2 + 1, False)} interligne"
    if position < 0:
        k, cote = -position, "au-dessous"
    else:
        k, cote = position - 8, "au-dessus"
    if k % 2 == 0:
        return f"{rangs(k // 2, True)} ligne supplémentaire {cote}"
    return f"{rangs(k // 2 + 1, False)} interligne supplémentaire {cote}"


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def verifier():
    # Le do central : première ligne supplémentaire, au-dessous en clé de sol,
    # au-dessus en clé de fa ; ligne désignée par les clés d'ut.
    assert position_de("sol", DO_CENTRAL) == -2
    assert position_de("fa", DO_CENTRAL) == 10
    assert lieu(-2) == "1re ligne supplémentaire au-dessous"
    assert lieu(10) == "1re ligne supplémentaire au-dessus"
    assert position_de("ut3", DO_CENTRAL) == 4 and position_de("ut4", DO_CENTRAL) == 6

    # Les quatre clés d'ut désignent toutes le do central, sur les lignes 1 à
    # 4 ; les deux clés de fa, le fa2, sur la 3e et la 4e ligne.
    for k, cle in enumerate(("ut1", "ut2", "ut3", "ut4")):
        assert nom(CLES[cle][2]) == nom(DO_CENTRAL) and ligne_de(cle) == lieu(2 * k)
    assert nom(CLES["fa3"][2]) == nom(CLES["fa"][2]) == "fa2"
    assert (ligne_de("fa3"), ligne_de("fa")) == ("3e ligne", "4e ligne")

    # Sept clés, sept noms : de la clé de sol à la clé de fa 4e ligne, la
    # première ligne descend d'une tierce à chaque clé, et porte chaque nom une
    # fois. Il en va de même à toute position.
    premieres = [note_a(cle, 0) for cle in CLES]
    assert [nom(n) for n in premieres] == ["mi3", "do3", "la2", "fa2", "ré2", "si1", "sol1"]
    assert all(rang(a) - rang(b) == 2 for a, b in zip(premieres, premieres[1:]))
    for p in range(-6, 15):
        assert len({note_a(cle, p).lettre for cle in CLES}) == 7

    # En clé d'ut 1re ligne, la note se lit deux noms avant la clé de sol, une
    # tierce plus bas : la première ligne porte do3 et non mi3.
    for p in range(-6, 15):
        assert rang(note_a("sol", p)) - rang(note_a("ut1", p)) == 2

    # Le diapason : le la3 au 2e interligne de la clé de sol.
    assert nom(note_a("sol", 3)) == "la3" and lieu(3) == "2e interligne"

    # La clé de sol octaviée : à position égale, une octave sous la clé de sol.
    assert SOL_OCTAVIEE == CLES["sol"][0] + "_8"

    # Le signe d'octave : do5 à fa5 joués, écrits do4 à fa4, dans la portée.
    assert [nom(n) for n in OTTAVA] == ["do5", "ré5", "mi5", "fa5"]
    ecrites = [Note(n.lettre, n.alt, n.octave - 1) for n in OTTAVA]
    assert [nom(n) for n in ecrites] == ["do4", "ré4", "mi4", "fa4"]
    assert all(0 <= position_de("sol", n) <= 8 for n in ecrites)

    # Les clés : sol3 sur la 2e ligne, fa2 sur la 4e.
    assert nom(note_a("sol", 2)) == "sol3" and lieu(2) == "2e ligne"
    assert nom(note_a("fa", 6)) == "fa2" and lieu(6) == "4e ligne"

    # Trois do : do4 au 3e interligne en clé de sol, do2 au 2e en clé de fa,
    # à égale distance du do central.
    assert nom(note_a("sol", 5)) == "do4" and lieu(5) == "3e interligne"
    assert nom(note_a("fa", 3)) == "do2" and lieu(3) == "2e interligne"
    assert rang(note_a("sol", 5)) - rang(DO_CENTRAL) == rang(DO_CENTRAL) - rang(note_a("fa", 3))

    # Sol3 et fa2 à deux lignes du do central, de part et d'autre.
    assert rang(note_a("sol", 2)) - rang(DO_CENTRAL) == 4
    assert rang(DO_CENTRAL) - rang(note_a("fa", 6)) == 4

    # À position égale, la clé de fa nomme la note deux noms plus loin, et
    # près de deux octaves plus bas : douze positions, une treizième.
    for p in range(-6, 15):
        s, f = note_a("sol", p), note_a("fa", p)
        assert (f.idx - s.idx) % 7 == 2
        assert rang(s) - rang(f) == 12

    # Une note et son octave : jamais toutes deux sur une ligne.
    for p in range(-6, 15):
        assert (p % 2) != ((p + 7) % 2)

    # La grande portée : lignes de la clé de fa, do central, lignes de la clé
    # de sol, toutes à une tierce l'une de l'autre — onze lignes régulières.
    onze = onze_lignes()
    assert len(onze) == 11 and onze[5] == DO_CENTRAL
    assert all(rang(b) - rang(a) == 2 for a, b in zip(onze, onze[1:]))


def onze_lignes():
    fa = [note_a("fa", p) for p in range(0, 9, 2)]
    sol = [note_a("sol", p) for p in range(0, 9, 2)]
    return fa + [DO_CENTRAL] + sol


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def suite_nommee(cle, notes):
    """Une portée de rondes, chacune nommée dessous (sans numéro d'octave)."""
    return r"""\score {
  \new Staff {
    \clef %s
    \omit Staff.TimeSignature
    \cadenzaOn
    %s
    \bar "|."
  }
  \addlyrics { %s }
  \layout { }
}
""" % (CLES[cle][0], " ".join(n.lily() + "1" for n in notes),
       " ".join(nom(n, octave=False) for n in notes))


def gamme_diatonique(depart, longueur, pas=1):
    return [Note(LETTRES[(rang(depart) + pas * i) % 7], 0, (rang(depart) + pas * i) // 7)
            for i in range(longueur)]


def figure_cle(cle):
    """La clé seule, et la note qu'elle désigne sur sa ligne."""
    lily, p, n = CLES[cle]
    return r"""\score {
  \new Staff {
    \clef %s
    \omit Staff.TimeSignature
    \cadenzaOn
    %s1
    \bar "|."
  }
  \layout { }
}
""" % (lily, n.lily())


def figure_sol_octaviee():
    """La clé de sol octaviée et la note de sa deuxième ligne, sol3 écrit."""
    _, p, n = CLES["sol"]
    return r"""\score {
  \new Staff {
    \clef "%s"
    \omit Staff.TimeSignature
    \cadenzaOn
    %s1
    \bar "|."
  }
  \layout { }
}
""" % (SOL_OCTAVIEE, n.lily())


def figure_ottava():
    """Quatre notes sous le signe 8va : écrites une octave plus bas qu'elles ne sonnent."""
    return r"""\score {
  \new Staff {
    \clef treble
    \omit Staff.TimeSignature
    \cadenzaOn
    \ottava #1 %s \ottava #0
    \bar "|."
  }
  \layout { }
}
""" % " ".join(n.lily() + "1" for n in OTTAVA)


def figure_grande_portee():
    """Le do central dans les deux portées, puis une gamme qui passe de l'une à l'autre."""
    montee = gamme_diatonique(note_a("fa", 6), 9)           # de fa2 à sol3
    bas = [n for n in montee if rang(n) < rang(DO_CENTRAL)]
    haut = [n for n in montee if rang(n) >= rang(DO_CENTRAL)]
    s_haut = " ".join(["s1"] * len(bas)) + " " + " ".join(n.lily() + "1" for n in haut)
    s_bas = " ".join(n.lily() + "1" for n in bas) + " " + " ".join(["s1"] * len(haut))
    do = DO_CENTRAL.lily() + "1"
    return r"""\score {
  \new PianoStaff <<
    \new Staff = "haut" {
      \clef treble \omit Staff.TimeSignature \cadenzaOn
      %s \bar "||" %s \bar "|."
    }
    \new Staff = "bas" {
      \clef bass \omit Staff.TimeSignature \cadenzaOn
      %s \bar "||" %s \bar "|."
    }
  >>
  \layout { }
}
""" % (do, s_haut, do, s_bas), montee


# Exercices : positions choisies pour couvrir la portée, ses deux bords et les
# deux premières lignes supplémentaires de chaque côté.
EXERCICES = {
    "sol": [2, 5, -2, 8, 0, 6, 3, 10, -1, 7, 4, 12],
    "fa": [6, 3, 10, 0, 8, -2, 5, 1, 12, 4, 7, -1],
    "ut1": [0, 4, 7, -2, 2, 9, 5, 1, 10, 6, -1, 3],
}


def figure_exercice(cle):
    notes = [note_a(cle, p) for p in EXERCICES[cle]]
    corps = " ".join(f"{n.lily()}1^\\markup{{\\small {i}}}" for i, n in enumerate(notes, 1))
    return r"""\score {
  \new Staff {
    \clef %s
    \omit Staff.TimeSignature
    \cadenzaOn
    %s
    \bar "|."
  }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #2.4 }
  }
}
""" % (CLES[cle][0], corps), notes


def ecrire_gravures():
    produits = []
    produits.append(ecrire("l-sol-montee",
                           suite_nommee("sol", gamme_diatonique(DO_CENTRAL, 15)),
                           preambule=PREAMBULE_LECTURE))
    produits.append(ecrire("l-fa-descente",
                           suite_nommee("fa", gamme_diatonique(DO_CENTRAL, 15, pas=-1)),
                           preambule=PREAMBULE_LECTURE))
    for cle in CLES:
        produits.append(ecrire(f"l-cle-{cle}", figure_cle(cle), preambule=PREAMBULE_LECTURE))
    produits.append(ecrire("l-cle-sol8", figure_sol_octaviee(), preambule=PREAMBULE_LECTURE))
    produits.append(ecrire("l-ottava", figure_ottava(), preambule=PREAMBULE_LECTURE))
    contenu, _ = figure_grande_portee()
    produits.append(ecrire("l-grande-portee", contenu, preambule=PREAMBULE_LECTURE))
    for cle in EXERCICES:
        contenu, _ = figure_exercice(cle)
        produits.append(ecrire(f"l-exercice-{cle}", contenu, preambule=PREAMBULE_LECTURE))
    return produits


# ---------------------------------------------------------------------------
# Tableaux et figure TikZ
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_lecture.py — ne pas modifier à la main.\n"


def ecrire_tex(nom_fichier, contenu):
    chemin = os.path.join(DIR_LY, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + contenu)
    return chemin


def tableau_reperes():
    """Les notes des lignes et des interlignes, dans les sept clés."""
    l = [r"\begin{tabular}{@{}l *{5}{c} @{\hspace{14pt}} *{4}{c}@{}}",
         r"\toprule",
         r" & \multicolumn{5}{c}{\textbf{Lignes}} & \multicolumn{4}{c}{\textbf{Interlignes}} \\",
         r"\cmidrule(lr){2-6}\cmidrule(l){7-10}",
         r" & 1 & 2 & 3 & 4 & 5 & 1 & 2 & 3 & 4 \\",
         r"\midrule"]
    for cle in CLES:
        lignes = [nom(note_a(cle, p)) for p in range(0, 9, 2)]
        inter = [nom(note_a(cle, p)) for p in range(1, 8, 2)]
        libelle = "C" + NOMS_CLES[cle][1:] + " " + exposant(CLES[cle][1]).replace(" ", "~")
        l.append(libelle + " & " + " & ".join(lignes + inter) + r" \\")
        if cle in ("sol", "ut4"):
            l.append(r"\addlinespace[3pt]")
    l += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(l) + "\n"


def exposant(position):
    """« 2\textsuperscript{e} ligne » pour LaTeX."""
    k = position // 2 + 1
    return r"%d\textsuperscript{%s} ligne" % (k, "re" if k == 1 else "e")


def tableau_cles():
    """
    Les sept clés, chacune avec la note qu'elle désigne et sa ligne : la clé de
    sol et les deux clés de fa, puis les quatre clés d'ut.
    """
    def bloc(cles, largeur):
        cols = "c" * len(cles)
        images = " &\n".join(r"\includegraphics{l-cle-%s.cropped.pdf}" % c for c in cles)
        noms = " & ".join(r"\small %s" % NOMS_CLES[c] for c in cles)
        notes = " &\n".join(r"\small\color{mygray} %s, %s" % (nom(CLES[c][2]), exposant(CLES[c][1]))
                            for c in cles)
        return (r"\begin{tabular*}{%s\linewidth}{@{\extracolsep{\fill}}%s@{}}" % (largeur, cols) + "\n"
                + images + r" \\[2pt]" + "\n" + noms + r" \\" + "\n" + notes + r" \\" + "\n"
                + r"\end{tabular*}" + "\n")
    return (bloc(["sol", "fa", "fa3"], "0.68") + r"\\[10pt]" + "\n"
            + bloc(["ut1", "ut2", "ut3", "ut4"], "0.9"))


def tikz_onze_lignes():
    """
    La grande portée vue comme une portée de onze lignes, dont la ligne du
    milieu — le do central — n'est tracée qu'à la demande.
    """
    onze = onze_lignes()
    l = [r"\begin{tikzpicture}[x=1cm, y=0.45cm]"]
    for i, n in enumerate(onze):
        y = i
        if i == 5:
            l.append(r"  \draw[accent, dashed, line width=0.7pt] (2.2,%d) -- (3.8,%d);" % (y, y))
            l.append(r"  \node[right, accent, font=\small\bfseries] at (6.3,%d) {%s, le do central};" % (y, nom(n)))
        else:
            l.append(r"  \draw[line width=0.5pt] (0,%d) -- (6,%d);" % (y, y))
            l.append(r"  \node[right, font=\small] at (6.3,%d) {%s};" % (y, nom(n)))
    l.append(r"  \draw[navy, decorate, decoration={brace, amplitude=5pt}] (-0.25,6) -- (-0.25,10)"
             r" node[midway, left=7pt, font=\small, navy] {clé de sol};")
    l.append(r"  \draw[navy, decorate, decoration={brace, amplitude=5pt}] (-0.25,0) -- (-0.25,4)"
             r" node[midway, left=7pt, font=\small, navy] {clé de fa};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l) + "\n"


def reponses():
    blocs = []
    for cle, libelle in (("sol", "En clé de sol"), ("fa", "En clé de fa"),
                         ("ut1", "En clé d'ut 1\\textsuperscript{re} ligne")):
        _, notes = figure_exercice(cle)
        items = ", ".join(f"{i}~:~{nom(n)}" for i, n in enumerate(notes, 1))
        blocs.append(r"\textbf{%s.} %s." % (libelle, items))
    return "\n\n".join(blocs) + "\n"


def legende_grande_portee():
    _, montee = figure_grande_portee()
    return r"de %s à %s" % (nom(montee[0]), nom(montee[-1]))


def ecrire_tableaux():
    return [ecrire_tex("lecture-cles.tex", tableau_cles()),
            ecrire_tex("lecture-reperes.tex", tableau_reperes()),
            ecrire_tex("lecture-onze-lignes.tex", tikz_onze_lignes()),
            ecrire_tex("lecture-reponses.tex", reponses())]


if __name__ == "__main__":
    verifier()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, os.path.dirname(DIR_LY)))
    for c in ecrire_tableaux():
        print("Tableaux :", os.path.relpath(c, os.path.dirname(DIR_LY)))
    print("Grande portée :", legende_grande_portee())
