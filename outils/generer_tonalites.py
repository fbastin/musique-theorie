#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les gravures, les tableaux, les réponses des exercices et le fichier
MusicXML du guide « Les tonalités ».

    python3 outils/generer_tonalites.py

Une tonalité y est un couple (tonique, mode). Son armure, son relatif, son
homonyme et ses tons voisins s'en déduisent sur le modèle de hauteurs des
autres guides (`gammes.py`, `intervalles.py`) ; une transposition déplace
chaque note d'un même intervalle ; un mode ancien fait tourner la gamme
majeure. Les affirmations du texte — les tons voisins à une altération près,
les notes modales qui seules changent d'un mode à l'autre, la transposition
qui conserve les intervalles et l'effet des altérations, l'échelle des modes
sur ré qui perd une altération à chaque marche — sont vérifiées avant toute
écriture.
"""

import os
import sys
from collections import namedtuple
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gammes import LETTRES, TETRACORDES, TONALITES, Note, gamme, note_de, octave_depart
from gammes import intervalles as pas_gamme
from generer import ACCENT_LY, DIR_LY, ENTETE_PORTEE, PIED_PORTEE, PREAMBULE, RACINE, crochet, ecrire
from generer_mordants import alt_armure, lily_duree, n
from intervalles import analyser, au_dessus, demi_tons, nom as nom_intervalle
import musicxml

PREAMBULE_TONALITES = PREAMBULE.replace("outils/generer.py", "outils/generer_tonalites.py")
TEMPO = 80
N = Fraction
NOIRE = N(1, 4)

# ---------------------------------------------------------------------------
# Modèle : les tonalités et leurs parentés
# ---------------------------------------------------------------------------
Tonalite = namedtuple("Tonalite", "tonique mode")


def ecrit(note):
    """L'orthographe d'une note, sans son octave : (lettre, altération)."""
    return note.lettre, note.alt


def cle(t):
    return ecrit(t.tonique) + (t.mode,)


def nom(t):
    return f"{t.tonique.nom_fr()} {t.mode}"


def ton(txt, mode):
    """« F# », « mineur » -> Tonalite, la tonique à l'octave du do central."""
    return Tonalite(note_de(txt, 4), mode)


# Les trente tonalités écrites : chaque armure en désigne deux.
TOUTES = [t for k, maj, mi in TONALITES for t in (ton(maj, "majeur"), ton(mi, "mineur"))]
ARMURES = {cle(ton(maj, "majeur")): k for k, maj, _ in TONALITES}
ARMURES.update({cle(ton(mi, "mineur")): k for k, _, mi in TONALITES})


def existe(t):
    return cle(t) in ARMURES


def armure(t):
    return ARMURES[cle(t)]


def echelle(t, forme="harmonique"):
    """La gamme de la tonalité ; en mineur, sous la forme demandée."""
    return gamme(t.tonique, "majeure" if t.mode == "majeur" else "mineure " + forme)


def relatif(t):
    """Même armure, autre mode : le 6e degré du majeur, le 3e du mineur."""
    if t.mode == "majeur":
        return Tonalite(gamme(t.tonique, "majeure")[5], "mineur")
    return Tonalite(gamme(t.tonique, "mineure naturelle")[2], "majeur")


def homonyme(t):
    """Même tonique, autre mode : la tonalité directe."""
    return Tonalite(t.tonique, "mineur" if t.mode == "majeur" else "majeur")


def dominante(t):
    return Tonalite(au_dessus(t.tonique, 5, "juste"), t.mode)


def sous_dominante(t):
    return Tonalite(au_dessus(t.tonique, 4, "juste"), t.mode)


def voisins(t):
    """Les cinq tons voisins : le relatif, la dominante et son relatif, la sous-dominante et son relatif."""
    d, s = dominante(t), sous_dominante(t)
    return [relatif(t), d, relatif(d), s, relatif(s)]


def classe(note):
    """La touche du piano : hauteur à l'octave près."""
    return note.hauteur % 12


# ---------------------------------------------------------------------------
# Modèle : la transposition
# ---------------------------------------------------------------------------
def en_dessous(note, numero, qualite):
    """La note située à cet intervalle au-dessous de `note`."""
    rang = note.idx - (numero - 1)
    lettre, octave = LETTRES[rang % 7], note.octave + rang // 7
    cible = note.hauteur - demi_tons(numero, qualite)
    return Note(lettre, cible - Note(lettre, 0, octave).hauteur, octave)


def transposer(note, intervalle):
    """`intervalle` : (numéro, qualité, sens), le sens valant 1 vers l'aigu, −1 vers le grave."""
    numero, qualite, sens = intervalle
    return au_dessus(note, numero, qualite) if sens > 0 else en_dessous(note, numero, qualite)


def intervalle_melodique(a, b):
    """(numéro, qualité, sens) de a vers b ; le sens se lit sur les lettres, comme sur la portée."""
    pa, pb = a.octave * 7 + a.idx, b.octave * 7 + b.idx
    if pa == pb:
        return (1, "juste" if a.alt == b.alt else "augmentée", 0)
    grave, aigu = (a, b) if pb > pa else (b, a)
    return analyser(grave, aigu) + (1 if pb > pa else -1,)


def ecart(note, k):
    """Ce qui distingue la note de l'armure : +1 haussée, −1 abaissée, 0 conforme."""
    return note.alt - alt_armure(note.lettre, k)


def imprimees(mesures, k):
    """L'altération imprimée devant chaque note, mesure par mesure (None si aucune)."""
    res = []
    for mesure in mesures:
        m = musicxml.Mesure(k)
        res.append([m.accidental(note) for note, _ in mesure])
    return res


# ---------------------------------------------------------------------------
# Modèle : les modes anciens
# ---------------------------------------------------------------------------
# Dans l'ordre des touches blanches, de do à si : chaque mode commence sur le
# degré de même rang de la gamme majeure.
MODES = ["ionien", "dorien", "phrygien", "lydien", "mixolydien", "éolien", "locrien"]
MODES_XML = {"ionien": "ionian", "dorien": "dorian", "phrygien": "phrygian", "lydien": "lydian",
             "mixolydien": "mixolydian", "éolien": "aeolian", "locrien": "locrian"}
