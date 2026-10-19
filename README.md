# Musique — théorie

Documents de théorie musicale composés en LaTeX, gravés avec LilyPond.

Les diagrammes d'accords de guitare vivent dans un dépôt séparé,
[fbastin/guitar_chords](https://github.com/fbastin/guitar_chords).

## Documents

Les guides se lisent dans l'ordre du tableau. *Lire les notes* ouvre la série ;
*Les intervalles* supposent les notes connues ; *Les gammes* emploient les
intervalles sans les redéfinir ; *Les fréquences* disent ce que mesurent ces
intervalles — des rapports de fréquences — et se lisent après *Les intervalles*.
*Les mordants* supposent les notes, le ton et le demi-ton connus, et prennent la
voisine d'une note dans la gamme que désigne l'armure.

| Fichier | Contenu |
| --- | --- |
| `lecture.tex` / `.pdf` | **Lire les notes — la portée, les clés, le do central.** La portée, ses lignes et interlignes comptés de bas en haut, les lignes supplémentaires, les sept noms de notes et l'octave, les clés de sol, de fa et d'ut, le do central et la grande portée vue comme une portée de onze lignes, des repères pour lire sans compter, et des exercices corrigés. |
| `intervalles.tex` / `.pdf` | **Les intervalles — du demi-ton à l'octave.** Un intervalle nommé en deux parties — un numéro compté en lettres, une qualité comptée en demi-tons —, les intervalles justes et majeurs ou mineurs, l'enharmonie, le renversement, les intervalles de la gamme majeure, la consonance et les intervalles composés. |
| `gammes.tex` / `.pdf` | **Les gammes — construction par tétracordes.** La gamme majeure vue comme deux tétracordes majeurs séparés par un ton, le cycle des quintes qui en découle, les trois formes de la gamme mineure, et la lecture d'une armure (le dernier dièse est la sensible, l'avant-dernier bémol la tonique, le relatif un ton sous le dernier dièse), démontrée. Les quinze tonalités sont tabulées, et gravées en annexe en clé de sol et en clé de fa. |
| `frequences.tex` / `.pdf` | **Les fréquences — de l'octave au comma.** Une note comme fréquence, un intervalle comme rapport : l'octave 2/1, la série des harmoniques, les cents, le ton et ses deux demi-tons, les commas pythagoricien et syntonique, les tempéraments jusqu'au tempérament égal. Chaque idée se vérifie à l'oreille avec le [synthétiseur](https://www.slashbin.net/musique/synth.php) de slashbin.net. |
| `mordants.tex` / `.pdf` | **Les mordants — du signe aux notes jouées.** Le signe barré et ses trois notes, la voisine prise dans la gamme à un ton ou à un demi-ton, l'ornement sur le temps et aussi vif sur toute valeur, les altérations, le mordant supérieur et le mordant long, le zigzag sans trait lu comme un trille chez Bach et comme un mordant supérieur plus tard, la comparaison avec le trille et le gruppetto, et un exercice corrigé. |

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
- `mordants.musicxml` — les exemples du guide des mordants et la mélodie de son exercice, écrits en toutes notes tels qu'ils se jouent

Chaque gamme y figure en clé de sol, montante puis descendante, avec son
armure et son nom.
Les mineures mélodiques descendent sous leur forme naturelle : c'est la seule
façon de rendre leur asymétrie visible. Chaque intervalle est joué note après
note, puis les deux notes ensemble.

## Compilation

Les PDF rognés des gravures étant suivis, les guides se recompilent avec LaTeX seul :

```bash
pdflatex lecture.tex         # deux fois, pour la table des matières
pdflatex gammes.tex          # deux fois aussi
pdflatex intervalles.tex     # deux fois aussi
pdflatex frequences.tex      # deux fois aussi
pdflatex mordants.tex        # deux fois aussi
```

Pour tout régénérer depuis le modèle de hauteurs — après avoir modifié une
gamme, ajouté une tonalité ou retouché une figure :

```bash
python3 outils/generer_lecture.py                    # lecture : figures .ly, tableaux, réponses des exercices
python3 outils/generer.py                            # gammes : MusicXML, figures .ly, tableaux LaTeX
python3 outils/generer_intervalles.py                # intervalles : idem
python3 outils/generer_frequences.py                 # fréquences : tableaux, figure, valeurs du texte
python3 outils/generer_mordants.py                   # mordants : figures .ly, réponses, MusicXML
(cd gravures && lilypond -dcrop --formats=pdf *.ly)  # gravures
pdflatex lecture.tex                                 # deux fois
pdflatex gammes.tex                                  # deux fois
pdflatex intervalles.tex                             # deux fois
pdflatex frequences.tex                              # deux fois
pdflatex mordants.tex                                # deux fois
```

### Un modèle, des générateurs

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

`outils/generer_lecture.py` repose sur le même modèle et sur une seule donnée
par clé : la ligne qu'elle désigne et la note qu'elle y place. La note de chaque
position, les noms sous les gravures, le tableau des repères et les réponses des
exercices en découlent ; le générateur vérifie d'abord ce que le guide affirme
(le do central sur la première ligne supplémentaire dans les deux clés, la
grande portée de onze lignes, l'écart de deux noms entre clé de sol et clé de fa).

`outils/frequences.py` fait de même pour le guide des fréquences, qui cite des
dizaines de nombres : commas, tailles de demi-tons, écarts en cents, fréquences
en hertz. Il les calcule en fractions exactes quand le rapport est rationnel et
vérifie chaque identité que le texte affirme (le ton majeur dépasse le mineur
d'un comma syntonique, les deux demi-tons pythagoriciens diffèrent d'un comma
pythagoricien, la tierce mésotonique est juste…) avant que
`outils/generer_frequences.py` n'écrive quoi que ce soit. Les nombres cités
dans le texte passent par des macros (`gravures/freq-valeurs.tex`) : le texte et
les tableaux ne peuvent pas se contredire.

`outils/generer_mordants.py` traite un ornement comme une règle : un motif joué
vite — la note et sa voisine du dessous pour le mordant —, puis la note
principale tenue jusqu'au bout de sa valeur. La voisine prend son altération de
l'armure, sauf altération écrite près du signe. Les portées « joué » des
gravures, les réponses de l'exercice et le fichier MusicXML en dérivent ; le
générateur vérifie d'abord ce que le texte affirme (la voisine à un ton ou à un
demi-ton selon la gamme, l'ornement de même durée sur toute valeur, chaque
valeur écrite respectée). Le zigzag sans trait y a deux lectures, celle de Bach
et celle du XIXe siècle, gravées l'une sous l'autre. Le fichier MusicXML écrit
les ornements en toutes notes plutôt qu'avec leurs signes, que tous les
logiciels ne savent pas jouer.

`outils/musicxml.py` traite une subtilité qui mérite d'être nommée : `<alter>`
porte le *son*, `<accidental>` porte ce qui est *imprimé*. Une altération ne
s'écrit que si elle contredit l'armure en vigueur, laquelle repart à chaque
barre de mesure — un bécarre apparaît donc là où elle s'annule, et nulle part
ailleurs.

### Dépendances

- LaTeX : `geometry`, `xcolor`, `titlesec`, `fancyhdr`, `booktabs`, `longtable`,
  `mdframed`, `enumitem`, `adjustbox`, `babel` (français), `lmodern`, `hyperref`,
  `amsmath` pour le guide des fréquences, et `tikz` pour ceux des fréquences et
  de la lecture des notes
- LilyPond 2.24 ou plus récent (seulement pour régénérer les gravures)
- Python 3 (bibliothèque standard uniquement)

## Licence

[Licence MIT](LICENSE).

---
Copyright (c) 2026 Fabian Bastin
