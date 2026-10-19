#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écriture MusicXML 4.0 (format « partwise ») des gammes, des intervalles et des
ornements joués.

Un point mérite l'attention : `<alter>` porte le *son*, `<accidental>` porte ce
qui est *imprimé*. Les deux se déduisent différemment. Une altération ne
s'imprime que si elle contredit l'état courant de la mesure — lequel repart de
l'armure à chaque barre. Sans cette règle, une gamme mineure mélodique afficherait
un dièse à chaque note dièsée, ce qu'aucun éditeur n'imprimerait, et il manquerait
les bécarres d'annulation à la descente.
"""

from collections import namedtuple
from datetime import date
from fractions import Fraction
from math import lcm
from xml.sax.saxutils import escape

from gammes import LETTRES, DEMI_TONS, armure_notes

ACCIDENTAL = {-2: "flat-flat", -1: "flat", 0: "natural", 1: "sharp", 2: "double-sharp"}

ENTETE = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
          '"http://www.musicxml.org/dtds/partwise.dtd">\n')


class Mesure:
    """Suit les altérations en vigueur, pour n'imprimer que les utiles."""

    def __init__(self, armure):
        self.armure = armure
        self.reset()

    def reset(self):
        """Début de mesure : seule l'armure est en vigueur."""
        alteres = armure_notes(self.armure)
        signe = 1 if self.armure > 0 else -1
        self.etat = {L: (signe if L in alteres else 0) for L in LETTRES}

    def accidental(self, note):
        """Altération à imprimer, ou None."""
        if note.alt == self.etat[note.lettre]:
            return None
        self.etat[note.lettre] = note.alt
        return ACCIDENTAL[note.alt]


def _note_xml(note, mesure, duree=1, type_="quarter", accord=False,
              points=0, liaisons=(), poutres=(), nolet=None, marques=()):
    """
    Une note, ou un silence si `note` est None ; `accord` la joint à la
    précédente (note simultanée).

    `liaisons` : « start » et/ou « stop », pour une note liée à la suivante ou
    à la précédente. `poutres` : couples (niveau, valeur MusicXML), du niveau 1
    (les croches) au niveau 4 (les quadruples croches). `nolet` : (réelles,
    normales, crochet), le crochet valant « start », « stop » ou None, pour une
    note d'un triolet ou d'un autre groupe irrégulier. `marques` : « fermata »
    pour un point d'orgue, ou une articulation MusicXML (« staccato »,
    « accent », « tenuto »…).
    """
    acc = mesure.accidental(note) if note is not None else None
    l = [" " * 6 + "<note>"]
    if accord:
        l.append(" " * 8 + "<chord/>")
    if note is None:
        l.append(" " * 8 + "<rest/>")
    else:
        l += [" " * 8 + "<pitch>",
             " " * 10 + f"<step>{note.lettre}</step>"]
        if note.alt:
            l.append(" " * 10 + f"<alter>{note.alt}</alter>")
        l += [" " * 10 + f"<octave>{note.octave}</octave>",
              " " * 8 + "</pitch>"]
    l.append(" " * 8 + f"<duration>{duree}</duration>")
    l += [" " * 8 + f"<tie type=\"{t}\"/>" for t in liaisons]
    l += [" " * 8 + "<voice>1</voice>",
          " " * 8 + f"<type>{type_}</type>"]
    l += [" " * 8 + "<dot/>"] * points
    if acc:
        l.append(" " * 8 + f"<accidental>{acc}</accidental>")
    if nolet:
        l.append(" " * 8 + f"<time-modification><actual-notes>{nolet[0]}</actual-notes>"
                 f"<normal-notes>{nolet[1]}</normal-notes></time-modification>")
    l += [" " * 8 + f"<beam number=\"{n}\">{v}</beam>" for n, v in poutres]
    notations = [f"<tied type=\"{t}\"/>" for t in liaisons]
    if nolet and nolet[2]:
        notations.append(f"<tuplet type=\"{nolet[2]}\"/>")
    if "fermata" in marques:
        notations.append("<fermata type=\"upright\"/>")
    articulations = [f"<{a}/>" for a in marques if a != "fermata"]
    if articulations:
        notations.append("<articulations>" + "".join(articulations) + "</articulations>")
    if notations:
        l.append(" " * 8 + "<notations>" + "".join(notations) + "</notations>")
    l.append(" " * 6 + "</note>")
    return l


def _silence_xml(duree=1, type_="quarter"):
    return [" " * 6 + "<note>",
            " " * 8 + "<rest/>",
            " " * 8 + f"<duration>{duree}</duration>",
            " " * 8 + "<voice>1</voice>",
            " " * 8 + f"<type>{type_}</type>",
            " " * 6 + "</note>"]


