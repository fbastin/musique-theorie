#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les fichiers MusicXML et les gravures LilyPond du guide des gammes.

    python3 outils/generer.py [--musicxml] [--lily]

Sans option, tout est régénéré. Les deux sorties viennent du même modèle de
hauteurs (`gammes.py`) : le PDF et les fichiers MusicXML ne peuvent donc pas
se contredire.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import (GAMMES, NOMS_FR, ORDRE_BEMOLS, ORDRE_DIESES, TETRACORDES,
                    TONALITES, Note, armure_notes, gamme, intervalles, note_de,
                    octave_depart, tetracorde)
from intervalles import analyser, au_dessus
import musicxml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_LY = os.path.join(RACINE, "gravures")

MODE_XML = {"majeure": "major", "mineure naturelle": "minor",
            "mineure harmonique": "minor", "mineure mélodique": "minor"}


# ---------------------------------------------------------------------------
# Suites de notes
# ---------------------------------------------------------------------------
def montee_descente(tonique, nom_gamme):
    """
    Gamme montante puis descendante, seize noires.

    La mineure mélodique descend sous sa forme naturelle : c'est sa définition
    classique, et la seule façon de rendre son asymétrie visible. Les autres
    gammes descendent comme elles montent, ce que le contraste met en relief.
    """
    montee = gamme(tonique, nom_gamme)
    if nom_gamme == "mineure mélodique":
        descente = list(reversed(gamme(tonique, "mineure naturelle")))
    else:
        descente = list(reversed(montee))
    return montee + descente


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
def ecrire_musicxml():
    familles = [
        ("gammes-majeures", "Gammes majeures",
         "Les quinze tonalités majeures, montantes et descendantes.",
         "majeure", 1),
        ("gammes-mineures-naturelles", "Gammes mineures naturelles",
         "Les quinze tonalités mineures sous leur forme naturelle : "
         "mêmes notes que la majeure relative, tonique différente.",
         "mineure naturelle", 2),
        ("gammes-mineures-harmoniques", "Gammes mineures harmoniques",
         "Septième degré haussé d'un demi-ton : la sensible apparaît, "
         "au prix d'une seconde augmentée entre les degrés 6 et 7.",
         "mineure harmonique", 2),
        ("gammes-mineures-melodiques", "Gammes mineures mélodiques",
         "Sixième et septième degrés haussés à la montée, forme naturelle "
         "à la descente.",
         "mineure mélodique", 2),
    ]
    produits = []
    for nom, titre, desc, type_gamme, col in familles:
        entrees = []
        for armure, maj, min_ in TONALITES:
            tonique_txt = maj if col == 1 else min_
            tonique = note_de(tonique_txt, 4)
            tonique = Note(tonique.lettre, tonique.alt, octave_depart(tonique))
            libelle = f"{tonique.nom_fr()} {type_gamme}"
            entrees.append((libelle, armure, MODE_XML[type_gamme],
                            montee_descente(tonique, type_gamme)))
        chemin = os.path.join(RACINE, nom + ".musicxml")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(musicxml.partition(titre, desc, entrees))
        produits.append(chemin)

    # Les tétracordes, sur do, pour comparer les quatre types à vue.
    entrees = []
    for type_, pas in TETRACORDES.items():
        notes = tetracorde(note_de("C", 4), type_)
        entrees.append((f"tétracorde {type_}", 0, "major", notes))
    chemin = os.path.join(RACINE, "tetracordes.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition(
            "Tétracordes",
            "Les cinq types de tétracordes, tous à partir de do, "
            "pour comparer leurs intervalles à vue.", entrees))
    produits.append(chemin)
    return produits


