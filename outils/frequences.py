#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle des fréquences : rapports exacts, cents et tempéraments.

Le guide des fréquences cite des dizaines de nombres — commas, tailles de
demi-tons, écarts en cents, fréquences en hertz. Ils sont tous calculés ici,
en fractions exactes quand le rapport est rationnel, et vérifiés avant que le
générateur n'écrive quoi que ce soit : une identité fausse (un comma mal
nommé, un demi-ton qui ne complète pas son ton) arrête tout.

    python3 outils/frequences.py      # lance les contrôles seuls
"""

from fractions import Fraction
from math import isclose, log2

LA = 440.0            # diapason, en hertz
OCTAVE = Fraction(2)
QUINTE = Fraction(3, 2)


def cents(r):
    """Taille d'un rapport de fréquences, en cents (1200 par octave)."""
    return 1200 * log2(float(r))


def tempere(n):
    """Rapport de n demi-tons du tempérament égal."""
    return 2 ** (n / 12)


# ---------------------------------------------------------------------------
# Les deux commas
# ---------------------------------------------------------------------------
# Douze quintes justes dépassent sept octaves ; quatre quintes justes,
# ramenées de deux octaves, dépassent la tierce majeure juste.
COMMA_PYTHAGORICIEN = QUINTE ** 12 / OCTAVE ** 7      # 531441/524288
COMMA_SYNTONIQUE = QUINTE ** 4 / OCTAVE ** 2 / Fraction(5, 4)   # 81/80

TON_MAJEUR = Fraction(9, 8)
TON_MINEUR = Fraction(10, 9)
LIMMA = OCTAVE ** 3 / QUINTE ** 5          # 256/243, demi-ton diatonique
APOTOME = QUINTE ** 7 / OCTAVE ** 4        # 2187/2048, demi-ton chromatique


# ---------------------------------------------------------------------------
# Les intervalles simples : nom, demi-tons, rapport juste de référence
# ---------------------------------------------------------------------------
# Le rapport « juste » est le plus simple qu'on rencontre dans la série des
# harmoniques. Le triton n'en a pas d'universellement admis : 45/32 est celui
# de la gamme de Zarlino (quarte augmentée fa--si de do majeur).
INTERVALLES = [
    ("unisson",            0, Fraction(1)),
    ("seconde mineure",    1, Fraction(16, 15)),
    ("seconde majeure",    2, Fraction(9, 8)),
    ("tierce mineure",     3, Fraction(6, 5)),
    ("tierce majeure",     4, Fraction(5, 4)),
    ("quarte juste",       5, Fraction(4, 3)),
    ("triton",             6, Fraction(45, 32)),
    ("quinte juste",       7, Fraction(3, 2)),
    ("sixte mineure",      8, Fraction(8, 5)),
    ("sixte majeure",      9, Fraction(5, 3)),
    ("septième mineure",  10, Fraction(16, 9)),
    ("septième majeure",  11, Fraction(15, 8)),
    ("octave",            12, Fraction(2)),
]


# ---------------------------------------------------------------------------
# La série des harmoniques, sur do1 (notation française ; C2 en notation
# internationale) — la note la plus grave qui garde la série lisible sur deux
# portées. Chaque harmonique y est rapprochée de la note tempérée la plus proche.
# ---------------------------------------------------------------------------
NOMS = ["do", "do♯", "ré", "mi♭", "mi", "fa", "fa♯", "sol", "la♭", "la", "si♭", "si"]
NOMS_TEX = ["do", "do dièse", "ré", "mi bémol", "mi", "fa", "fa dièse", "sol",
            "la bémol", "la", "si bémol", "si"]


def frequence_midi(m):
    """Fréquence tempérée d'un numéro MIDI (69 = la 440)."""
    return LA * 2 ** ((m - 69) / 12)


def nom_francais(m):
    """Nom français et numéro d'octave français (do3 = do du milieu = MIDI 60)."""
    return NOMS_TEX[m % 12], m // 12 - 2


