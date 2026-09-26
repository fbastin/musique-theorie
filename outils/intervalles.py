#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle des intervalles, sur le modèle de hauteurs de `gammes.py`.

Un intervalle a deux coordonnées, comme une hauteur : son *numéro* se compte
en lettres (do–mi est une tierce, quelles que soient les altérations), sa
*qualité* en demi-tons (quatre pour une tierce majeure, trois pour une
mineure). C'est ce qui distingue une seconde augmentée d'une tierce mineure,
qui sonnent pareil : elles n'enjambent pas le même nombre de lettres.
"""

from gammes import LETTRES, Note

# Demi-tons de l'intervalle juste ou majeur, par numéro (1 = unisson).
REFERENCE = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11, 8: 12}
# Les numéros « justes » : unisson, quarte, quinte, octave. Les autres sont
# majeurs ou mineurs.
JUSTES = {1, 4, 5, 8}

# Écart à la référence, selon la qualité et la famille.
ECART_JUSTE = {"diminuée": -1, "juste": 0, "augmentée": 1}
ECART_MAJEUR = {"diminuée": -2, "mineure": -1, "majeure": 0, "augmentée": 1}

NOMS = {1: "unisson", 2: "seconde", 3: "tierce", 4: "quarte", 5: "quinte",
        6: "sixte", 7: "septième", 8: "octave"}
ABREGES = {1: "1", 2: "2de", 3: "3ce", 4: "4te", 5: "5te", 6: "6te", 7: "7e", 8: "8ve"}
QUALITES_ABREGEES = {"juste": "J", "majeure": "M", "mineure": "m",
                     "augmentée": "aug.", "diminuée": "dim."}

# Le renversement échange les qualités, et les numéros se complètent à 9.
RENVERSE = {"juste": "juste", "majeure": "mineure", "mineure": "majeure",
            "augmentée": "diminuée", "diminuée": "augmentée"}


def demi_tons(numero, qualite):
    """Taille d'un intervalle simple, en demi-tons."""
    ecarts = ECART_JUSTE if numero in JUSTES else ECART_MAJEUR
    if qualite not in ecarts:
        raise ValueError(f"une {NOMS[numero]} ne peut être {qualite}")
    return REFERENCE[numero] + ecarts[qualite]


def au_dessus(note, numero, qualite):
    """La note située à cet intervalle au-dessus de `note`."""
    rang = note.idx + numero - 1
    lettre = LETTRES[rang % 7]
    octave = note.octave + rang // 7
    cible = note.hauteur + demi_tons(numero, qualite)
    base = Note(lettre, 0, octave).hauteur
    return Note(lettre, cible - base, octave)


def analyser(grave, aigu):
    """(numéro, qualité) de l'intervalle simple entre deux notes, grave d'abord."""
    numero = (aigu.idx - grave.idx) % 7 + 1
    if numero == 1 and aigu.hauteur - grave.hauteur >= 11:
        numero = 8
    taille = aigu.hauteur - grave.hauteur
    ecarts = ECART_JUSTE if numero in JUSTES else ECART_MAJEUR
    for qualite, ecart in ecarts.items():
        if REFERENCE[numero] + ecart == taille:
            return numero, qualite
    raise ValueError(f"intervalle hors du modèle : {grave!r} – {aigu!r}")


def renverser(numero, qualite):
    """Le renversement : la note grave passe à l'octave supérieure."""
    return 9 - numero, RENVERSE[qualite]


def nom(numero, qualite):
    """« tierce majeure », « quarte juste », « unisson »…"""
    if numero == 1:
        return "unisson"
    if numero == 8 and qualite == "juste":
        return "octave"
    return f"{NOMS[numero]} {qualite}"


def abrege(numero, qualite):
    """« 3ce M », « 4te J », « 5te dim. »…"""
    if numero == 1:
        return "unisson"
    if numero == 8 and qualite == "juste":
        return "8ve"
    return f"{ABREGES[numero]} {QUALITES_ABREGEES[qualite]}"


# Les intervalles simples, du plus petit au plus grand, avec leurs deux noms
# quand deux écritures désignent le même son (le triton).
SIMPLES = [
    (1, "juste"), (2, "mineure"), (2, "majeure"), (3, "mineure"), (3, "majeure"),
    (4, "juste"), (4, "augmentée"), (5, "diminuée"), (5, "juste"),
    (6, "mineure"), (6, "majeure"), (7, "mineure"), (7, "majeure"), (8, "juste"),
]


def verifier():
    """
    Contrôles de cohérence du modèle, sur toutes les toniques des gammes :
    construire puis analyser redonne l'intervalle, et le renversement
    complète bien à l'octave.
    """
    from gammes import TONALITES, note_de
    toniques = {t for _, maj, mi in TONALITES for t in (maj, mi)}
    for txt in toniques:
        base = note_de(txt, 4)
        for numero, qualite in SIMPLES:
            haut = au_dessus(base, numero, qualite)
            assert analyser(base, haut) == (numero, qualite), (txt, numero, qualite)
            if numero != 1 and numero != 8:
                # La note grave passée à l'octave : le renversement.
                n2, q2 = renverser(numero, qualite)
                octave = Note(base.lettre, base.alt, base.octave + 1)
                assert analyser(haut, octave) == (n2, q2), (txt, numero, qualite)
                assert demi_tons(numero, qualite) + demi_tons(n2, q2) == 12


if __name__ == "__main__":
    verifier()
    print("Modèle des intervalles : cohérent.")