PAS_MAJEUR = pas_gamme("majeure")
DO = Note("C", 0, 4)

# Du plus clair au plus sombre : sur une même tonique, chaque marche abaisse
# une note d'un demi-ton.
ECHELLE_CLAIRE = ["lydien", "ionien", "mixolydien", "dorien", "éolien", "phrygien", "locrien"]

# La gamme de référence de chaque mode, et ce qui l'en distingue : degré et
# déplacement en demi-tons.
CARACTERISTIQUES = {
    "ionien": ("majeure", {}),
    "dorien": ("mineure naturelle", {6: 1}),
    "phrygien": ("mineure naturelle", {2: -1}),
    "lydien": ("majeure", {4: 1}),
    "mixolydien": ("majeure", {7: -1}),
    "éolien": ("mineure naturelle", {}),
    "locrien": ("mineure naturelle", {2: -1, 5: -1}),
}

# Deux tétracordes et ce qui les sépare : un ton, ou un demi-ton quand l'un
# d'eux couvre un triton.
DECOUPAGE = {
    "ionien": ("majeur", 2, "majeur"),
    "dorien": ("mineur", 2, "mineur"),
    "phrygien": ("phrygien", 2, "phrygien"),
    "lydien": ("lydien", 1, "majeur"),
    "mixolydien": ("majeur", 2, "mineur"),
    "éolien": ("mineur", 2, "phrygien"),
    "locrien": ("phrygien", 1, "lydien"),
}


def pas_mode(mode):
    r = MODES.index(mode)
    return PAS_MAJEUR[r:] + PAS_MAJEUR[:r]


def echelle_mode(tonique, mode):
    notes = [tonique]
    for p in pas_mode(mode):
        notes.append(notes[-1].suivante(p))
    return notes


def gamme_mere(tonique, mode):
    """La tonalité majeure dont le mode emprunte les notes : la tonique y est au rang du mode."""
    r = MODES.index(mode)
    if r == 0:
        return Tonalite(tonique, "majeur")
    numero, qualite = analyser(DO, gamme(DO, "majeure")[r])
    return Tonalite(en_dessous(tonique, numero, qualite), "majeur")


def armure_mode(tonique, mode):
    return armure(gamme_mere(tonique, mode))


def differences(notes, reference):
    """{degré : déplacement} là où deux échelles de même tonique diffèrent."""
    return {i + 1: a.alt - b.alt for i, (a, b) in enumerate(zip(notes[:7], reference[:7]))
            if ecrit(a) != ecrit(b)}


def tetracorde_de(quatre):
    pas = tuple(b.hauteur - a.hauteur for a, b in zip(quatre, quatre[1:]))
    return next(t for t, p in TETRACORDES.items() if p == pas)


def identifier(notes):
    """Le mode d'une échelle, à sa suite de tons et de demi-tons."""
    pas = [b.hauteur - a.hauteur for a, b in zip(notes, notes[1:])]
    trouves = [m for m in MODES if pas_mode(m) == pas]
    assert len(trouves) == 1, notes
    return trouves[0]


# ---------------------------------------------------------------------------
# Les exemples
# ---------------------------------------------------------------------------
def mesures(*txt):
    """« C5 D5 E5:2 » -> une mesure de (note, valeur) ; noire par défaut, « :2 » blanche, « :1 » ronde."""
    res = []
    for m in txt:
        mesure = []
        for x in m.split():
            hauteur, _, duree = x.partition(":")
            mesure.append((n(hauteur), N(1, int(duree)) if duree else NOIRE))
        res.append(mesure)
    return res


# Deux mélodies qui commencent de même ; la troisième mesure décide. La
# modulation commence à la mesure `depuis` (comptée à partir de 0).
Modulation = namedtuple("Modulation", "depart arrivee depuis mesures")
MODULATIONS = {
    "t-modulation-dominante": Modulation(
        ton("C", "majeur"), ton("G", "majeur"), 2,
        mesures("C5 D5 E5 F5", "G5 E5 C5 E5", "D5 F#5 A5 F#5", "G5:1")),
    "t-modulation-relatif": Modulation(
        ton("C", "majeur"), ton("A", "mineur"), 2,
        mesures("C5 D5 E5 F5", "G5 E5 C5 E5", "D5 B4 G#4 B4", "A4:1")),
}

# Une mélodie, sa tonalité et l'intervalle de transposition.
Transposition = namedtuple("Transposition", "tonalite intervalle mesures")
TRANSPOSITION = Transposition(
    ton("G", "majeur"), (2, "majeure", -1),
    mesures("G4 B4 D5 B4", "E5 C#5 D5:2", "C5 A4 F#4 A4", "G4:1"))

# Les exercices.
EXERCICE_VOISINS = [ton("D", "majeur"), ton("Eb", "majeur"), ton("B", "mineur"), ton("F", "mineur")]
EXERCICE_TRANSPOSITION = Transposition(
    ton("D", "majeur"), (3, "mineure", 1),
    mesures("D4 F#4 A4 D5", "C5 B4 A4 G4", "F#4 A4 G4 E4", "D4:1"))
EXERCICE_MODES = [("G", "mixolydien"), ("A", "dorien"), ("D", "lydien"), ("C", "phrygien")]


def a_l_octave(txt):
    """Tonique à l'octave qui garde l'échelle sur la portée de sol."""
    t = note_de(txt, 4)
    return Note(t.lettre, t.alt, octave_depart(t))


def transposee(tr):
    """La tonalité d'arrivée et les mesures transposées."""
    t = Tonalite(transposer(tr.tonalite.tonique, tr.intervalle), tr.tonalite.mode)
    return t, [[(transposer(note, tr.intervalle), v) for note, v in m] for m in tr.mesures]