def nom_international(m):
    lettres = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    return lettres[m % 12] + str(m // 12 - 1)


FONDAMENTALE_MIDI = 36   # do1 en notation française, C2 en internationale


def harmoniques(n_max=16):
    """
    Pour chaque harmonique k : fréquence, note tempérée la plus proche (MIDI),
    écart en cents à cette note.
    """
    f0 = frequence_midi(FONDAMENTALE_MIDI)
    rangs = []
    for k in range(1, n_max + 1):
        hauteur = FONDAMENTALE_MIDI + 12 * log2(k)
        proche = round(hauteur)
        rangs.append({
            "k": k,
            "f": k * f0,
            "midi": proche,
            "ecart": 100 * (hauteur - proche),
        })
    return rangs


# ---------------------------------------------------------------------------
# La spirale des quintes, depuis la 440, ramenée dans l'octave [440, 880)
# ---------------------------------------------------------------------------
CHAINE_QUINTES = ["la", "mi", "si", "fa dièse", "do dièse", "sol dièse",
                  "ré dièse", "la dièse", "mi dièse", "si dièse",
                  "fa double dièse", "do double dièse", "sol double dièse"]
EQUIVALENT_TEMPERE = {"mi dièse": "fa", "si dièse": "do",
                      "fa double dièse": "sol", "do double dièse": "ré",
                      "sol double dièse": "la"}


def spirale_quintes():
    pas = []
    r = Fraction(1)
    for k, nom in enumerate(CHAINE_QUINTES):
        if k:
            r *= QUINTE
            while r >= 2:
                r /= 2
        demi = (7 * k) % 12
        pas.append({
            "k": k,
            "nom": nom,
            "tempere_nom": EQUIVALENT_TEMPERE.get(nom, nom),
            "pyth": LA * float(r),
            "egal": LA * tempere(demi),
            # La dernière quinte retombe sur la, mais à l'octave près : 12 * 7
            # demi-tons font 7 octaves, que la réduction ci-dessus a déjà ôtées.
            "ecart": cents(r) - 100 * demi,
        })
    return pas


# ---------------------------------------------------------------------------
# Quatre systèmes d'accord, décrits par leur quinte (et, pour l'intonation
# juste, par ses rapports propres). Toutes les tailles sont en cents.
# ---------------------------------------------------------------------------
def systeme_par_quintes(q):
    """Tailles des intervalles d'un système engendré par une quinte de q cents."""
    return {
        "quinte": q,
        "ton": 2 * q - 1200,
        "tierce": 4 * q - 2400,
        "diatonique": 3600 - 5 * q,      # mi--fa, si--do
        "chromatique": 7 * q - 4800,     # do--do dièse
        "loup": 8400 - 11 * q,           # la douzième « quinte », qui ferme le cycle
    }


QUINTE_MESOTONIQUE = cents(QUINTE) - cents(COMMA_SYNTONIQUE) / 4

SYSTEMES = [
    ("pythagoricien", systeme_par_quintes(cents(QUINTE))),
    ("juste (Zarlino)", {
        "quinte": cents(QUINTE),
        "ton": cents(TON_MAJEUR),          # le ton mineur, 10/9, est noté à part
        "tierce": cents(Fraction(5, 4)),
        "diatonique": cents(Fraction(16, 15)),
        "chromatique": cents(Fraction(25, 24)),
        "loup": None,
    }),
    ("mésotonique ¼ de comma", systeme_par_quintes(QUINTE_MESOTONIQUE)),
    ("tempérament égal", systeme_par_quintes(700.0)),
]


# ---------------------------------------------------------------------------
# Les fréquences du clavier du synthétiseur (musique/synth.php), do3 à do6 en
# notation internationale. Le synthétiseur les écrit au centième, tronquées
# ou arrondies selon la note : 659,25 pour mi5, quand le calcul donne 659,255.
# ---------------------------------------------------------------------------
SYNTH_MIN, SYNTH_MAX = 50, 2000          # bornes du curseur, en hertz
SYNTH_PAS = 1.059463                     # facteur des boutons − et +


def verifier():
    """Arrête tout si une identité citée par le guide est fausse."""
    assert COMMA_PYTHAGORICIEN == Fraction(531441, 524288)
    assert COMMA_SYNTONIQUE == Fraction(81, 80)
    # Le ton majeur dépasse le ton mineur d'un comma syntonique.
    assert TON_MAJEUR / TON_MINEUR == COMMA_SYNTONIQUE
    # Les deux demi-tons pythagoriciens font un ton, et diffèrent d'un comma.
    assert LIMMA == Fraction(256, 243) and APOTOME == Fraction(2187, 2048)
    assert LIMMA * APOTOME == TON_MAJEUR
    assert APOTOME / LIMMA == COMMA_PYTHAGORICIEN
    # Deux tons, c'est la tierce pythagoricienne ; elle dépasse la juste d'un comma.
    assert TON_MAJEUR ** 2 == Fraction(81, 64)
    assert Fraction(81, 64) / Fraction(5, 4) == COMMA_SYNTONIQUE
    # Le ton juste majeur et le mineur font la tierce juste.
    assert TON_MAJEUR * TON_MINEUR == Fraction(5, 4)
    # Quinte et quarte font l'octave ; tierces majeure et mineure, la quinte.
    assert QUINTE * Fraction(4, 3) == OCTAVE
    assert Fraction(5, 4) * Fraction(6, 5) == QUINTE
    # Les renversements des rapports justes complètent l'octave.
    for nom, n, r in INTERVALLES:
        inv = [x for x in INTERVALLES if x[1] == 12 - n][0]
        if nom != "triton":
            assert r * inv[2] == OCTAVE, (nom, inv[0])
    # Douze demi-tons tempérés font l'octave ; la quinte tempérée vaut 700 cents.
    assert isclose(tempere(12), 2) and isclose(cents(tempere(7)), 700)
    # Le facteur des boutons du synthétiseur est le demi-ton, à 10⁻⁶ près.
    assert abs(SYNTH_PAS - tempere(1)) < 1e-6
    # La spirale des quintes dérive d'un comma pythagoricien par tour.
    sp = spirale_quintes()
    assert isclose(sp[-1]["ecart"], cents(COMMA_PYTHAGORICIEN))
    for p in sp:
        assert isclose(p["ecart"], p["k"] * cents(COMMA_PYTHAGORICIEN) / 12)
    # Chaque système engendré par une quinte : les deux demi-tons font le ton,
    # et leur différence est le comma de ce système (nulle au tempérament égal).
    for nom, s in SYSTEMES:
        assert isclose(s["diatonique"] + s["chromatique"], s["ton"]) or nom.startswith("juste"), nom
    pyth = dict(SYSTEMES)["pythagoricien"]
    assert isclose(pyth["chromatique"] - pyth["diatonique"], cents(COMMA_PYTHAGORICIEN))
    assert isclose(pyth["quinte"] - pyth["loup"], cents(COMMA_PYTHAGORICIEN))
    meso = dict(SYSTEMES)["mésotonique ¼ de comma"]
    assert isclose(meso["tierce"], cents(Fraction(5, 4)))       # tierces pures
    # Do dièse plus haut que ré bémol : seulement en pythagoricien.
    for nom, s in SYSTEMES:
        plus_haut = s["chromatique"] > s["diatonique"] + 1e-9
        assert plus_haut == (nom == "pythagoricien"), nom
    # La série des harmoniques retombe sur des do aux puissances de deux.
    for h in harmoniques():
        if h["k"] in (1, 2, 4, 8, 16):
            assert h["midi"] % 12 == 0 and abs(h["ecart"]) < 1e-9
    # Le comma de Holder (1/53 d'octave) se loge entre les deux commas.
    holder = 1200 / 53
    assert cents(COMMA_SYNTONIQUE) < holder < cents(COMMA_PYTHAGORICIEN)


if __name__ == "__main__":
    verifier()
    print("Contrôles du modèle des fréquences : tous passés.")
    print("comma pythagoricien : %.2f cents" % cents(COMMA_PYTHAGORICIEN))
    print("comma syntonique    : %.2f cents" % cents(COMMA_SYNTONIQUE))
