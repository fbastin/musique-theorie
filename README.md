# Musique — théorie

Documents de théorie musicale composés en LaTeX, gravés avec LilyPond.

Les diagrammes d'accords de guitare vivent dans un dépôt séparé,
[fbastin/guitar_chords](https://github.com/fbastin/guitar_chords).

## Documents

Deux guides, à lire dans cet ordre : le second emploie les intervalles que le
premier définit.

| Fichier | Contenu |
| --- | --- |
| `intervalles.tex` / `.pdf` | **1. Les intervalles — du demi-ton à l'octave.** Un intervalle nommé en deux parties — un numéro compté en lettres, une qualité comptée en demi-tons —, les intervalles justes et majeurs ou mineurs, l'enharmonie, le renversement, les intervalles de la gamme majeure, la consonance et les intervalles composés. |
| `gammes.tex` / `.pdf` | **2. Les gammes — construction par tétracordes.** La gamme majeure vue comme deux tétracordes majeurs séparés par un ton, le cycle des quintes qui en découle, et les trois formes de la gamme mineure. Les quinze tonalités sont tabulées et gravées en annexe. |

## Partitions (MusicXML)

Les gammes et les intervalles sont aussi fournis en MusicXML 4.0, lisibles par
MuseScore, Finale, Sibelius, Dorico, Sodor Piano et la plupart des éditeurs de
partitions :

- `gammes-majeures.musicxml` — les 15 tonalités majeures
- `gammes-mineures-naturelles.musicxml` — les 15 mineures naturelles
- `gammes-mineures-harmoniques.musicxml` — les 15 mineures harmoniques
- `gammes-mineures-melodiques.musicxml` — les 15 mineures mélodiques
- `tetracordes.musicxml` — les cinq tétracordes, sur do
- `intervalles.musicxml` — les quatorze intervalles simples au-dessus de do
- `intervalles-gamme-majeure.musicxml` — de la tonique de do majeur à chacun de ses degrés
- `intervalles-renversements.musicxml` — cinq intervalles, chacun suivi de son renversement

Chaque gamme y figure montante puis descendante, avec son armure et son nom.
Les mineures mélodiques descendent sous leur forme naturelle : c'est la seule
façon de rendre leur asymétrie visible. Chaque intervalle est joué note après
note, puis les deux notes ensemble.

## Compilation

Les PDF rognés des gravures étant suivis, les guides se recompilent avec LaTeX seul :

```bash
pdflatex gammes.tex          # deux fois, pour la table des matières
pdflatex intervalles.tex
```

Pour tout régénérer depuis le modèle de hauteurs — après avoir modifié une
gamme, ajouté une tonalité ou retouché une figure :

```bash
python3 outils/generer.py                      # gammes : MusicXML, figures .ly, tableaux LaTeX
python3 outils/generer_intervalles.py          # intervalles : idem
lilypond -dcrop --formats=pdf gravures/*.ly    # gravures
pdflatex gammes.tex                            # deux fois
pdflatex intervalles.tex                       # deux fois
```

### Pourquoi un générateur

`outils/gammes.py` contient un modèle de hauteurs unique, dont dérivent à la
fois les gravures et les fichiers MusicXML. Une hauteur y est un couple
*(lettre, altération)* et non un numéro de demi-ton, ce qui permet d'obtenir si
dièse majeur ou ré dièse mineur harmonique — avec son double dièse — sans cas
particulier. Écrire le guide et les fichiers MusicXML séparément aurait garanti
qu'ils finissent par se contredire.

`outils/intervalles.py` bâtit les intervalles sur ce même modèle : un
intervalle y est un couple *(numéro, qualité)*. Construire puis analyser un
intervalle redonne le même nom, et chaque renversement complète l'octave — le
générateur le vérifie sur toutes les toniques des gammes avant d'écrire quoi
que ce soit (`python3 outils/intervalles.py` lance ces contrôles seuls).

`outils/musicxml.py` traite une subtilité qui mérite d'être nommée : `<alter>`
porte le *son*, `<accidental>` porte ce qui est *imprimé*. Une altération ne
s'écrit que si elle contredit l'armure en vigueur, laquelle repart à chaque
barre de mesure — un bécarre apparaît donc là où elle s'annule, et nulle part
ailleurs.

### Dépendances

- LaTeX : `geometry`, `xcolor`, `titlesec`, `fancyhdr`, `booktabs`, `longtable`,
  `mdframed`, `adjustbox`, `babel` (français), `hyperref`
- LilyPond 2.24 ou plus récent (seulement pour régénérer les gravures)
- Python 3 (bibliothèque standard uniquement)

## Licence

[Licence MIT](LICENSE).

---
Copyright (c) 2026 Fabian Bastin
