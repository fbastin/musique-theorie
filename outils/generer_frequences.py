#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit la gravure, les tableaux, la figure et les valeurs citées du guide des
fréquences.

    python3 outils/generer_frequences.py

Tout dérive du modèle `frequences.py`, vérifié avant toute écriture. Les
nombres que le texte cite passent par des macros (gravures/freq-valeurs.tex) :
le texte et les tableaux ne peuvent pas se contredire.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frequences import (APOTOME, COMMA_PYTHAGORICIEN, COMMA_SYNTONIQUE,
                        INTERVALLES, LA, LIMMA, QUINTE, QUINTE_MESOTONIQUE,
                        SYSTEMES, TON_MAJEUR, TON_MINEUR, cents,
                        frequence_midi, harmoniques, nom_francais,
                        nom_international, spirale_quintes, tempere, verifier)
from generer import DIR_LY, ecrire

ENTETE_TEX = "%% Produit par outils/generer_frequences.py — ne pas modifier à la main.\n\n"

# Fréquences affichées par le clavier du synthétiseur (musique/synth.php), pour
# les touches que les expériences du guide emploient. Relevées dans la page :
# le synthétiseur arrondit au centième, parfois par défaut (659,25 et non 659,26).
SYNTH = {"A4": 440.00, "E5": 659.25, "C#5": 554.37, "A3": 220.00, "A5": 880.00}


# ---------------------------------------------------------------------------
# Mise en forme française des nombres
# ---------------------------------------------------------------------------
def num(x, d=2):
    """Nombre à la française : virgule décimale, signe moins typographique."""
    s = ("%." + str(d) + "f") % abs(x)
    s = s.replace(".", "{,}")
    return ("$-$" if x < 0 and round(abs(x), d) != 0 else "") + s


def signe(x, d=2):
    """Écart signé : +3,91 ou −13,69 ; 0 sans signe."""
    if round(abs(x), d) == 0:
        return num(0, d)
    return ("+" if x > 0 else "") + num(x, d)


def frac(r):
    r = Fraction(r)
    return str(r.numerator) if r.denominator == 1 else "%d/%d" % (r.numerator, r.denominator)