def orthographes(t):
    """Les notes d'une tonalité ; en mineur, ses trois formes réunies."""
    if t.mode == "majeur":
        return {ecrit(x) for x in gamme(t.tonique, "majeure")}
    return {ecrit(x) for forme in ("naturelle", "harmonique", "mélodique")
            for x in gamme(t.tonique, "mineure " + forme)}


def possibles(notes):
    """Les tonalités écrites dont la gamme contient toutes ces notes."""
    return [t for t in TOUTES if {ecrit(x) for x in notes} <= orthographes(t)]


# ---------------------------------------------------------------------------
# Vérifications : ce que le texte affirme
# ---------------------------------------------------------------------------
def verifier():
    def meme(a, b):
        return cle(a) == cle(b)

    def dans(t, liste):
        return any(meme(t, u) for u in liste)

    # Trente tonalités écrites, vingt-quatre entendues : trois paires
    # enharmoniques dans chaque mode.
    assert len(TOUTES) == 30
    for mode in ("majeur", "mineur"):
        assert len({classe(t.tonique) for t in TOUTES if t.mode == mode}) == 12
    paires = {mode: sorted(sorted(ecrit(t.tonique) for t in TOUTES if t.mode == mode
                                  and classe(t.tonique) == c)
                           for c in range(12)
                           if sum(1 for t in TOUTES if t.mode == mode and classe(t.tonique) == c) == 2)
              for mode in ("majeur", "mineur")}
    assert paires["majeur"] == [[("B", 0), ("C", -1)], [("C", 1), ("D", -1)], [("F", 1), ("G", -1)]]
    assert paires["mineur"] == [[("A", -1), ("G", 1)], [("A", 1), ("B", -1)], [("D", 1), ("E", -1)]]

    # La tierce au-dessus de la tonique décide du mode.
    for t in TOUTES:
        tierce = analyser(t.tonique, echelle(t)[2])
        assert tierce == (3, "majeure" if t.mode == "majeur" else "mineure")

    # Notes tonales et notes modales : sur une même tonique, le majeur et le
    # mineur harmonique ne diffèrent qu'aux degrés 3 et 6 ; le mineur naturel,
    # aux degrés 3, 6 et 7. Les accords des degrés 1, 4 et 5 contiennent
    # toutes les notes de la gamme.
    directs = [t for t in TOUTES if t.mode == "majeur" and existe(homonyme(t))]
    assert len(directs) == 12
    for t in directs:
        maj = gamme(t.tonique, "majeure")
        assert set(differences(gamme(t.tonique, "mineure harmonique"), maj)) == {3, 6}
        assert set(differences(gamme(t.tonique, "mineure naturelle"), maj)) == {3, 6, 7}
        # L'homonyme mineur a trois altérations de plus vers les bémols.
        assert armure(t) - armure(homonyme(t)) == 3
    for t in TOUTES:
        g = echelle(t)
        accords = {ecrit(g[(d + k) % 7]) for d in (0, 3, 4) for k in (0, 2, 4)}
        assert accords == {ecrit(x) for x in g}

    # Le relatif : même armure, une tierce mineure plus bas.
    for t in TOUTES:
        if t.mode == "majeur":
            r = relatif(t)
            assert existe(r) and armure(r) == armure(t)
            assert ecrit(en_dessous(t.tonique, 3, "mineure")) == ecrit(r.tonique)
            assert meme(relatif(r), t)

    # Les tons voisins : cinq, à une altération d'écart au plus, et ce sont
    # exactement les tonalités des trois armures consécutives.
    for t in TOUTES:
        v = voisins(t)
        if not all(existe(x) for x in v):
            continue
        assert len({cle(x) for x in v}) == 5 and not dans(t, v)
        assert all(abs(armure(x) - armure(t)) <= 1 for x in v)
        famille = [u for u in TOUTES if abs(armure(u) - armure(t)) <= 1 and not meme(u, t)]
        assert {cle(x) for x in famille} == {cle(x) for x in v}
        # Un ton et son relatif : même famille.
        assert {cle(x) for x in v + [t]} == {cle(x) for x in voisins(relatif(t)) + [relatif(t)]}
        # Les toniques des voisins sont les degrés qui portent un accord
        # parfait, tonique exceptée : 2 à 6 en majeur, 3 à 7 en mineur naturel.
        g = echelle(t, "naturelle")[:7]
        g = g + [Note(x.lettre, x.alt, x.octave + 1) for x in g]
        portes = []
        for d in range(1, 7):
            if analyser(g[d], g[d + 4]) == (5, "juste"):
                tierce = analyser(g[d], g[d + 2])
                portes.append((d + 1, Tonalite(g[d], "majeur" if tierce[1] == "majeure" else "mineur")))
        attendus = [2, 3, 4, 5, 6] if t.mode == "majeur" else [3, 4, 5, 6, 7]
        assert [d for d, _ in portes] == attendus, (nom(t), portes)
        assert {cle(x) for _, x in portes} == {cle(x) for x in v}

    # Aux deux bouts : la dominante de do dièse majeur demanderait huit dièses,
    # on l'écrit la bémol majeur ; même chose pour son relatif.
    cis = ton("C#", "majeur")
    assert not existe(dominante(cis)) and not existe(relatif(dominante(cis)))
    assert classe(dominante(cis).tonique) == classe(note_de("Ab"))
    assert classe(relatif(dominante(cis)).tonique) == classe(note_de("F"))
    assert existe(ton("Ab", "majeur")) and existe(ton("F", "mineur"))

    # Les modulations : la mélodie commence en do majeur ; après le
    # changement, une note altérée exclut do majeur ; c'est la sensible de la
    # tonalité d'arrivée, qui mène à sa tonique ; la mélodie conclut sur
    # celle-ci ; et c'est un ton voisin.
    for mod in MODULATIONS.values():
        avant = [x for m in mod.mesures[:mod.depuis] for x, _ in m]
        apres = [x for m in mod.mesures[mod.depuis:] for x, _ in m]
        assert dans(mod.depart, possibles(avant))
        assert not dans(mod.depart, possibles(apres)) and dans(mod.arrivee, possibles(apres))
        sensible = echelle(mod.arrivee)[6]
        alterees = [x for x in apres if ecart(x, armure(mod.depart))]
        assert alterees and all(ecrit(x) == ecrit(sensible) for x in alterees)
        assert ecrit(apres[-1]) == ecrit(mod.arrivee.tonique)
        assert dans(mod.arrivee, voisins(mod.depart))
    # Les deux mélodies commencent de même.
    a, b = MODULATIONS.values()
    assert [[ecrit(x) for x, _ in m] for m in a.mesures[:2]] == [[ecrit(x) for x, _ in m] for m in b.mesures[:2]]

    # Les transpositions : chaque intervalle conservé, chaque note garde son
    # écart à l'armure ; l'exemple change un dièse en bécarre, l'exercice un
    # bécarre en bémol.
    for tr in (TRANSPOSITION, EXERCICE_TRANSPOSITION):
        for m in tr.mesures:
            assert sum(v for _, v in m) == 1
        t2, m2 = transposee(tr)
        assert existe(t2)
        avant = [x for m in tr.mesures for x, _ in m]
        apres = [x for m in m2 for x, _ in m]
        for (a1, b1), (a2, b2) in zip(zip(avant, avant[1:]), zip(apres, apres[1:])):
            assert intervalle_melodique(a1, b1) == intervalle_melodique(a2, b2)
        assert [ecart(x, armure(tr.tonalite)) for x in avant] == [ecart(x, armure(t2)) for x in apres]
    t2, m2 = transposee(TRANSPOSITION)
    assert nom(t2) == "fa majeur" and armure(t2) == -1
    signes = [(a, b) for ma, mb in zip(imprimees(TRANSPOSITION.mesures, armure(TRANSPOSITION.tonalite)),
                                        imprimees(m2, armure(t2)))
              for a, b in zip(ma, mb) if a or b]
    assert signes == [("sharp", "natural")]
    t3, m3 = transposee(EXERCICE_TRANSPOSITION)
    assert nom(t3) == "fa majeur"
    signes = [(a, b) for ma, mb in zip(imprimees(EXERCICE_TRANSPOSITION.mesures,
                                                 armure(EXERCICE_TRANSPOSITION.tonalite)),
                                        imprimees(m3, armure(t3)))
              for a, b in zip(ma, mb) if a or b]
    assert signes == [("natural", "flat")]

    # La clarinette en si bémol lue en clé d'ut quatrième ligne : la même
    # position de la portée y porte la lettre précédente, une octave plus bas.
    # (Première ligne : mi4 en clé de sol, ré3 en clé d'ut 4e ligne.)
    sol_ligne1, ut4_ligne1 = Note("E", 0, 4), Note("D", 0, 3)
    assert (sol_ligne1.idx - ut4_ligne1.idx) % 7 == 1 and sol_ligne1.octave - ut4_ligne1.octave == 1

    # Les modes : les touches blanches, deux tétracordes, une note
    # caractéristique, la gamme mère et son armure.
    blancs = {m: echelle_mode(a_l_octave(LETTRES[i]), m) for i, m in enumerate(MODES)}
    for m, notes in blancs.items():
        assert all(x.alt == 0 for x in notes)
        assert ecrit(notes[0]) == ecrit(notes[7])
        bas, joint, haut = DECOUPAGE[m]
        assert (tetracorde_de(notes[:4]), notes[4].hauteur - notes[3].hauteur,
                tetracorde_de(notes[4:])) == (bas, joint, haut), m
        assert armure_mode(notes[0], m) == 0
    assert blancs["ionien"][0].lettre == "C" and blancs["éolien"][0].lettre == "A"
    for txt in ("C", "D", "E", "F", "G", "A", "B", "Bb", "F#", "Eb", "C#"):
        for m in MODES:
            notes = echelle_mode(note_de(txt), m)
            ref, diff = CARACTERISTIQUES[m]
            assert differences(notes, gamme(note_de(txt), ref)) == diff, (txt, m)
            # Les notes du mode sont celles de sa gamme mère.
            mere = gamme(gamme_mere(note_de(txt), m).tonique, "majeure")
            assert {ecrit(x) for x in notes} == {ecrit(x) for x in mere}
            assert identifier(notes) == m
    # Sur ré, du lydien au locrien : une altération de moins à chaque marche,
    # une seule note abaissée d'un demi-ton.
    re = note_de("D")
    armures_re = [armure_mode(re, m) for m in ECHELLE_CLAIRE]
    assert armures_re == [3, 2, 1, 0, -1, -2, -3]
    abaissees, nouvelles = [], []
    for m1, m2 in zip(ECHELLE_CLAIRE, ECHELLE_CLAIRE[1:]):
        d = differences(echelle_mode(re, m2), echelle_mode(re, m1))
        assert list(d.values()) == [-1]
        abaissees.append(list(d)[0])
        nouvelles.append(ecrit(echelle_mode(re, m2)[list(d)[0] - 1]))
    # Les degrés abaissés se suivent de quarte en quarte : les dièses s'en
    # vont dans l'ordre inverse de l'armure, puis les bémols viennent dans
    # l'ordre de l'armure.
    assert abaissees == [4, 7, 3, 6, 2, 5]
    assert nouvelles == [("G", 0), ("C", 0), ("F", 0), ("B", -1), ("E", -1), ("A", -1)]
    assert nom(gamme_mere(note_de("G"), "dorien")) == "fa majeur"

    # Les exercices.
    assert [identifier(echelle_mode(a_l_octave(t), m)) for t, m in EXERCICE_MODES] == \
        [m for _, m in EXERCICE_MODES]
    assert all(existe(x) for t in EXERCICE_VOISINS for x in voisins(t))