# ---------------------------------------------------------------------------
# LilyPond
# ---------------------------------------------------------------------------
PREAMBULE = r"""\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
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


# Préambule des planches de référence.
#
# Deux réglages les distinguent des figures didactiques. La largeur de ligne est
# *fixée* et la justification rétablie : sans cela, chaque gamme sortait à sa
# largeur naturelle — 154 pt pour do majeur, 202 pt pour la dièse mineur
# harmonique, dont l'armure est plus encombrante. Les mettre toutes à la largeur
# de la colonne aurait alors imposé des facteurs d'échelle différents, et des
# portées de tailles différentes sur une même page.
#
# 79 mm est la largeur de colonne du guide (0,48 × textwidth = 226,7 pt), à un
# cheveu près pour que l'ajustement final soit un agrandissement infime plutôt
# qu'une réduction.
#
# La taille de portée passe de 20 à 24 : les planches n'occupaient que les deux
# tiers de leur page, la place était disponible.
PREAMBULE_REF = r"""\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
#(set-global-staff-size 24)
\paper {
  indent = 0
  ragged-right = ##f
  %% Les trois doivent s'accorder : LilyPond rejette une largeur de ligne qui ne
  %% s'ajuste pas aux marges et revient silencieusement à ses valeurs par défaut
  %% (« margins do not fit with line-width »). D'où la largeur de page explicite.
  paper-width = 81\mm
  line-width = 79\mm
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


def ly_notes(notes):
    return " ".join(n.lily() for n in notes)


def ecrire(nom, contenu, preambule=None):
    os.makedirs(DIR_LY, exist_ok=True)
    chemin = os.path.join(DIR_LY, nom + ".ly")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write((preambule or PREAMBULE) + contenu)
    return chemin


def portee(notes, armure=0, mode="major", ancrages=""):
    return (r"""\score {
  \new Staff {
    \clef treble
    \key %s \%s
    \omit Staff.TimeSignature
    \cadenzaOn
    %s
    \bar "|."
  }
  \layout { }
}
""" % (_lily_tonique(armure, mode), mode, ancrages or ly_notes(notes)))


def _lily_tonique(armure, mode):
    """Tonique correspondant à l'armure, pour la commande \\key de LilyPond."""
    for k, maj, min_ in TONALITES:
        if k == armure:
            return note_de(maj if mode == "major" else min_, 4).lily().rstrip("',")
    return "c"


ENTETE_PORTEE = r"""\score {
  \new Staff \with {
    \consists "Horizontal_bracket_engraver"
    \override HorizontalBracket.direction = #DOWN
    \override HorizontalBracketText.font-size = #-3
    \override HorizontalBracketText.font-shape = #'italic
  } {
    %% Sans barres de mesure, une altération reste en vigueur jusqu'à la fin de
    %% la figure : le ré bémol du tétracorde phrygien n'était pas réimprimé sur
    %% la ligne du tétracorde harmonique, qui se lisait donc « do ré mi fa » —
    %% l'orthographe du tétracorde majeur. Même effet sur la mineure mélodique,
    %% dont le sol dièse disparaissait et qui se lisait en mode dorien.
    %% `forget` réimprime chaque altération par rapport à l'armure, sans
    %% mémoire de ce qui précède : chaque ligne se lit alors seule.
    \accidentalStyle forget
    \clef treble
    \omit Staff.TimeSignature
    \cadenzaOn
"""

PIED_PORTEE = r"""    \bar "|."
  }
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.2
    }
  }
}
"""


def crochet(libelle):
    """Ouvre un crochet d'analyse portant `libelle` sous les notes groupées."""
    return ('    \\once \\override Staff.HorizontalBracketText.text = "%s"\n'
            % libelle)


def groupe(notes, libelle):
    """Notes encadrées par un crochet d'analyse légendé."""
    n = [x.lily() for x in notes]
    return (crochet(libelle)
            + "    " + n[0] + "\\startGroup "
            + " ".join(n[1:-1]) + " " + n[-1] + "\\stopGroup\n")


def figure_do_majeur():
    """Do majeur, ses deux tétracordes et le ton disjonctif qui les sépare."""
    g = gamme(note_de("C", 4), "majeure")
    corps = "    \\key c \\major\n"
    corps += groupe(g[0:4], "inférieur")
    # Le ton disjonctif relie fa à sol ; il n'appartient à aucun tétracorde,
    # et c'est tout son intérêt. Un crochet le recouvrirait, on l'annote.
    corps = corps.replace(
        g[3].lily() + "\\stopGroup",
        "\\once \\override TextScript.extra-offset = #'(3.2 . 0) "
        + g[3].lily() + "\\stopGroup^\\markup\\tiny \\italic "
        "\"ton disjonctif\"")
    corps += groupe(g[4:8], "supérieur")
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_quatre_tetracordes():
    """Les quatre tétracordes utiles, tous à partir de do, pour comparaison."""
    corps = "    \\key c \\major\n"
    for type_ in ("majeur", "mineur", "phrygien", "harmonique"):
        corps += groupe(tetracorde(note_de("C", 4), type_), type_)
        corps += "    \\bar \"\" \\break\n"
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_chaine_quintes():
    """
    Le tétracorde supérieur de do majeur est le tétracorde inférieur de sol.

    C'est le mécanisme du cycle des quintes : on ne choisit pas d'ajouter un
    dièse, on le subit — le tétracorde supérieur de la nouvelle gamme exige
    un fa dièse pour rester majeur.
    """
    do = gamme(note_de("C", 4), "majeure")
    sol = gamme(note_de("G", 4), "majeure")
    corps = "    \\key c \\major\n"
    corps += groupe(do[0:4], "inférieur")
    corps += groupe(do[4:8], "supérieur")
    corps += "    \\bar \"||\" \\break\n"
    corps += "    \\key g \\major\n"
    corps += groupe(sol[0:4], "inférieur")
    corps += groupe(sol[4:8], "supérieur")
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_la_mineures():
    """Les trois formes de la mineure, l'une sous l'autre."""
    corps = ""
    for i, (nom, libelle) in enumerate((("mineure naturelle", "naturelle"),
                                        ("mineure harmonique", "harmonique"),
                                        ("mineure mélodique", "mélodique"))):
        g = gamme(note_de("A", 3), nom)
        if i == 0:
            corps += "    \\key a \\minor\n"
        corps += groupe(g, libelle)
        if i < 2:
            corps += "    \\bar \"\" \\break\n"
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_seconde_augmentee():
    """L'intervalle qui fait le caractère — et le problème — de l'harmonique."""
    g = gamme(note_de("A", 3), "mineure harmonique")
    corps = "    \\key a \\minor\n"
    corps += "    " + " ".join(x.lily() for x in g[0:5]) + "\n"
    corps += groupe(g[5:7], "2de aug.")
    corps += "    " + g[7].lily() + "\n"
    return ENTETE_PORTEE + corps + PIED_PORTEE


# Un libellé par note, et non un découpage en syllabes : dans LilyPond, chaque
# syllabe séparée par `--` consomme une note. Les vingt-six syllabes des huit
# noms se répartissaient donc sur les huit notes, et la figure affichait
# « to – ni – que sus – to – ni – que mé ». Les noms composés sont mis entre
# guillemets pour que le trait d'union ne soit pas lu comme un séparateur.
DEGRES_FR = ['tonique', '"sus-tonique"', 'médiante', '"sous-dominante"',
             'dominante', '"sus-dominante"', 'sensible', 'tonique']


def figure_degres():
    """Do majeur avec le nom français de chaque degré."""
    g = gamme(note_de("C", 4), "majeure")
    notes = " ".join(x.lily() for x in g)
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
      \override SpacingSpanner.spacing-increment = #2.2
    }
    \context { \Lyrics \override LyricText.font-size = #-2.5 }
  }
}
""" % (notes, " ".join(DEGRES_FR))


# Rouge de l'accent du guide (\definecolor{accent}{RGB}{150,40,30}).
ACCENT_LY = "#(rgb-color 0.588 0.157 0.118)"

# Une armure est un seul objet graphique : LilyPond ne sait pas en colorer un
# signe isolé. On la dessine donc deux fois, superposées — entière en couleur,
# puis sans le nouveau signe, en noir. Seul ce dernier reste coloré.
#
# La superposition tombe juste parce que le nouveau signe est toujours le
# dernier de l'armure : les autres gardent leur place quand on le retire.
ARMURE_COLOREE = r"""#(define (armure-nouveau-signe pas couleur)
   (lambda (grob)
     (let* ((alist (ly:grob-property grob 'alteration-alist))
            (reste (filter (lambda (e) (not (eqv? (car e) pas))) alist))
            (tout (stencil-with-color
                   (ly:key-signature-interface::print grob) couleur)))
       (if (null? reste)
           tout
           (begin
             (ly:grob-set-property! grob 'alteration-alist reste)
             (let ((ancien (ly:key-signature-interface::print grob)))
               (ly:grob-set-property! grob 'alteration-alist alist)
               (ly:stencil-add tout ancien)))))))

"""


def figure_chaine(sens):
    """
    Les huit gammes d'une chaîne de quintes, une par ligne, de do à sept
    altérations. Vers les dièses si `sens` = 1, vers les bémols si `sens` = -1.

    Chaque gamme porte sa propre armure. Le signe que la construction vient
    d'y ajouter est en couleur, comme la note qu'il affecte ; celle-ci ne
    porte pas d'altération, puisque l'armure la donne déjà. La chaîne vient
    de `chaine_tetracordes`, qui a vérifié qu'une seule note change à chaque
    étape.
    """
    # La sensible vers les dièses, la sous-dominante vers les bémols.
    degre = 6 if sens > 0 else 3
    corps = ("    \\set Staff.printKeyCancellation = ##f\n"
             "    \\set Staff.explicitKeySignatureVisibility = #end-of-line-invisible\n")
    chaine = chaine_tetracordes(sens)
    for i, (g, alteree) in enumerate(chaine):
        t = Note(g[0].lettre, g[0].alt, octave_depart(g[0]))
        notes = [n.lily() for n in gamme(t, "majeure")]
        nom = t.nom_fr()
        corps += "    \\set Staff.%s = \\markup \\small \"%s\"\n" % (
            "instrumentName" if i == 0 else "shortInstrumentName", nom)
        if alteree is not None:
            notes[degre] = ("\\tweak color %s \\tweak Stem.color %s %s"
                            % (ACCENT_LY, ACCENT_LY, notes[degre]))
            corps += ("    \\once \\override Staff.KeySignature.stencil = "
                      "#(armure-nouveau-signe %d %s)\n"
                      % (alteree.idx, ACCENT_LY[1:]))
        corps += "    \\key %s \\major\n" % _lily_tonique(sens * i, "major")
        for moitie, libelle in ((notes[0:4], "inférieur"), (notes[4:8], "supérieur")):
            corps += (crochet(libelle) + "    " + moitie[0] + "\\startGroup "
                      + " ".join(moitie[1:3]) + " " + moitie[3] + "\\stopGroup\n")
        if i < len(chaine) - 1:
            corps += "    \\bar \"\" \\break\n"
    # Le nom de la gamme en marge exige un retrait ; `indent` vaut 0 dans le
    # préambule commun, on le rétablit pour cette figure seulement.
    pied = PIED_PORTEE.replace(
        "  \\layout {\n",
        "  \\layout {\n    indent = 18\\mm\n    short-indent = 18\\mm\n", 1)
    return ARMURE_COLOREE + ENTETE_PORTEE + corps + pied


FIGURES = {
    "f-do-majeur": figure_do_majeur,
    "f-quatre-tetracordes": figure_quatre_tetracordes,
    "f-chaine-quintes": figure_chaine_quintes,
    "f-la-mineures": figure_la_mineures,
    "f-seconde-augmentee": figure_seconde_augmentee,
    "f-degres": figure_degres,
    "f-chaine-dieses": lambda: figure_chaine(1),
    "f-chaine-bemols": lambda: figure_chaine(-1),
}


def ecrire_figures():
    return [ecrire(nom, fabrique()) for nom, fabrique in FIGURES.items()]


def ecrire_lilypond():
    produits = []

    # --- une gamme par fichier, pour les tableaux de référence -------------
    for armure, maj, min_ in TONALITES:
        for type_gamme, col, prefixe in (("majeure", 1, "maj"),
                                         ("mineure naturelle", 2, "min-nat"),
                                         ("mineure harmonique", 2, "min-harm"),
                                         ("mineure mélodique", 2, "min-mel")):
            txt = maj if col == 1 else min_
            t = note_de(txt, 4)
            t = Note(t.lettre, t.alt, octave_depart(t))
            notes = gamme(t, type_gamme)
            mode = "major" if col == 1 else "minor"
            slug = txt.replace("#", "d").replace("b", "b").lower()
            produits.append(ecrire(f"{prefixe}-{slug}",
                                   portee(notes, armure, mode),
                                   preambule=PREAMBULE_REF))

    return produits


# ---------------------------------------------------------------------------
# Tableaux LaTeX
# ---------------------------------------------------------------------------
def _armure_txt(k):
    if k == 0:
        return "---"
    return f"{abs(k)}~{'dièse' if k > 0 else 'bémol'}{'s' if abs(k) > 1 else ''}"


def _notes_txt(notes):
    """Les sept degrés, séparés par des espaces insécables fines."""
    return " -- ".join(n.nom_fr() for n in notes[:-1])


def ecrire_tables():
    """
    Tableaux de référence, engendrés depuis le modèle.

    Les saisir à la main garantirait une coquille quelque part parmi les
    420 notes des soixante gammes.
    """
    l = ["%% Produit par outils/generer.py — ne pas modifier à la main.", ""]

    # --- les quinze tonalités majeures -----------------------------------
    l += [r"\begin{longtable}{@{}l l >{\raggedright\arraybackslash}p{9.4cm}@{}}",
          r"\toprule",
          r"\textbf{Tonique} & \textbf{Armure} & \textbf{Degrés} \\",
          r"\midrule", r"\endhead"]
    for armure, maj, _ in TONALITES:
        t = note_de(maj, 4)
        g = gamme(t, "majeure")
        l.append(f"{t.nom_fr()} & {_armure_txt(armure)} & {_notes_txt(g)} \\\\")
    l += [r"\bottomrule", r"\end{longtable}", ""]

    # --- les mineures, trois formes --------------------------------------
    for nom_gamme, titre in (("mineure naturelle", "naturelles"),
                             ("mineure harmonique", "harmoniques"),
                             ("mineure mélodique", "mélodiques (forme ascendante)")):
        l.append(r"\subsection{Gammes mineures %s}" % titre)
        l += [r"\begin{longtable}{@{}l l >{\raggedright\arraybackslash}p{9.4cm}@{}}",
              r"\toprule",
              r"\textbf{Tonique} & \textbf{Armure} & \textbf{Degrés} \\",
              r"\midrule", r"\endhead"]
        for armure, _, min_ in TONALITES:
            t = note_de(min_, 4)
            g = gamme(t, nom_gamme)
            l.append(f"{t.nom_fr()} & {_armure_txt(armure)} & {_notes_txt(g)} \\\\")
        l += [r"\bottomrule", r"\end{longtable}", ""]

    chemin = os.path.join(DIR_LY, "tables.tex")
    os.makedirs(DIR_LY, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(l) + "\n")
    return chemin


def ecrire_table_tetracordes():
    """Le tableau qui porte la thèse : chaque gamme, ses deux tétracordes."""
    nom_pas = {1: "½ ton", 2: "ton", 3: "1 ½ ton"}
    l = ["%% Produit par outils/generer.py — ne pas modifier à la main.", ""]
    l += [r"\begin{tabular}{@{}l l l@{}}", r"\toprule",
          r"\textbf{Tétracorde} & \textbf{Intervalles} & \textbf{Exemple sur do} \\",
          r"\midrule"]
    for type_, pas in TETRACORDES.items():
        notes = tetracorde(note_de("C", 4), type_)
        inter = " -- ".join(nom_pas[x] for x in pas)
        l.append(f"{type_} & {inter} & {_notes_txt(notes)} -- {notes[-1].nom_fr()} \\\\")
    l += [r"\bottomrule", r"\end{tabular}", ""]

    l += ["", r"\begin{tabular}{@{}l l l@{}}", r"\toprule",
          r"\textbf{Gamme} & \textbf{Tétracorde inférieur} & \textbf{Tétracorde supérieur} \\",
          r"\midrule"]
    for nom_gamme, (bas, haut) in GAMMES.items():
        l.append(f"{nom_gamme} & {bas} & {haut} \\\\")
    l += [r"\bottomrule", r"\end{tabular}", ""]

    coupure = l.index(r"\begin{tabular}{@{}l l l@{}}", 3)
    chemins = []
    for nom, bloc in (("tetracordes-types", l[:coupure]),
                      ("tetracordes-gammes", l[:2] + l[coupure:])):
        chemin = os.path.join(DIR_LY, nom + ".tex")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("\n".join(bloc) + "\n")
        chemins.append(chemin)
    return chemins


def _meme_hauteur_ecrite(a, b):
    """Même lettre, même altération ; l'octave est indifférente."""
    return a.lettre == b.lettre and a.alt == b.alt


def chaine_tetracordes(sens):
    """
    Refait la construction de proche en proche, à partir de do majeur.

    Vers les dièses (`sens` = 1), le tétracorde supérieur devient l'inférieur
    de la gamme une quinte au-dessus ; vers les bémols (`sens` = -1),
    l'inférieur devient le supérieur de la gamme une quinte au-dessous. Le
    tétracorde à bâtir reprend les lettres de l'ancienne gamme — degrés 2 à 5
    vers les dièses, 4 à 7 vers les bémols — et une seule de ses notes doit
    changer pour qu'il soit majeur. On vérifie que c'est bien le cas, et
    laquelle.

    Renvoie la liste des (gamme, note altérée). L'ordre des altérations n'est
    donc pas recopié : il est *retrouvé*, puis comparé à celui des armures.
    """
    g = gamme(note_de("C", 4), "majeure")
    chaine = [(g, None)]
    for _ in range(7):
        if sens > 0:
            ng = gamme(g[4], "majeure")
            garde, herite = ng[0:4], g[4:8]
            cree, lettres, pos = ng[4:8], g[1:5], 2   # la 3e note, future sensible
        else:
            ng = gamme(g[3], "majeure")
            garde, herite = ng[4:8], g[0:4]
            cree, lettres, pos = ng[0:4], g[3:7], 3   # la 4e, future sous-dominante
        assert all(map(_meme_hauteur_ecrite, garde, herite))
        diff = [i for i in range(4) if not _meme_hauteur_ecrite(cree[i], lettres[i])]
        assert diff == [pos] and cree[pos].alt - lettres[pos].alt == sens, diff
        chaine.append((ng, cree[pos]))
        g = ng
    trouve = "".join(n.lettre for _, n in chaine[1:])
    assert trouve == (ORDRE_DIESES if sens > 0 else ORDRE_BEMOLS), trouve
    return chaine


# ---------------------------------------------------------------------------
# Lire une armure
# ---------------------------------------------------------------------------
def _meme_note(a, b):
    return _meme_hauteur_ecrite(a, b)


def _quinte(n):
    """La quinte juste au-dessus, ramenée à l'octave 4 : seule l'écriture compte."""
    q = au_dessus(n, 5, "juste")
    return Note(q.lettre, q.alt, 4)


# Degrés d'une gamme majeure rangée de quinte en quinte : fa do sol ré la mi si
# pour do majeur. La thèse de la dernière sous-section de « Lire une armure ».
DEGRES_EN_QUINTES = (4, 1, 5, 2, 6, 3, 7)


def ligne_des_quintes(depart="Fb", longueur=21):
    """De fa bémol à si dièse : toutes les notes des quinze armures, en quintes."""
    ligne = [note_de(depart, 4)]
    while len(ligne) < longueur:
        ligne.append(_quinte(ligne[-1]))
    return ligne


def lire_armures():
    """
    Les règles de lecture des armures, refaites et vérifiées sur les quinze
    tonalités, avant d'écrire le moindre tableau. Le texte du guide les énonce ;
    rien ici n'est recopié de lui.

    Renvoie, par armure, un dict : dernière altération, avant-dernière, tonique
    majeure, relatif mineur, sensible du mineur (altération accidentelle).
    """
    ligne = ligne_des_quintes()
    lignes = {}
    for armure, maj, min_ in TONALITES:
        g = gamme(note_de(maj, 4), "majeure")          # g[0] … g[7]
        alterees = armure_notes(armure)                 # lettres, dans l'ordre de l'armure
        sens = 1 if armure > 0 else -1

        # L'armure est bien celle de la gamme : les lettres altérées, et elles seules.
        assert sorted(n.lettre for n in g[:7] if n.alt) == sorted(alterees), maj
        assert all(n.alt in (0, sens) for n in g[:7]), maj

        # Relatif mineur : le sixième degré, une tierce mineure sous la tonique.
        rel = g[5]
        assert _meme_note(rel, note_de(min_)), (maj, min_)
        assert analyser(g[5], g[7]) == (3, "mineure"), maj

        # Sensible du mineur (formes harmonique et mélodique) : la dominante de la
        # majeure, haussée d'un demi-ton. Jamais dans l'armure.
        hm = gamme(Note(rel.lettre, rel.alt, 4), "mineure harmonique")
        sens_min = hm[6]
        assert sens_min.lettre == g[4].lettre and sens_min.alt == g[4].alt + 1, maj
        assert analyser(hm[6], hm[7]) == (2, "mineure"), maj

        d = {"armure": armure, "tonique": g[0], "relatif": rel,
             "sensible_min": sens_min, "derniere": None, "avant_derniere": None}

        if armure > 0:
            # Le dernier dièse est la sensible (degré 7) ; la tonique est une
            # seconde mineure au-dessus, sur la lettre suivante ; le relatif, une
            # seconde majeure au-dessous, sur la lettre précédente.
            der = g[6]
            assert der.lettre == alterees[-1] and der.alt == 1, maj
            assert analyser(g[6], g[7]) == (2, "mineure"), maj
            assert analyser(g[5], g[6]) == (2, "majeure"), maj
            d["derniere"] = der
        elif armure < 0:
            # Le dernier bémol est la sous-dominante (degré 4), une quarte juste
            # au-dessus de la tonique ; l'avant-dernier bémol est la tonique —
            # sauf à un bémol, où la tonique (fa) n'est pas altérée.
            der = g[3]
            assert der.lettre == alterees[-1] and der.alt == -1, maj
            assert analyser(g[0], g[3]) == (4, "juste"), maj
            d["derniere"] = der
            if armure <= -2:
                assert g[0].lettre == alterees[-2] and g[0].alt == -1, maj
                d["avant_derniere"] = g[0]
            else:
                assert g[0].alt == 0, maj

        # La même chose, lue sur la ligne des quintes : la gamme y occupe sept
        # cases consécutives, degrés 4 1 5 2 6 3 7, décalées d'une case par
        # dièse vers la droite, d'une case par bémol vers la gauche.
        i = next(k for k, n in enumerate(ligne) if _meme_note(n, g[3]))
        assert i == 7 + armure, maj                     # do majeur commence à fa, case 7
        fenetre = ligne[i:i + 7]
        attendu = [g[deg - 1] for deg in DEGRES_EN_QUINTES]
        assert all(map(_meme_note, fenetre, attendu)), maj
        # Les altérées sont les |armure| dernières cases (dièses) ou premières (bémols).
        alt_fen = [k for k, n in enumerate(fenetre) if n.alt]
        attendu_k = list(range(7 - armure, 7)) if armure > 0 else list(range(-armure))
        assert alt_fen == attendu_k, maj

        lignes[armure] = d
    return lignes


def _nom_accidentel(note, armure):
    """Le nom de l'altération à écrire : bécarre quand elle annule un bémol de l'armure."""
    if note.alt == 0 and armure < 0 and note.lettre in armure_notes(armure):
        return note.nom_fr() + " bécarre"
    return note.nom_fr()


def _court(n):
    """Écriture compacte, pour la ligne des quintes : la$\\flat$, fa$\\sharp$."""
    signe = {-2: r"$\flat\flat$", -1: r"$\flat$", 0: "", 1: r"$\sharp$", 2: r"$\times$"}
    return NOMS_FR[n.lettre] + signe[n.alt]


def _entete(*titres):
    """Ligne d'en-tête ; les titres de plusieurs mots sur deux lignes, pour tenir
    six colonnes dans la largeur de la page."""
    cases = []
    for t in titres:
        mots = t.split(" ", 1)
        txt = t if len(mots) == 1 else r"\shortstack[l]{%s\\%s}" % tuple(mots)
        cases.append(r"\textbf{%s}" % txt)
    return " & ".join(cases) + r" \\"


def ecrire_tables_armures():
    """Les deux tableaux de lecture des armures, et la ligne des quintes."""
    a = lire_armures()
    entete = ["%% Produit par outils/generer.py — ne pas modifier à la main.", ""]
    chemins = []

    l = entete + [r"\begin{tabular}{@{}l l l l l@{}}", r"\toprule",
                  _entete("Armure", "Dernier dièse", "Tonique majeure", "Relatif mineur",
                          "Sensible du mineur"),
                  r"\midrule"]
    for k in range(1, 8):
        d = a[k]
        l.append(f"{_armure_txt(k)} & {d['derniere'].nom_fr()} & {d['tonique'].nom_fr()}"
                 f" & {d['relatif'].nom_fr()} & {_nom_accidentel(d['sensible_min'], k)} \\\\")
    l += [r"\bottomrule", r"\end{tabular}", ""]
    chemins.append(("armures-dieses", l))

    l = entete + [r"\begin{tabular}{@{}l l l l l l@{}}", r"\toprule",
                  _entete("Armure", "Dernier bémol", "Avant-dernier bémol",
                          "Tonique majeure", "Relatif mineur", "Sensible du mineur"),
                  r"\midrule"]
    for k in range(-1, -8, -1):
        d = a[k]
        avant = d["avant_derniere"].nom_fr() if d["avant_derniere"] else "---"
        l.append(f"{_armure_txt(k)} & {d['derniere'].nom_fr()} & {avant}"
                 f" & {d['tonique'].nom_fr()} & {d['relatif'].nom_fr()}"
                 f" & {_nom_accidentel(d['sensible_min'], k)} \\\\")
    l += [r"\bottomrule", r"\end{tabular}", ""]
    chemins.append(("armures-bemols", l))

    # La ligne des quintes, de la bémol à sol dièse, avec deux fenêtres : la
    # majeur (3 dièses) et mi bémol majeur (3 bémols). En couleur, les degrés
    # que désignent les règles : la sensible, la sous-dominante, la tonique.
    ligne = ligne_des_quintes()[4:17]
    l = entete + [r"{\small\setlength{\tabcolsep}{4.2pt}%",
                  r"\begin{tabular}{@{}l*{%d}{c}@{}}" % len(ligne), r"\toprule",
                  " & " + " & ".join(_court(n) for n in ligne) + r" \\", r"\midrule"]
    for armure, marques in ((3, {7}), (-3, {4, 1})):
        d = a[armure]
        g = gamme(d["tonique"], "majeure")
        cases = []
        for n in ligne:
            deg = next((DEGRES_EN_QUINTES[j] for j, x in
                        enumerate(g[deg - 1] for deg in DEGRES_EN_QUINTES)
                        if _meme_note(x, n)), None)
            if deg is None:
                cases.append("")
            elif deg in marques:
                cases.append(r"\textcolor{accent}{\textbf{%d}}" % deg)
            elif n.alt:
                cases.append(r"\textbf{%d}" % deg)
            else:
                cases.append(str(deg))
        l.append(f"{d['tonique'].nom_fr()} majeur ({_armure_txt(armure)}) & "
                 + " & ".join(cases) + r" \\")
    l += [r"\bottomrule", r"\end{tabular}}", ""]
    chemins.append(("armures-quintes", l))

    sorties = []
    for nom, bloc in chemins:
        chemin = os.path.join(DIR_LY, nom + ".tex")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("\n".join(bloc) + "\n")
        sorties.append(chemin)
    return sorties


def ecrire_planches():
    """
    Planches de gammes gravées, deux par ligne.

    Engendrées plutôt qu'écrites à la main : soixante appels à
    \\gammeref saisis manuellement seraient soixante occasions de se tromper
    de fichier ou de libellé.
    """
    familles = [("planche-majeures", "maj", 1, "majeure"),
                ("planche-min-nat", "min-nat", 2, "mineure naturelle"),
                ("planche-min-harm", "min-harm", 2, "mineure harmonique"),
                ("planche-min-mel", "min-mel", 2, "mineure mélodique")]
    chemins = []
    for nom, prefixe, col, libelle in familles:
        l = ["%% Produit par outils/generer.py — ne pas modifier à la main.", ""]
        for i, (armure, maj, min_) in enumerate(TONALITES):
            txt = maj if col == 1 else min_
            slug = txt.replace("#", "d").lower()
            t = note_de(txt, 4)
            l.append("\\gammeref{%s-%s}{%s}%%" % (prefixe, slug, t.nom_fr()))
            if i % 2 == 1:
                l.append("")
        chemin = os.path.join(DIR_LY, nom + ".tex")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("\n".join(l) + "\n")
        chemins.append(chemin)
    return chemins


if __name__ == "__main__":
    quoi = set(a for a in sys.argv[1:])
    tout = not quoi
    if tout or "--musicxml" in quoi:
        f = ecrire_musicxml()
        print(f"MusicXML : {len(f)} fichiers")
        for x in f:
            print("  ", os.path.relpath(x, RACINE))
    if tout or "--tex" in quoi:
        print("Tableaux :", os.path.relpath(ecrire_tables(), RACINE))
        for c in ecrire_table_tetracordes():
            print("Tableaux :", os.path.relpath(c, RACINE))
        for c in ecrire_tables_armures():
            print("Tableaux :", os.path.relpath(c, RACINE))
        for c in ecrire_planches():
            print("Planches :", os.path.relpath(c, RACINE))
    if tout or "--lily" in quoi:
        f = ecrire_figures()
        print(f"LilyPond : {len(f)} figures didactiques")
        f = ecrire_lilypond()
        print(f"LilyPond : {len(f)} gammes de référence")