def _debut(titre, sous_titre, partie):
    """En-tête du document, jusqu'à l'ouverture de l'unique partie."""
    return [ENTETE, '<score-partwise version="4.0">\n',
            "  <work>\n",
            f"    <work-title>{escape(titre)}</work-title>\n",
            "  </work>\n",
            "  <identification>\n",
            "    <creator type=\"composer\">Fabian Bastin</creator>\n",
            "    <rights>Licence MIT</rights>\n",
            "    <encoding>\n",
            "      <software>dépôt musique-theorie, dossier outils</software>\n",
            f"      <encoding-date>{date.today().isoformat()}</encoding-date>\n",
            "    </encoding>\n",
            f"    <miscellaneous>\n"
            f"      <miscellaneous-field name=\"description\">{escape(sous_titre)}"
            f"</miscellaneous-field>\n"
            f"    </miscellaneous>\n",
            "  </identification>\n",
            "  <part-list>\n",
            "    <score-part id=\"P1\">\n",
            f"      <part-name>{escape(partie)}</part-name>\n",
            "    </score-part>\n",
            "  </part-list>\n",
            "  <part id=\"P1\">\n"]


def partition(titre, sous_titre, entrees, partie="Gammes"):
    """
    Document MusicXML complet.

    `entrees` : liste de (libellé, armure, mode, notes). Les notes sont écrites
    en noires, quatre par mesure ; chaque entrée s'achève sur une double barre.
    Un élément de `notes` est une note, une liste de notes jouées ensemble
    (un accord, un intervalle harmonique), ou None pour un silence.
    """
    out = _debut(titre, sous_titre, partie)

    num = 0
    premiere = True
    for libelle, armure, mode, notes in entrees:
        m = Mesure(armure)
        # Les notes sont groupées par quatre ; la dernière mesure d'une entrée
        # peut être incomplète, ce que `<barline>` referme proprement.
        paquets = [notes[i:i + 4] for i in range(0, len(notes), 4)]
        for j, paquet in enumerate(paquets):
            num += 1
            out.append(f"    <measure number=\"{num}\">\n")
            if j == 0:
                out.append("      <attributes>\n")
                out.append("        <divisions>1</divisions>\n")
                out.append(f"        <key><fifths>{armure}</fifths>"
                           f"<mode>{mode}</mode></key>\n")
                if premiere:
                    out.append("        <time><beats>4</beats>"
                               "<beat-type>4</beat-type></time>\n")
                    out.append("        <clef><sign>G</sign><line>2</line></clef>\n")
                out.append("      </attributes>\n")
                out.append("      <direction placement=\"above\">\n"
                           "        <direction-type>\n"
                           f"          <words font-weight=\"bold\">{escape(libelle)}</words>\n"
                           "        </direction-type>\n"
                           "      </direction>\n")
                premiere = False
            else:
                m.reset()
            for n in paquet:
                if n is None:
                    lignes = _silence_xml()
                elif isinstance(n, (list, tuple)):
                    lignes = [x for i, k in enumerate(n) for x in _note_xml(k, m, accord=i > 0)]
                else:
                    lignes = _note_xml(n, m)
                out += [x + "\n" for x in lignes]
            if j == len(paquets) - 1:
                out.append("      <barline location=\"right\">\n"
                           "        <bar-style>light-light</bar-style>\n"
                           "      </barline>\n")
            out.append("    </measure>\n")

    out.append("  </part>\n</score-partwise>\n")
    return "".join(out)


# ---------------------------------------------------------------------------
# Notes de durées quelconques
# ---------------------------------------------------------------------------
# Valeurs en fraction de ronde. Le nombre de divisions par noire se calcule
# pour chaque document : le plus petit qui donne à chaque note une durée
# entière (huit quand la triple croche est la plus brève, un multiple de trois
# dès qu'il y a un triolet).
TYPES = {Fraction(1): "whole", Fraction(1, 2): "half", Fraction(1, 4): "quarter",
         Fraction(1, 8): "eighth", Fraction(1, 16): "16th", Fraction(1, 32): "32nd",
         Fraction(1, 64): "64th"}
POUTRES = {"eighth": 1, "16th": 2, "32nd": 3, "64th": 4}


def type_et_points(valeur):
    """(type MusicXML, nombre de points) d'une valeur ; 3/16 est une croche pointée."""
    for base, type_ in TYPES.items():
        for points in range(3):
            if base * (2 - Fraction(1, 2 ** points)) == valeur:
                return type_, points
    raise ValueError(f"valeur sans écriture simple : {valeur}")


def _poutres(types):
    """Poutres d'un groupe de notes réunies : begin, continue, end, ou crochet."""
    niveaux = [POUTRES[t] for t in types]
    res = []
    for i, n in enumerate(niveaux):
        p = []
        for niveau in range(1, n + 1):
            avant = i > 0 and niveaux[i - 1] >= niveau
            apres = i < len(niveaux) - 1 and niveaux[i + 1] >= niveau
            if avant and apres:
                p.append((niveau, "continue"))
            elif apres:
                p.append((niveau, "begin"))
            elif avant:
                p.append((niveau, "end"))
            else:
                p.append((niveau, "forward hook" if i == 0 else "backward hook"))
        res.append(p)
    return res


Nolet = namedtuple("Nolet", "reelles normales notes")
Nolet.__doc__ = """
Groupe irrégulier : `reelles` notes écrites dans le temps de `normales`
(3 pour 2 dans un triolet). Les valeurs de `notes` sont les valeurs écrites.
"""