# ---------------------------------------------------------------------------
# La modulation : accord pivot, homonyme, tons éloignés, tierce picarde
# ---------------------------------------------------------------------------
def accord_degre(t, degre, sons=3):
    """L'accord bâti sur un degré, avec les notes de la gamme (harmonique en mineur)."""
    g = echelle(t)[:7]
    return [g[(degre - 1 + 2 * i) % 7] for i in range(sons)]


def orthographe(notes):
    return {ecrit(x) for x in notes}


# De do majeur à sol majeur par un accord commun : (accord, tonalités et degrés).
PIVOT = [
    ([n("C4"), n("E4"), n("G4")], [(ton("C", "majeur"), 1)]),
    ([n("A4"), n("C5"), n("E5")], [(ton("C", "majeur"), 6), (ton("G", "majeur"), 2)]),
    ([n("D4"), n("F#4"), n("A4")], [(ton("G", "majeur"), 5)]),
    ([n("G4"), n("B4"), n("D5")], [(ton("G", "majeur"), 1)]),
]
ROMAINS = ["I", "II", "III", "IV", "V", "VI", "VII"]
TONS_DIMINUEE = [ton(x, "mineur") for x in ("A", "C", "Eb", "F#")]


def verifier_modulation():
    """Ce que la section de la modulation affirme, au-delà des deux exemples."""
    do, sol = ton("C", "majeur"), ton("G", "majeur")
    # Chaque accord de l'exemple est bien celui du degré annoncé ; l'accord
    # pivot appartient aux deux tonalités, le suivant à sol seulement.
    for notes, lectures in PIVOT:
        for t, d in lectures:
            assert orthographe(notes) == orthographe(accord_degre(t, d)), (notes, t, d)
    assert orthographe(PIVOT[1][0]) <= orthographes(do) and orthographe(PIVOT[1][0]) <= orthographes(sol)
    assert not orthographe(PIVOT[2][0]) <= orthographes(do)
    assert [x.nom_fr() for x in PIVOT[1][0]] == ["la", "do", "mi"]

    # Vers l'homonyme : la dominante est la même, la tonique change de tierce.
    for t in TOUTES:
        h = homonyme(t)
        if existe(h):
            assert orthographe(accord_degre(t, 5)) == orthographe(accord_degre(h, 5)), t
            i, j = accord_degre(t, 1), accord_degre(h, 1)
            assert ecrit(i[0]) == ecrit(j[0]) and ecrit(i[2]) == ecrit(j[2]) and ecrit(i[1]) != ecrit(j[1])
    assert [x.nom_fr() for x in accord_degre(do, 5)] == ["sol", "si", "ré"]

    # La tierce picarde : la mineur s'achève sur la–do dièse–mi, l'accord de
    # tonique de la majeur, son homonyme.
    la = ton("A", "mineur")
    assert [x.nom_fr() for x in accord_degre(homonyme(la), 1)] == ["la", "do dièse", "mi"]
    assert [x.nom_fr() for x in accord_degre(la, 1)] == ["la", "do", "mi"]

    # Les tons éloignés : la septième diminuée de la mineur sonne comme celles
    # de do, mi bémol et fa dièse mineur, sous quatre orthographes.
    septiemes = [accord_degre(t, 7, sons=4) for t in TONS_DIMINUEE]
    assert len({frozenset(classe(x) for x in a) for a in septiemes}) == 1
    assert len({frozenset(orthographe(a)) for a in septiemes}) == 4
    assert [x.nom_fr() for x in septiemes[0]] == ["sol dièse", "si", "ré", "fa"]
    assert [x.nom_fr() for x in septiemes[1]] == ["si", "ré", "fa", "la bémol"]
    # Ces quatre tonalités sont loin de la mineur : aucune n'est son voisin.
    assert not any(cle(t) in {cle(v) for v in voisins(la)} for t in TONS_DIMINUEE[1:])