def ecrire_tex(nom, contenu):
    os.makedirs(DIR_LY, exist_ok=True)
    chemin = os.path.join(DIR_LY, nom + ".tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + contenu)
    return chemin


def nom_complet(m):
    nom, octave = nom_francais(m)
    return "%s%d" % (nom, octave)


# ---------------------------------------------------------------------------
# Tableaux
# ---------------------------------------------------------------------------
def table_octaves():
    lignes = []
    for oct_fr in range(0, 6):
        do, la = 12 * (oct_fr + 2), 12 * (oct_fr + 2) + 9
        lignes.append("%d & do%d & %s & %s & la%d & %s & %s \\\\" % (
            oct_fr, oct_fr, nom_international(do), num(frequence_midi(do)),
            oct_fr, nom_international(la), num(frequence_midi(la))))
    return (r"""\begin{tabular}{@{}c l l r l l r@{}}
\toprule
\textbf{Octave} & \multicolumn{2}{l}{\textbf{Do}} & \textbf{Hz} & \multicolumn{2}{l}{\textbf{La}} & \textbf{Hz} \\
 & \textit{français} & \textit{intern.} & & \textit{français} & \textit{intern.} & \\
\midrule
""" + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabular}\n")


def table_harmoniques():
    lignes = []
    for h in harmoniques():
        k = h["k"]
        rapport = "" if k == 1 else frac(Fraction(k, k - 1))
        taille = "" if k == 1 else num(cents(Fraction(k, k - 1)), 1)
        lignes.append("%d & %s & %s & %s & %s & %s \\\\" % (
            k, num(h["f"]), nom_complet(h["midi"]), signe(h["ecart"], 1),
            rapport, taille))
    return (r"""\begin{tabular}{@{}r r l r c r@{}}
\toprule
\textbf{Rang} & \textbf{Hz} & \textbf{Note tempérée} & \textbf{Écart} & \multicolumn{2}{c}{\textbf{Depuis la précédente}} \\
 & & \textit{la plus proche} & \textit{(cents)} & \textit{rapport} & \textit{cents} \\
\midrule
""" + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabular}\n")


def table_intervalles():
    lignes = []
    for nom, n, juste in INTERVALLES:
        lignes.append("%s & %d & %s & %d & %s & %s & %s & %s & %s \\\\" % (
            nom, n, num(tempere(n), 4), 100 * n, frac(juste),
            num(cents(juste)), signe(100 * n - cents(juste)),
            num(LA * tempere(n)), num(LA * float(juste))))
    return (r"""\begin{tabular}{@{}l r r r l r r r r@{}}
\toprule
 & & \multicolumn{2}{c}{\textbf{Tempéré}} & \multicolumn{2}{c}{\textbf{Juste}} & \textbf{Écart} & \multicolumn{2}{c}{\textbf{Sur la 440 (Hz)}} \\
\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(l){8-9}
\textbf{Intervalle} & \textbf{½ tons} & \textit{rapport} & \textit{cents} & \textit{rapport} & \textit{cents} & \textit{(cents)} & \textit{tempéré} & \textit{juste} \\
\midrule
""" + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabular}\n")


def table_quintes():
    lignes = []
    for p in spirale_quintes():
        tempere_nom = p["tempere_nom"]
        lignes.append("%d & %s & %s & %s & %s & %s \\\\" % (
            p["k"], p["nom"], num(p["pyth"]),
            tempere_nom if tempere_nom != p["nom"] else p["nom"],
            num(p["egal"]), signe(p["ecart"])))
    return (r"""\begin{tabular}{@{}r l r l r r@{}}
\toprule
 & \multicolumn{2}{c}{\textbf{Quintes justes (3/2)}} & \multicolumn{2}{c}{\textbf{Tempérament égal}} & \textbf{Écart} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
\textbf{Quintes} & \textit{note} & \textit{Hz} & \textit{note} & \textit{Hz} & \textit{(cents)} \\
\midrule
""" + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabular}\n")


def table_systemes():
    lignes_def = [
        ("quinte", "quinte"),
        ("ton", "ton"),
        ("tierce", "tierce majeure"),
        ("diatonique", "demi-ton diatonique (mi--fa)"),
        ("chromatique", "demi-ton chromatique (do--do dièse)"),
        ("loup", "quinte du loup"),
    ]
    # En-têtes courts : le tableau doit tenir dans la largeur de la page.
    courts = {"pythagoricien": "Pythagore", "juste (Zarlino)": "juste (Zarlino)",
              "mésotonique ¼ de comma": "mésotonique", "tempérament égal": "égal"}
    entetes = " & ".join(r"\textbf{%s}" % courts[n] for n, _ in SYSTEMES)
    lignes = []
    for cle, libelle in lignes_def:
        cellules = []
        for nom, s in SYSTEMES:
            v = s[cle]
            if v is None:
                cellules.append("---")
            elif cle == "ton" and nom.startswith("juste"):
                cellules.append("%s / %s" % (num(v), num(cents(TON_MINEUR))))
            else:
                cellules.append(num(v))
        lignes.append(libelle + " & " + " & ".join(cellules) + r" \\")
    return (r"""\begin{tabular}{@{}l r r r r@{}}
\toprule
\textbf{En cents} & """ + entetes + r""" \\
\midrule
""" + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabular}\n")


# ---------------------------------------------------------------------------
# Figure : écart des degrés de do majeur au tempérament égal
# ---------------------------------------------------------------------------
DEGRES = ["do", "ré", "mi", "fa", "sol", "la", "si", "do"]
DEMI_TONS = [0, 2, 4, 5, 7, 9, 11, 12]
PYTHAGORE = [Fraction(1), Fraction(9, 8), Fraction(81, 64), Fraction(4, 3),
             Fraction(3, 2), Fraction(27, 16), Fraction(243, 128), Fraction(2)]
ZARLINO = [Fraction(1), Fraction(9, 8), Fraction(5, 4), Fraction(4, 3),
           Fraction(3, 2), Fraction(5, 3), Fraction(15, 8), Fraction(2)]


def figure_ecarts():
    # La gamme pythagoricienne se construit par quintes : chaque degré en vérifie la
    # chaîne (fa est une quinte sous do, les autres de une à cinq quintes au-dessus).
    for r in PYTHAGORE:
        assert any(r == QUINTE ** k / Fraction(2) ** e for k in range(-1, 6) for e in range(-3, 4))
    ech_x, ech_y = 1.7, 0.16          # cm par degré, cm par cent
    ymin, ymax = -20, 12
    t = [r"\begin{tikzpicture}[font=\small]"]
    # Grille horizontale tous les 5 cents, axe du tempérament égal en gras.
    for y in range(ymin, ymax + 1, 5):
        style = "black, thick" if y == 0 else "gray!30"
        t.append(r"\draw[%s] (0,%.2f) -- (%.2f,%.2f);" % (style, y * ech_y, 7 * ech_x, y * ech_y))
        t.append(r"\node[left, gray] at (0,%.2f) {%s};" % (y * ech_y, signe(y, 0)))
    t.append(r"\node[rotate=90, gray] at (-1.1,%.2f) {cents};" % ((ymin + ymax) / 2 * ech_y))
    t.append(r"\node[right, font=\footnotesize] at (%.2f,0.18) {tempérament égal};" % (7 * ech_x + 0.05))
    for i, d in enumerate(DEGRES):
        t.append(r"\node[below] at (%.2f,%.2f) {%s};" % (i * ech_x, ymin * ech_y - 0.1, d))
    def point(couleur, carre, x, y):
        if carre:
            return r"\fill[%s] (%.2f,%.2f) +(-2pt,-2pt) rectangle +(2pt,2pt);" % (couleur, x, y)
        return r"\fill[%s] (%.2f,%.2f) circle (2.2pt);" % (couleur, x, y)

    ecarts = {}
    for nom, serie in (("pyth", PYTHAGORE), ("juste", ZARLINO)):
        ecarts[nom] = [cents(r) - 100 * DEMI_TONS[i] for i, r in enumerate(serie)]
    for nom, couleur in (("pyth", "navy"), ("juste", "accent")):
        t.append(r"\draw[%s, thick] %s;" % (couleur, " -- ".join(
            "(%.2f,%.2f)" % (i * ech_x, e * ech_y) for i, e in enumerate(ecarts[nom]))))
    # Une étiquette par point, au-dessus si l'écart est positif, au-dessous sinon.
    # Là où les deux gammes coïncident (ré, fa, sol), une seule, en noir.
    for i in range(len(DEGRES)):
        ep, ej = ecarts["pyth"][i], ecarts["juste"][i]
        commun = abs(ep - ej) < 1e-9
        for nom, e, couleur in (("pyth", ep, "navy"), ("juste", ej, "accent")):
            if abs(e) < 0.5 or (commun and nom == "juste"):
                continue
            t.append(r"\node[%s, %s, font=\scriptsize] at (%.2f,%.2f) {%s};"
                     % ("above" if e > 0 else "below", "black" if commun else couleur,
                        i * ech_x, e * ech_y, signe(e, 1)))
    for nom, couleur, carre in (("pyth", "navy", False), ("juste", "accent", True)):
        for i, e in enumerate(ecarts[nom]):
            t.append(point(couleur, carre, i * ech_x, e * ech_y))
    # Légende sur une ligne, sous les noms des degrés : entre les courbes, elle
    # finissait toujours par en croiser une (vers mi en haut, vers la en bas).
    y = ymin * ech_y - 0.95
    for x0, (libelle, couleur, carre) in ((1.2 * ech_x, ("gamme pythagoricienne", "navy", False)),
                                          (4.0 * ech_x, ("gamme juste (Zarlino)", "accent", True))):
        t.append(r"\draw[%s, thick] (%.2f,%.2f) -- (%.2f,%.2f);" % (couleur, x0, y, x0 + 0.6, y))
        t.append(point(couleur, carre, x0 + 0.3, y))
        t.append(r"\node[right, %s, font=\footnotesize] at (%.2f,%.2f) {%s};" % (couleur, x0 + 0.65, y, libelle))
    t.append(r"\end{tikzpicture}")
    return "\n".join(t) + "\n"


# ---------------------------------------------------------------------------
# Gravure : la série des harmoniques sur do1
# ---------------------------------------------------------------------------
LY_NOMS = ["c", "cis", "d", "ees", "e", "f", "fis", "g", "aes", "a", "bes", "b"]


def ly_hauteur(m):
    """Nom LilyPond absolu : MIDI 48 = c (do2), 60 = c' (do3)."""
    octave = m // 12 - 4
    return LY_NOMS[m % 12] + ("'" * octave if octave > 0 else "," * -octave)


def gravure_harmoniques():
    graves, aigues = [], []
    for h in harmoniques():
        etiquette = r'^\markup { \bold "%d" }' % h["k"]
        if abs(h["ecart"]) >= 10:
            etiquette += r' _\markup { \italic \small "%+d" }' % round(h["ecart"])
        note = ly_hauteur(h["midi"]) + "1" + etiquette
        (graves if h["midi"] < 60 else aigues).append(note)
    contenu = r"""\score {
  \new Staff {
    \omit Staff.TimeSignature
    \cadenzaOn
    \accidentalStyle forget
    \clef bass
    %s
    \clef treble
    %s
    \bar "|."
  }
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
    }
  }
}
""" % ("  ".join(graves), "  ".join(aigues))
    return ecrire("freq-harmoniques", contenu)


# ---------------------------------------------------------------------------
# Valeurs citées dans le texte
# ---------------------------------------------------------------------------
def valeurs():
    sp = spirale_quintes()
    meso = dict(SYSTEMES)["mésotonique ¼ de comma"]
    pyth = dict(SYSTEMES)["pythagoricien"]
    v = {
        "commaPyth": num(cents(COMMA_PYTHAGORICIEN)),
        "commaPythRapport": num(float(COMMA_PYTHAGORICIEN), 4),
        "commaSynt": num(cents(COMMA_SYNTONIQUE)),
        "commaHolder": num(1200 / 53),
        "limma": num(cents(LIMMA)),
        "apotome": num(cents(APOTOME)),
        "tonMaj": num(cents(TON_MAJEUR)),
        "tonMin": num(cents(TON_MINEUR)),
        "quinteJuste": num(cents(QUINTE)),
        "quarteJuste": num(cents(Fraction(4, 3))),
        "tierceJuste": num(cents(Fraction(5, 4))),
        "tiercePyth": num(cents(Fraction(81, 64))),
        "quinteMeso": num(QUINTE_MESOTONIQUE),
        "loupPyth": num(pyth["loup"]),
        "loupMeso": num(meso["loup"]),
        "demiTon": num(tempere(1), 6),
        "ecartQuinte": num(cents(QUINTE) - 700),
        "ecartTierce": num(400 - cents(Fraction(5, 4))),
        "ecartTierceMin": num(cents(Fraction(6, 5)) - 300),
        "puissanceDouze": num(float(QUINTE) ** 12, 2),
        "spiraleFin": num(sp[-1]["pyth"]),
        "spiraleHz": num(sp[-1]["pyth"] - LA),
        # Les douze pas de l'expérience au curseur, arrondis au hertz (demi-hertz
        # vers le haut : le curseur ne prend que des entiers).
        "spiraleArrondie": ", ".join(str(int(p["pyth"] + 0.5)) for p in sp[1:-1])
                           + ", puis " + str(int(sp[-1]["pyth"] + 0.5)),
        "septiemeHarm": num(-harmoniques()[6]["ecart"], 1),
        "centHz": num(LA * (2 ** (1 / 1200) - 1), 2),
        "periodeLa": num(1000 / LA, 2),           # en millisecondes
        # Expériences au synthétiseur, avec les fréquences qu'il affiche.
        "miSynth": num(SYNTH["E5"]),
        "miJuste": num(LA * 3 / 2, 0),
        "doDSynth": num(SYNTH["C#5"]),
        "doDJuste": num(LA * 5 / 4, 0),
        "doDPyth": num(LA * float(Fraction(81, 64))),
        "battQuinte": num(abs(3 * SYNTH["A4"] - 2 * SYNTH["E5"]), 1),
        "battTierce": num(abs(5 * SYNTH["A4"] - 4 * SYNTH["C#5"]), 1),
    }
    lignes = [r"\newcommand{\%s}{%s}" % (k, s) for k, s in v.items()]
    return ecrire_tex("freq-valeurs", "\n".join(lignes) + "\n")


def main():
    verifier()
    ecrits = [
        ecrire_tex("freq-octaves", table_octaves()),
        ecrire_tex("freq-harmoniques-table", table_harmoniques()),
        ecrire_tex("freq-intervalles", table_intervalles()),
        ecrire_tex("freq-quintes", table_quintes()),
        ecrire_tex("freq-systemes", table_systemes()),
        ecrire_tex("freq-ecarts", figure_ecarts()),
        gravure_harmoniques(),
        valeurs(),
    ]
    for c in ecrits:
        print("écrit", os.path.relpath(c))


if __name__ == "__main__":
    main()
