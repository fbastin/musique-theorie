# Musique — théorie

Documents de théorie musicale composés en LaTeX, gravés avec LilyPond.

Les diagrammes d'accords de guitare vivent dans un dépôt séparé,
[fbastin/guitar_chords](https://github.com/fbastin/guitar_chords).

## Documents

| Fichier | Contenu |
| --- | --- |
| `gammes.tex` / `.pdf` | **Les gammes — construction par tétracordes.** La gamme majeure vue comme deux tétracordes majeurs séparés par un ton, le cycle des quintes qui en découle, et les trois formes de la gamme mineure. Les quinze tonalités sont tabulées et gravées en annexe. |

## Partitions (MusicXML)

Les gammes sont aussi fournies en MusicXML 4.0, lisibles par MuseScore, Finale,
Sibelius, Dorico et la plupart des éditeurs de partitions :

- `gammes-majeures.musicxml` — les 15 tonalités majeures
- `gammes-mineures-naturelles.musicxml` — les 15 mineures naturelles
- `gammes-mineures-harmoniques.musicxml` — les 15 mineures harmoniques
- `gammes-mineures-melodiques.musicxml` — les 15 mineures mélodiques
- `tetracordes.musicxml` — les cinq tétracordes, sur do

Chaque gamme y figure montante puis descendante, avec son armure et son nom.
Les mineures mélodiques descendent sous leur forme naturelle : c'est la seule
façon de rendre leur asymétrie visible.

## Compilation

Les PDF rognés des gravures étant suivis, le guide se recompile avec LaTeX seul :

```bash
pdflatex gammes.tex          # deux fois, pour la table des matières
```

Pour tout régénérer depuis le modèle de hauteurs — après avoir modifié une
gamme, ajouté une tonalité ou retouché une figure :

```bash
python3 outils/generer.py                      # MusicXML, figures .ly, tableaux LaTeX
lilypond -dcrop --formats=pdf gravures/*.ly    # gravures
pdflatex gammes.tex                            # deux fois
```

### Pourquoi un générateur

`outils/gammes.py` contient un modèle de hauteurs unique, dont dérivent à la
fois les gravures et les fichiers MusicXML. Une hauteur y est un couple
*(lettre, altération)* et non un numéro de demi-ton, ce qui permet d'obtenir si
dièse majeur ou ré dièse mineur harmonique — avec son double dièse — sans cas
particulier. Écrire le guide et les fichiers MusicXML séparément aurait garanti
qu'ils finissent par se contredire.

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