# ---------------------------------------------------------------------------
# Textes : noms, armures, réponses
# ---------------------------------------------------------------------------
SIGNE_TEX = {-2: r"$\flat\flat$", -1: r"$\flat$", 0: "", 1: r"$\sharp$", 2: r"$\times$"}


def court(note):
    """« fa$\\sharp$ » : le nom français et le signe, pour les tableaux."""
    return note.nom_fr().split()[0] + SIGNE_TEX[note.alt]


def armure_texte(k):
    if k == 0:
        return "aucune altération"
    nombre = {1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept"}[abs(k)]
    signe = "dièse" if k > 0 else "bémol"
    return f"{nombre} {signe}{'s' if abs(k) > 1 else ''}"


def armure_courte(k):
    if k == 0:
        return "aucune"
    return f"{abs(k)}~{'dièse' if k > 0 else 'bémol'}{'s' if abs(k) > 1 else ''}"


def reponse_voisins(t):
    return f"{nom(t)}~:~" + ", ".join(nom(x) for x in voisins(t))


NOM_SIGNE = {"sharp": "dièse", "natural": "bécarre", "flat": "bémol"}


def reponse_transposition(tr):
    t2, m2 = transposee(tr)
    avant = imprimees(tr.mesures, armure(tr.tonalite))
    apres = imprimees(m2, armure(t2))
    changes = []
    for i, (ma, mb, notes_a, notes_b) in enumerate(zip(avant, apres, tr.mesures, m2)):
        for a, b, (xa, _), (xb, _) in zip(ma, mb, notes_a, notes_b):
            if a or b:
                changes.append(f"le {xa.nom_fr().split()[0]} {NOM_SIGNE[a]} de la mesure~{i + 1} "
                               f"devient {xb.nom_fr().split()[0]} {NOM_SIGNE[b]}")
    return (f"en {nom(t2)}, {armure_texte(armure(t2))} à l'armure ; "
            + " ; ".join(changes))


def majuscule(txt):
    return txt[0].upper() + txt[1:]


def reponse_mode(txt, m):
    t = a_l_octave(txt)
    mere = gamme_mere(t, m)
    return f"{t.nom_fr()} {m}, les notes de {nom(mere)}"


# ---------------------------------------------------------------------------
# Gravures
# ---------------------------------------------------------------------------
def couleur(txt):
    """Note en couleur : tête, hampe et altération."""
    return (r"\tweak color %s \tweak Stem.color %s \tweak Accidental.color %s %s"
            % (ACCENT_LY, ACCENT_LY, ACCENT_LY, txt))


def cle_lily(tonique, mode):
    """\\key de LilyPond : « majeur », « mineur », ou un mode ancien."""
    ly = {"majeur": "major", "mineur": "minor"}.get(mode) or MODES_XML[mode]
    return r"\key %s \%s" % (tonique.lily().rstrip("',"), ly)


MARGE = r"""    \set Staff.printKeyCancellation = ##f
    \set Staff.explicitKeySignatureVisibility = #end-of-line-invisible
"""


def pied_avec_marge(mm):
    """Le pied de portée commun, avec un retrait pour les noms en marge."""
    return PIED_PORTEE.replace(
        "  \\layout {\n",
        "  \\layout {\n    indent = %d\\mm\n    short-indent = %d\\mm\n" % (mm, mm), 1)


def ligne_en_marge(i, libelle):
    return "    \\set Staff.%s = \\markup \\small \"%s\"\n" % (
        "instrumentName" if i == 0 else "shortInstrumentName", libelle)


def figure_relatives():
    """Do majeur, son relatif la mineur, son homonyme do mineur : armure et tonique."""
    do = ton("C", "majeur")
    lignes = [(do, "do majeur"), (relatif(do), "la mineur"), (homonyme(do), "do mineur")]
    corps = MARGE
    for i, (t, libelle) in enumerate(lignes):
        tonique = Note(t.tonique.lettre, t.tonique.alt, octave_depart(t.tonique))
        g = echelle(Tonalite(tonique, t.mode))
        corps += ligne_en_marge(i, libelle)
        corps += "    %s\n" % cle_lily(t.tonique, t.mode)
        corps += "    " + " ".join(x.lily() for x in g) + "\n"
        if i < len(lignes) - 1:
            corps += "    \\bar \"\" \\break\n"
    return ENTETE_PORTEE + corps + pied_avec_marge(18)


def figure_tonales():
    """Do majeur et do mineur : degrés numérotés, notes modales en couleur, notes tonales en gras."""
    corps = MARGE
    do = note_de("C", 4)
    for i, (mode, forme) in enumerate((("majeur", "majeure"), ("mineur", "mineure harmonique"))):
        g = gamme(do, forme)
        corps += ligne_en_marge(i, f"do {mode}")
        corps += "    %s\n    " % cle_lily(do, mode)
        notes = []
        for d, x in enumerate(g[:7], 1):
            txt = x.lily()
            chiffre = r'\small "%d"' % d
            if d in (3, 6):
                txt = couleur(txt)
                chiffre = r'\small \with-color %s "%d"' % (ACCENT_LY, d)
            elif d in (1, 4, 5):
                chiffre = r'\small \bold "%d"' % d
            notes.append(txt + r"_\markup " + chiffre)
        notes.append(g[7].lily())
        corps += " ".join(notes) + "\n"
        if i == 0:
            corps += "    \\bar \"\" \\break\n"
    return ENTETE_PORTEE + corps + pied_avec_marge(18)


def portee_mesuree(t, mesures_, colorer=lambda x: False, sous=None):
    """Une portée mesurée en 4/4 ; `sous` : {indice de mesure : texte sous sa première note}."""
    sous = sous or {}
    corps = []
    for i, m in enumerate(mesures_):
        for j, (x, v) in enumerate(m):
            txt = x.lily() + lily_duree(v)
            if colorer(x):
                txt = couleur(txt)
            if j == 0 and i in sous:
                txt += r'_\markup \small \italic "%s"' % sous[i]
            corps.append(txt)
        corps.append("|")
    return r"""\clef treble \time 4/4 %s
      %s
      \bar "|." """ % (cle_lily(t.tonique, t.mode), " ".join(corps[:-1]))


def partition_ly(portees, noms=None):
    """Une ou plusieurs portées mesurées, réunies en groupe si plusieurs."""
    blocs = []
    for i, corps in enumerate(portees):
        avec = (r'\with { instrumentName = \markup \small \italic "%s" }' % noms[i]) if noms else ""
        blocs.append("    \\new Staff %s {\n      %s\n    }" % (avec, corps))
    musique = blocs[0].strip() if len(blocs) == 1 else "\\new StaffGroup <<\n" + "\n".join(blocs) + "\n  >>"
    retrait = "indent = 18\\mm" if noms else ""
    return r"""\score {
  %s
  \layout {
    %s
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
""" % (musique, retrait)


def figure_modulation(mod):
    k = armure(mod.depart)
    corps = portee_mesuree(mod.depart, mod.mesures, colorer=lambda x: ecart(x, k) != 0,
                           sous={0: nom(mod.depart), mod.depuis: nom(mod.arrivee)})
    corps = corps.replace(r"\time 4/4", r"\time 4/4 \override TextScript.staff-padding = #2.5", 1)
    return partition_ly([corps])


def figure_transposition(tr, avec_reponse=True):
    t2, m2 = transposee(tr)
    k1, k2 = armure(tr.tonalite), armure(t2)
    if not avec_reponse:
        # L'énoncé de l'exercice : rien n'y désigne la note altérée.
        return partition_ly([portee_mesuree(tr.tonalite, tr.mesures)])
    haut = portee_mesuree(tr.tonalite, tr.mesures, colorer=lambda x: ecart(x, k1) != 0)
    bas = portee_mesuree(t2, m2, colorer=lambda x: ecart(x, k2) != 0)
    return partition_ly([haut, bas], [nom(tr.tonalite), nom(t2)])


def figure_reponse_transposition(tr):
    t2, m2 = transposee(tr)
    k2 = armure(t2)
    return partition_ly([portee_mesuree(t2, m2, colorer=lambda x: ecart(x, k2) != 0)])


def echelle_ly(notes, mode, dessus=None):
    """Une échelle et ses deux tétracordes, légendés par leur type."""
    ly = [x.lily() for x in notes]
    bas, _, haut = DECOUPAGE[mode]
    premier = ly[0]
    if dessus:
        premier += r'^\markup \small \bold "%s"' % dessus
    return (crochet(bas) + "    " + premier + "\\startGroup " + " ".join(ly[1:3]) + " " + ly[3] + "\\stopGroup\n"
            + crochet(haut) + "    " + ly[4] + "\\startGroup " + " ".join(ly[5:7]) + " " + ly[7] + "\\stopGroup\n")


def figure_modes():
    """Les sept modes sur les touches blanches, deux par ligne, chacun avec ses tétracordes."""
    corps = "    \\key c \\major\n"
    for i, m in enumerate(MODES):
        notes = echelle_mode(a_l_octave(LETTRES[i]), m)
        corps += echelle_ly(notes, m, dessus=f"{notes[0].nom_fr()} {m}")
        if i == len(MODES) - 1:
            break
        corps += "    \\bar \"\" \\break\n" if i % 2 == 1 else "    \\bar \"||\"\n"
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_exercice_modes():
    """Quatre échelles numérotées, altérations écrites, sans armure ni crochets."""
    corps = "    \\key c \\major\n"
    for i, (txt, m) in enumerate(EXERCICE_MODES):
        notes = echelle_mode(a_l_octave(txt), m)
        ly = [x.lily() for x in notes]
        ly[0] += r'_\markup \small "%d"' % (i + 1)
        corps += "    " + " ".join(ly) + "\n"
        if i < len(EXERCICE_MODES) - 1:
            corps += "    \\bar \"\" \\break\n" if i % 2 == 1 else "    \\bar \"||\"\n"
    return ENTETE_PORTEE + corps + PIED_PORTEE


def figure_pivot():
    """Quatre accords, chacun lu sous son degré ; l'accord pivot, sous deux."""
    corps = []
    for notes, lectures in PIVOT:
        lignes = " ".join(r'"%s : %s"' % (t.tonique.nom_fr(), ROMAINS[d - 1]) for t, d in lectures)
        corps.append("<%s>1_\\markup \\small \\center-column { %s }"
                     % (" ".join(x.lily() for x in notes), lignes))
    return r"""\score {
  \new Staff {
    \clef treble \key c \major \time 4/4
    \override TextScript.staff-padding = #3.5
    %s
    \bar "|."
  }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
""" % " | ".join(corps)


def figures():
    res = {
        "t-relatives": figure_relatives(),
        "t-tonales": figure_tonales(),
        "t-transposition": figure_transposition(TRANSPOSITION),
        "t-modes": figure_modes(),
        "t-exercice-transposition": figure_transposition(EXERCICE_TRANSPOSITION, avec_reponse=False),
        "t-exercice-reponse": figure_reponse_transposition(EXERCICE_TRANSPOSITION),
        "t-exercice-modes": figure_exercice_modes(),
        "t-pivot": figure_pivot(),
    }
    res.update({nom_figure: figure_modulation(mod) for nom_figure, mod in MODULATIONS.items()})
    return res


def ecrire_gravures():
    return [ecrire(nom_figure, contenu, preambule=PREAMBULE_TONALITES)
            for nom_figure, contenu in figures().items()]


# ---------------------------------------------------------------------------
# Tableaux LaTeX : le cercle des quintes, les modes sur ré, les réponses
# ---------------------------------------------------------------------------
ENTETE_TEX = "%% Produit par outils/generer_tonalites.py — ne pas modifier à la main.\n"


def ecrire_tex(nom_fichier, contenu):
    chemin = os.path.join(DIR_LY, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE_TEX + contenu)
    return chemin


def cercle():
    """
    Le cercle des quintes en TikZ : les majeures dehors, leurs relatifs dedans,
    l'armure au bord ; en couleur, do majeur et ses cinq voisins.

    La case p (de 0 à 11, dans le sens des aiguilles d'une montre depuis le
    haut) réunit les armures p et p − 12 : à 5, 6 et 7, deux écritures du même
    son.
    """
    do = ton("C", "majeur")
    famille = {cle(x) for x in voisins(do)}
    lignes = [r"\begin{tikzpicture}[x=1cm, y=1cm]",
              r"  \fill[lightnavy] (135:1.2) arc (135:45:1.2) -- (45:3.7) arc (45:135:3.7) -- cycle;",
              r"  \draw[navy, line width=0.6pt] (0,0) circle (3.7);",
              r"  \draw[navy!40, line width=0.4pt] (0,0) circle (2.45);",
              r"  \draw[navy!40, line width=0.4pt] (0,0) circle (1.2);"]
    for p in range(12):
        angle = 90 - 30 * p
        # L'armure la plus légère d'abord, et les dièses à égalité :
        # si / do bémol, fa dièse / sol bémol, ré bémol / do dièse.
        cases = sorted(((k, maj, mi) for k, maj, mi in TONALITES if k % 12 == p),
                       key=lambda c: (abs(c[0]), -c[0]))
        # Deux écritures du même son : l'une au-dessus de l'autre.
        maj = r"\\".join(court(note_de(c[1])) for c in cases)
        mi = r"\\".join(court(note_de(c[2])) for c in cases)
        arm = r"\\".join(str(abs(c[0])) + (r"$\sharp$" if c[0] > 0 else r"$\flat$" if c[0] < 0 else "")
                          for c in cases)
        style_maj, style_mi = r"\small", r"\small\itshape"
        if any(cle(ton(c[1], "majeur")) == cle(do) for c in cases):
            style_maj = r"\small\bfseries\color{accent}"
        elif any(cle(ton(c[1], "majeur")) in famille for c in cases):
            style_maj = r"\small\bfseries"
        if any(cle(ton(c[2], "mineur")) in famille for c in cases):
            style_mi = r"\small\itshape\bfseries"
        lignes.append(r"  \node[align=center, font=%s] at (%d:3.08) {%s};" % (style_maj, angle, maj))
        lignes.append(r"  \node[align=center, font=%s] at (%d:1.83) {%s};" % (style_mi, angle, mi))
        lignes.append(r"  \node[align=center, font=\scriptsize\color{mygray}] at (%d:4.15) {%s};"
                      % (angle, arm))
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes) + "\n"