CLES = {"G": 2, "F": 4}


def _elements(element):
    """Une entrée de groupe : (note, valeur, liée), avec ou sans ses marques."""
    note, valeur, liee, *reste = element
    return note, valeur, liee, (reste[0] if reste else ())


def _durees(entrees):
    """Durées réelles de toutes les notes, en fraction de ronde."""
    for _, _, _, _, mesures in entrees:
        for mesure in mesures:
            for groupe in mesure:
                rapport = (Fraction(groupe.normales, groupe.reelles)
                           if isinstance(groupe, Nolet) else 1)
                notes = groupe.notes if isinstance(groupe, Nolet) else groupe
                for element in notes:
                    yield _elements(element)[1] * rapport


def partition_rythmee(titre, sous_titre, entrees, partie, tempo, cle="G"):
    """
    Document MusicXML dont chaque note a sa durée.

    `entrees` : liste de (libellé, armure, mode, (temps, unité), mesures). Une
    mesure est une liste de groupes, un groupe une liste de (note, valeur,
    liée) ou de (note, valeur, liée, marques) : la valeur en fraction de ronde,
    `liée` vraie si la note se prolonge dans la suivante, `marques` comme pour
    `_note_xml`. Une note peut être None (un silence) ou une liste de notes
    jouées ensemble (un accord). Un groupe peut aussi être un `Nolet`. Les notes
    d'un groupe de plus d'une note sont réunies par des poutres. Chaque entrée
    s'achève sur une double barre ; un libellé vide prolonge l'entrée
    précédente, sous une autre armure. `cle` : « G » (clé de sol) ou « F »
    (clé de fa).
    """
    divisions = lcm(*((d * 4).denominator for d in _durees(entrees)))
    out = _debut(titre, sous_titre, partie)
    num = 0
    chiffrage = None
    for libelle, armure, mode, temps, mesures in entrees:
        m = Mesure(armure)
        # Une liaison peut franchir la barre : la note qui la reçoit, au début
        # de la mesure suivante, en porte la fin.
        lie = False
        for j, mesure in enumerate(mesures):
            num += 1
            out.append(f"    <measure number=\"{num}\">\n")
            if j == 0:
                out.append("      <attributes>\n")
                if num == 1:
                    out.append(f"        <divisions>{divisions}</divisions>\n")
                out.append(f"        <key><fifths>{armure}</fifths>"
                           f"<mode>{mode}</mode></key>\n")
                if temps != chiffrage:
                    out.append(f"        <time><beats>{temps[0]}</beats>"
                               f"<beat-type>{temps[1]}</beat-type></time>\n")
                    chiffrage = temps
                if num == 1:
                    out.append(f"        <clef><sign>{cle}</sign><line>{CLES[cle]}</line></clef>\n")
                out.append("      </attributes>\n")
                if num == 1:
                    out.append("      <direction placement=\"above\">\n"
                               "        <direction-type>\n"
                               "          <metronome><beat-unit>quarter</beat-unit>"
                               f"<per-minute>{tempo}</per-minute></metronome>\n"
                               "        </direction-type>\n"
                               f"        <sound tempo=\"{tempo}\"/>\n"
                               "      </direction>\n")
                if libelle:
                    out.append("      <direction placement=\"above\">\n"
                               "        <direction-type>\n"
                               f"          <words font-weight=\"bold\">{escape(libelle)}</words>\n"
                               "        </direction-type>\n"
                               "      </direction>\n")
            else:
                m.reset()
            for groupe in mesure:
                nolet = isinstance(groupe, Nolet)
                notes = [_elements(e) for e in (groupe.notes if nolet else groupe)]
                rapport = Fraction(groupe.normales, groupe.reelles) if nolet else 1
                types = [type_et_points(v) for _, v, _, _ in notes]
                poutres = (_poutres([t for t, _ in types])
                           if len(notes) > 1 and all(t in POUTRES for t, _ in types)
                           else [()] * len(notes))
                for i, ((note, valeur, liee, marques), (type_, points), p) in enumerate(
                        zip(notes, types, poutres)):
                    liaisons = (["stop"] if lie else []) + (["start"] if liee else [])
                    crochet = "start" if i == 0 else "stop" if i == len(notes) - 1 else None
                    duree = valeur * rapport * 4 * divisions
                    accord = note if isinstance(note, (list, tuple)) else [note]
                    for k, n in enumerate(accord):
                        out += [x + "\n" for x in _note_xml(
                            n, m, duree=int(duree), type_=type_, accord=k > 0,
                            points=points, liaisons=liaisons, poutres=p,
                            nolet=(groupe.reelles, groupe.normales, crochet) if nolet else None,
                            marques=marques)]
                    lie = liee
            if j == len(mesures) - 1:
                out.append("      <barline location=\"right\">\n"
                           "        <bar-style>light-light</bar-style>\n"
                           "      </barline>\n")
            out.append("    </measure>\n")

    out.append("  </part>\n</score-partwise>\n")
    return "".join(out)