def tableau_modes_re():
    """Les sept modes sur ré, du plus clair au plus sombre : notes, armure, note caractéristique."""
    re = note_de("D")
    lignes = [r"{\small\setlength{\tabcolsep}{5pt}%",
              r"\begin{tabular}{@{}l l l l l@{}}",
              r"\toprule",
              r"\textbf{Mode} & \textbf{Notes} & \textbf{Armure} & \textbf{Comparé à} "
              r"& \textbf{Note caractéristique} \\",
              r"\midrule"]
    for m in ECHELLE_CLAIRE:
        notes = echelle_mode(re, m)
        ref, diff = CARACTERISTIQUES[m]
        cellules = []
        for d, x in enumerate(notes, 1):
            c = court(x)
            cellules.append(r"\textcolor{accent}{\textbf{%s}}" % c if d in diff else c)
        traits = [nom_intervalle(*analyser(notes[0], notes[d - 1])) for d in sorted(diff)]
        distingue = ", ".join(traits) if traits else "aucune"
        base = "ré majeur" if ref == "majeure" else "ré mineur"
        lignes.append(f"{m} & {' '.join(cellules)} & {armure_courte(armure_mode(re, m))} "
                      f"& {base} & {distingue} \\\\")
    lignes += [r"\bottomrule", r"\end{tabular}}"]
    return "\n".join(lignes) + "\n"


def ecrire_reponses():
    voisins_txt = "~; ".join(reponse_voisins(t) for t in EXERCICE_VOISINS)
    modes_txt = "~; ".join(f"{i}~:~{reponse_mode(t, m)}" for i, (t, m) in enumerate(EXERCICE_MODES, 1))
    contenu = (r"\textbf{1.} " + voisins_txt + ".\n\n"
               + r"\textbf{2.} " + majuscule(reponse_transposition(EXERCICE_TRANSPOSITION)) + ".\n\n"
               + r"\begin{center}\includegraphics[width=0.8\linewidth]{t-exercice-reponse.cropped.pdf}\end{center}"
               + "\n\n"
               + r"\textbf{3.} " + modes_txt + ".\n")
    return ecrire_tex("tonalites-reponses.tex", contenu)


def ecrire_tableaux():
    return [ecrire_tex("tonalites-cercle.tex", cercle()),
            ecrire_tex("tonalites-modes-re.tex", tableau_modes_re()),
            ecrire_reponses()]


# ---------------------------------------------------------------------------
# MusicXML
# ---------------------------------------------------------------------------
MODE_XML = {"majeur": "major", "mineur": "minor"}


def en_noires(notes):
    """Une échelle en noires, quatre par mesure."""
    groupes = [[(x, NOIRE, False)] for x in notes]
    return [groupes[i:i + 4] for i in range(0, len(groupes), 4)]


def en_groupes(mesures_):
    return [[[(x, v, False)] for x, v in m] for m in mesures_]


def ecrire_musicxml():
    entrees = []
    do = ton("C", "majeur")
    for t, libelle in ((do, "do majeur"), (relatif(do), "la mineur, son relatif"),
                       (homonyme(do), "do mineur, son homonyme")):
        tonique = Note(t.tonique.lettre, t.tonique.alt, octave_depart(t.tonique))
        entrees.append((libelle, armure(t), MODE_XML[t.mode], (4, 4),
                        en_noires(echelle(Tonalite(tonique, t.mode)))))
    for mod in MODULATIONS.values():
        entrees.append((f"de {nom(mod.depart)} à {nom(mod.arrivee)}", armure(mod.depart),
                        MODE_XML[mod.depart.mode], (4, 4), en_groupes(mod.mesures)))
    entrees.append(("de do majeur à sol majeur, par un accord pivot", 0, "major", (4, 4),
                    [[[(list(notes), N(1), False)]] for notes, _ in PIVOT]))
    t2, m2 = transposee(TRANSPOSITION)
    entrees.append((f"une mélodie en {nom(TRANSPOSITION.tonalite)}", armure(TRANSPOSITION.tonalite),
                    "major", (4, 4), en_groupes(TRANSPOSITION.mesures)))
    entrees.append((f"transposée en {nom(t2)}", armure(t2), "major", (4, 4), en_groupes(m2)))
    for i, m in enumerate(MODES):
        notes = echelle_mode(a_l_octave(LETTRES[i]), m)
        entrees.append((f"{notes[0].nom_fr()} {m}", 0, MODES_XML[m], (4, 4), en_noires(notes)))
    re = Note("D", 0, 4)
    for m in ECHELLE_CLAIRE:
        entrees.append((f"ré {m}", armure_mode(re, m), MODES_XML[m], (4, 4),
                        en_noires(echelle_mode(re, m))))
    ex = EXERCICE_TRANSPOSITION
    entrees.append((f"l'exercice de transposition, en {nom(ex.tonalite)}", armure(ex.tonalite),
                    "major", (4, 4), en_groupes(ex.mesures)))
    chemin = os.path.join(RACINE, "tonalites.musicxml")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(musicxml.partition_rythmee(
            "Les tonalités",
            "Relatif et homonyme, deux modulations et un accord pivot, une transposition, "
            "les modes anciens "
            f"sur les touches blanches puis sur ré, à la noire {TEMPO}.",
            entrees, "Piano", TEMPO))
    return chemin


if __name__ == "__main__":
    verifier()
    verifier_modulation()
    print("Vérifications : toutes passées")
    for c in ecrire_gravures():
        print("LilyPond :", os.path.relpath(c, RACINE))
    for c in ecrire_tableaux():
        print("LaTeX :", os.path.relpath(c, RACINE))
    print("MusicXML :", os.path.relpath(ecrire_musicxml(), RACINE))
