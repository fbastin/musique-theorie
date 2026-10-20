# Musique — théorie

Documents de théorie musicale composés en LaTeX, gravés avec LilyPond.

Les diagrammes d'accords de guitare vivent dans un dépôt séparé,
[fbastin/guitar_chords](https://github.com/fbastin/guitar_chords).

## Documents

Les guides s'inspirent du programme de matières théoriques de l'École de musique
Vincent-d'Indy, du niveau 1 au niveau 6, et les cadences des niveaux 7 et 8 : la
colonne *Niveaux* dit à quels niveaux ce programme place les notions de chaque
guide. Ils se lisent dans l'ordre du tableau, chacun après ceux dont il a
besoin. *Lire les notes* ouvre la série ; *Les valeurs* puis *La mesure*
traitent de la durée ; *Les intervalles* supposent les notes connues ; *Les
gammes* emploient les intervalles sans les redéfinir. *Les ornements* et *Les
mordants* prennent la voisine d'une note dans la gamme que désigne l'armure ;
*L'interprétation* suppose les valeurs et la mesure ; *Les tonalités* et *Les
accords* partent des gammes ; *Les cadences*, des niveaux 7 et 8, enchaînent ces
accords. *Les fréquences*, hors programme, disent ce que mesurent les
intervalles — des rapports de fréquences — et se lisent après *Les intervalles*.

| Fichier | Niveaux | Contenu |
| --- | --- | --- |
| `lecture.tex` / `.pdf` | 1, 2, 3, 6 | **Lire les notes — la portée, les clés, le do central.** La portée, ses lignes et interlignes comptés de bas en haut, les lignes supplémentaires et le signe d'octave, les sept noms de notes, l'octave et le diapason, les sept clés (sol 2e ligne, ut 1re à 4e lignes, fa 3e et 4e lignes) et la clé de sol octaviée, le do central et la grande portée vue comme une portée de onze lignes, des repères pour lire sans compter, les altérations (dièse, bémol, bécarre et doubles altérations, accidentelles ou à l'armure, la liaison qui les prolonge, la précaution), et des exercices corrigés en clé de sol, de fa et d'ut 1re ligne, et sur les altérations. |
| `valeurs.tex` / `.pdf` | 1 à 4 | **Les valeurs — de la ronde aux groupes irréguliers.** Les sept figures de notes et leurs silences, la carrée et le bâton de pause, les mesures à compter, la tête, la hampe, le crochet et la ligature, l'arbre des valeurs, le point d'augmentation, le double et le triple point, la liaison de prolongation distinguée de la liaison d'expression, le point d'orgue et le point d'arrêt, le triolet et le sextolet, puis le duolet, le quartolet et les autres groupes irréguliers, avec des exercices corrigés. |
| `mesure.tex` / `.pdf` | 1 à 6 | **La mesure — du temps aux mesures composées.** La pulsation et le temps, les barres de mesure, la lecture des chiffres indicateurs, le C et le C barré, les mesures simples avec leur unité de temps et leur unité de mesure, les temps forts, mi-forts et faibles, les parties du temps, la battue et l'anacrouse, ou levée, les mesures composées, leur temps ternaire et la sicilienne, les mesures correspondantes avec le triolet, le duolet et l'hémiole, la syncope, la syncopette et le contretemps, les mesures irrégulières, et trois exercices corrigés. |
| `intervalles.tex` / `.pdf` | 2 à 6 | **Les intervalles — du demi-ton à l'octave.** Un intervalle nommé en deux parties — un numéro compté en lettres, une qualité comptée en demi-tons —, ascendant ou descendant, conjoint ou disjoint, les intervalles justes et majeurs ou mineurs et leurs abréviations (3ce m, 5te J), les formes augmentées, diminuées, sur-augmentées et sous-diminuées, l'enharmonie et les deux demi-tons, diatonique et chromatique, le renversement, les intervalles de la gamme majeure, la consonance et les intervalles composés, ou redoublés. |
| `gammes.tex` / `.pdf` | 1, 3, 5, 6 | **Les gammes — construction par tétracordes.** La gamme majeure vue comme deux tétracordes majeurs séparés par un ton, le cycle des quintes qui en découle, les trois formes de la gamme mineure et ses parentés, relative et directe, avec la majeure, la gamme chromatique et son écriture, la gamme pentatonique et la gamme par tons, et la lecture d'une armure (le dernier dièse est la sensible, l'avant-dernier bémol la tonique, le relatif un ton sous le dernier dièse), démontrée. Les quinze tonalités sont tabulées, et gravées en annexe en clé de sol et en clé de fa. |
| `ornements.tex` / `.pdf` | 3, 5 | **Les ornements — de l'appogiature à la fioriture.** Les petites notes et les signes, l'appogiature (la moitié de la note, les deux tiers d'une note pointée, toute la note devant un silence), l'appogiature brève ou acciaccatura, les deux mordants en bref, le trille (sa vitesse, sa note de départ selon l'époque, sa terminaison), le trémolo (sur une note, mesuré ou non, et sur deux notes), le gruppetto (sur la note, après la note, renversé, avec ses altérations), la fioriture, un tableau récapitulatif et un exercice corrigé. |
| `mordants.tex` / `.pdf` | 3, 5 | **Les mordants — du signe aux notes jouées.** Le mordant inférieur (zigzag barré) et le mordant supérieur (sans trait) côte à côte, la voisine prise dans la gamme à un ton ou à un demi-ton, l'ornement sur le temps et aussi vif sur toute valeur, les altérations, les noms des deux mordants, le mordant long, le trille (son signe, sa vitesse, sa note de départ selon l'époque, sa terminaison, le trille altéré, le mordant supérieur comme son début), le zigzag sans trait lu comme un trille chez Bach et comme un mordant supérieur plus tard, et un exercice corrigé. |
| `interpretation.tex` / `.pdf` | 4, 5 | **L'interprétation — mouvements, nuances, articulations, caractère.** Les mouvements du plus lent au plus vif, avec leur sens littéral et des fourchettes métronomiques indicatives, les changements de mouvement (jusqu'à *l'istesso tempo* et *ad libitum*), les nuances et leurs changements progressifs ou soudains (*rinforzando*, *smorzando*…), les sept articulations usuelles, leurs combinaisons et ce qu'elles laissent de la valeur écrite, les termes de caractère et les mots qui les modifient, les reprises et les signes de répétition, et des exercices corrigés. |
| `tonalites.tex` / `.pdf` | 5, 6 | **Les tonalités — des tons voisins aux modes anciens.** La tonalité et son mode, les notes tonales et modales, le relatif et l'homonyme (tonalités directes), les cinq tons voisins sur le cercle des quintes, la modulation, la note modulante et l'accord pivot, la modulation vers l'homonyme et vers les tons éloignés, l'emprunt et la tierce picarde, la transposition écrite, par changement de clé et pour les instruments transpositeurs, les sept modes anciens, leurs tétracordes, leur note caractéristique et leur échelle sur une même finale, et des exercices corrigés. |
| `accords.tex` / `.pdf` | 5, 6 | **Les accords — de l'accord parfait à la septième diminuée.** L'accord bâti en tierces superposées, les quatre accords de trois sons, l'accord de chaque degré en majeur et en mineur harmonique, la position fondamentale et les renversements avec leur chiffrage (5, 6, 6/4), la septième de dominante, sa résolution et ses renversements (V7, V6/5, V4/3, V2), la septième diminuée et sa symétrie, une méthode pour reconnaître un accord écrit, les symboles anglo-saxons (C, Cm, G7, C/E), et un exercice corrigé. |
| `cadences.tex` / `.pdf` | 7, 8 | **Les cadences.** La cadence comme ponctuation de la phrase ; les cadences parfaite, imparfaite, plagale, la demi-cadence et la cadence rompue, avec leur tronc commun et leurs variantes ; leur forme en mineur ; la préparation par IV ou II6, la septième de dominante et la quarte et sixte de cadence ; des enchaînements courants ; au clavier, deux dispositions courantes : quatre voix, deux par main, et le style clavier, trois sons à la main droite et la basse seule, avec ses positions, et deux tableaux de I–IV–V–I et I–V7–I dans les trente tonalités, majeur et mineur homonymes sur la même ligne ; les règles des voix ; d'un ouvrage à l'autre, un tableau des définitions (Wikipédia, Apprendre le solfège, usages américain et britannique) ; des exercices corrigés à reconnaître, à réaliser et à écouter. |
| `frequences.tex` / `.pdf` | hors programme | **Les fréquences — de l'octave au comma.** Une note comme fréquence, un intervalle comme rapport : l'octave 2/1, la série des harmoniques, les cents, le ton et ses deux demi-tons, les commas pythagoricien et syntonique, les tempéraments jusqu'au tempérament égal. Chaque idée se vérifie à l'oreille avec le [synthétiseur](https://www.slashbin.net/musique/synth.php) de slashbin.net. |

## Partitions (MusicXML)

Les exemples des guides sont aussi fournis en MusicXML 4.0, lisibles par
MuseScore, Finale, Sibelius, Dorico, Sodor Piano et la plupart des éditeurs de
partitions :

- `valeurs.musicxml` — les exemples du guide des valeurs, de la ronde à la quadruple croche jusqu'aux groupes irréguliers, et les groupes de son exercice, à la noire 60
- `mesure.musicxml` — les exemples du guide de la mesure, anacrouse, sicilienne, hémiole et syncopettes comprises, puis ses deux exercices gravés, avec leurs chiffres indicateurs
- `intervalles.musicxml` — les quatorze intervalles simples au-dessus de do
- `intervalles-gamme-majeure.musicxml` — de la tonique de do majeur à chacun de ses degrés
- `intervalles-renversements.musicxml` — cinq intervalles, chacun suivi de son renversement
- `tetracordes.musicxml` — les cinq tétracordes, sur do
- `gammes-majeures.musicxml` — les 15 tonalités majeures
- `gammes-mineures-naturelles.musicxml` — les 15 mineures naturelles
- `gammes-mineures-harmoniques.musicxml` — les 15 mineures harmoniques
- `gammes-mineures-melodiques.musicxml` — les 15 mineures mélodiques
- `gammes-autres.musicxml` — la gamme chromatique, montante avec des dièses, descendante avec des bémols, puis la pentatonique et la gamme par tons, sur do
- `ornements.musicxml` — les exemples du guide des ornements, trémolo compris, et la mélodie de son exercice, écrits en toutes notes tels qu'ils se jouent ; le trille y figure sous ses deux lectures
- `mordants.musicxml` — les exemples du guide des mordants et la mélodie de son exercice, écrits en toutes notes tels qu'ils se jouent ; le trille long et le zigzag sans trait y figurent sous leurs deux lectures
- `interpretation.musicxml` — *Au clair de la lune* sous chaque articulation, accent cumulé avec le point compris, nuance et mouvement, un ritardando suivi d'un a tempo, puis les reprises, les signes de répétition joués en toutes notes et les exercices du guide d'interprétation
- `tonalites.musicxml` — do majeur, son relatif et son homonyme, deux modulations et un accord pivot, une mélodie transposée, les sept modes sur les touches blanches puis sur ré
- `accords.musicxml` — les accords des gravures du guide des accords, puis ceux de son exercice, une ronde chacun
- `cadences.musicxml` — les enchaînements du guide à quatre voix, deux par main, sur une grande portée de piano, un accord par blanche, puis les exemples du style clavier (I–V7–I en do majeur, la majeur et la mineur, I–IV–V–I dans les trois positions) et les six enchaînements de l'exercice d'écoute, sans leur nom
- `cadences-tonalites.musicxml` — I–IV–V–I et I–V7–I en style clavier, position d'octave, dans les trente tonalités, chaque majeur suivi de son homonyme mineur

Chaque gamme y figure en clé de sol, montante puis descendante, avec son
armure et son nom.
Les mineures mélodiques descendent sous leur forme naturelle : c'est la seule
façon de rendre leur asymétrie visible. Chaque intervalle est joué note après
note, puis les deux notes ensemble.

## Compilation

Les PDF rognés des gravures étant suivis, les guides se recompilent avec LaTeX seul :

```bash
pdflatex lecture.tex          # deux fois, pour la table des matières
pdflatex valeurs.tex          # deux fois aussi
pdflatex mesure.tex           # deux fois aussi
pdflatex intervalles.tex      # deux fois aussi
pdflatex gammes.tex           # deux fois aussi
pdflatex ornements.tex        # deux fois aussi
pdflatex mordants.tex         # deux fois aussi
pdflatex interpretation.tex   # deux fois aussi
pdflatex tonalites.tex        # deux fois aussi
pdflatex accords.tex          # deux fois aussi
pdflatex cadences.tex         # deux fois aussi
pdflatex frequences.tex       # deux fois aussi
```

Pour tout régénérer depuis le modèle de hauteurs — après avoir modifié une
gamme, ajouté une tonalité ou retouché une figure :

```bash
python3 outils/generer_lecture.py                    # lecture : figures .ly, tableaux, réponses des exercices
python3 outils/generer_valeurs.py                    # valeurs : figures .ly, tableau, exercices, MusicXML
python3 outils/generer_mesure.py                     # mesure : figures .ly, tableaux, exercices, réponses, MusicXML
python3 outils/generer_intervalles.py                # intervalles : MusicXML, figures .ly, tableaux LaTeX
python3 outils/generer.py                            # gammes : idem
python3 outils/generer_ornements.py                  # ornements : figures .ly, réponses, MusicXML
python3 outils/generer_mordants.py                   # mordants : figures .ly, réponses, MusicXML
python3 outils/generer_interpretation.py             # interprétation : tableaux, figures .ly, exercices, MusicXML
python3 outils/generer_tonalites.py                  # tonalités : figures .ly, cercle, tableau des modes, réponses, MusicXML
python3 outils/generer_accords.py                    # accords : figures .ly, tableaux, réponses, MusicXML
python3 outils/generer_cadences.py                   # cadences : figures .ly, réponses, MusicXML
python3 outils/generer_frequences.py                 # fréquences : tableaux, figure, valeurs du texte
(cd gravures && lilypond -dcrop --formats=pdf *.ly)  # gravures
pdflatex lecture.tex                                 # puis chaque guide, deux fois
```

### Un modèle, des générateurs

`outils/gammes.py` contient un modèle de hauteurs unique, dont dérivent à la
fois les gravures et les fichiers MusicXML. Une hauteur y est un couple
*(lettre, altération)* et non un numéro de demi-ton, ce qui permet d'obtenir si
dièse majeur ou ré dièse mineur harmonique — avec son double dièse — sans cas
particulier. Écrire le guide et les fichiers MusicXML séparément aurait garanti
qu'ils finissent par se contredire. `outils/generer.py`, qui en tire les gammes, vérifie
aussi l'écriture de la gamme chromatique et la symétrie de la gamme par tons.

`outils/intervalles.py` bâtit les intervalles sur ce même modèle : un
intervalle y est un couple *(numéro, qualité)*. Construire puis analyser un
intervalle redonne le même nom, et chaque renversement complète l'octave — le
générateur le vérifie sur toutes les toniques des gammes avant d'écrire quoi
que ce soit (`python3 outils/intervalles.py` lance ces contrôles seuls). Il
vérifie aussi qu'un intervalle redoublé gagne sept lettres et douze demi-tons.

`outils/generer_lecture.py` repose sur le même modèle et sur une seule donnée
par clé : la ligne qu'elle désigne et la note qu'elle y place. La note de chaque
position, les noms sous les gravures, le tableau des sept clés, celui des repères
et les réponses des exercices en découlent ; le générateur vérifie d'abord ce que
le guide affirme (le do central sur la première ligne supplémentaire en clé de sol
et en clé de fa, la grande portée de onze lignes, l'écart de deux noms entre clé
de sol et clé de fa, la tierce qui sépare chaque clé de la suivante et donne à
chaque position les sept noms). Les altérations s'y lisent selon une règle :
une altération écrite vaut pour sa position jusqu'à la barre, l'armure sinon,
et une liaison la prolonge sur la note liée ; le générateur vérifie que chaque
signe gravé est exigé par la règle, sauf ceux de précaution.

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
vite — la note et sa voisine du dessous pour le mordant inférieur —, puis la
note principale tenue jusqu'au bout de sa valeur. Le trille y alterne la note et
sa voisine du dessus jusqu'au bout de la valeur, commencé sur la voisine ou sur
la note selon l'époque, avec ou sans terminaison. La voisine prend son altération de
l'armure, sauf altération écrite près du signe. Les portées « joué » des
gravures, les réponses de l'exercice et le fichier MusicXML en dérivent ; le
générateur vérifie d'abord ce que le texte affirme (la voisine à un ton ou à un
demi-ton selon la gamme, l'ornement de même durée sur toute valeur, chaque
valeur écrite respectée, le mordant supérieur identique au début d'un trille
commencé sur la note). Le zigzag sans trait y a deux lectures, celle de Bach
et celle du XIXe siècle, gravées l'une sous l'autre. Le fichier MusicXML écrit
les ornements en toutes notes plutôt qu'avec leurs signes, que tous les
logiciels ne savent pas jouer.

`outils/generer_valeurs.py` traite une valeur comme une fraction de ronde, et un
rythme comme une suite de notes, de silences, de ligatures et de groupes
irréguliers dont la durée se calcule. Les gravures, le tableau des figures, les
deux exercices et leurs réponses, et le fichier MusicXML en dérivent ; le
générateur vérifie d'abord ce que le texte affirme (chaque figure vaut deux fois
la suivante, le point ajoute la moitié de la valeur, le triple point et la
carrée qui vaut deux rondes, cinq croches ne s'écrivent
pas d'une seule figure, un groupe irrégulier dure autant que la division
régulière qu'il remplace et en garde la figure), et que les deux portées de
chaque figure comparative durent autant l'une que l'autre.

`outils/generer_mesure.py` ne part que du chiffre indicateur. Il en déduit le
genre de la mesure (simple, composée, irrégulière), le nombre de temps, l'unité
de temps et l'unité de mesure, la mesure correspondante, et la force de chaque
temps et de chaque partie de temps. Les tableaux, les numéros et les forces
gravés sous les temps, la reconnaissance des syncopes et des contretemps et les
réponses des exercices en découlent. Le générateur vérifie d'abord ce que le
texte affirme : les unités de chaque mesure, les correspondances 2/4–6/8 et
suivantes, chaque mesure complète, le triolet à 2/4 qui attaque comme une
mesure à 6/8, les syncopes et contretemps des exemples, la sicilienne qui
remplit un temps ternaire, la syncopette, les trois appuis de l'hémiole, et un
seul chiffre possible pour chaque mesure de l'exercice.

`outils/generer_ornements.py` prolonge le générateur des mordants, dont il
reprend le modèle et la règle du mordant, du trille et du gruppetto. L'appogiature y prend
la moitié d'une valeur simple, les deux tiers d'une valeur pointée et toute la
note devant un silence ; l'appogiature brève, une triple croche sur toute
valeur ; le trille alterne jusqu'au bout de la valeur, commencé sur la voisine
ou sur la note selon l'époque, et s'achève sur la note ; le gruppetto tourne
autour d'elle, sur la note ou après elle ; le trémolo répète la note, ou en
alterne deux, à la valeur que donnent ses barres. Le générateur vérifie d'abord ce que
le texte affirme, puis écrit les portées « joué », les réponses de l'exercice et
le fichier MusicXML, où les ornements sont écrits en toutes notes.

`outils/generer_interpretation.py` tient les termes du guide d'interprétation
dans des listes : les mouvements et leurs fourchettes, les nuances, les
articulations et la part de la valeur que chacune laisse, les termes de
caractère. Les tableaux, les énoncés et les réponses des exercices et le fichier
MusicXML en dérivent. Le générateur vérifie d'abord ce que le texte affirme :
les fourchettes ordonnées, les nuances graduées, le staccatissimo plus bref que
le staccato, les signes cumulés, chaque mot à traduire présent dans les
tableaux, l'ordre dans lequel se jouent des mesures reprises, chaque signe de
répétition qui redonne son motif. Le fichier MusicXML porte les indications
comme une partition ; le ritardando y est en plus inscrit temps par temps.

`outils/generer_tonalites.py` traite une tonalité comme un couple *(tonique,
mode)* ; son armure, son relatif, son homonyme et ses tons voisins s'en
déduisent sur le modèle de hauteurs commun. Une transposition y déplace chaque
note d'un même intervalle, et un mode ancien fait tourner la gamme majeure.
Avant d'écrire quoi que ce soit, le générateur vérifie ce que le texte affirme :
les cinq tons voisins sur trois armures consécutives et sur les degrés de la
gamme, les notes modales seules à changer d'un mode à l'autre, la transposition
qui conserve chaque intervalle et l'effet de chaque altération accidentelle, les
tétracordes de chaque mode, l'échelle des modes sur ré, qui perd une
altération à chaque marche, l'accord pivot, la dominante commune à l'homonyme
et la septième diminuée commune à quatre tonalités mineures.

`outils/generer_accords.py` bâtit un accord comme une pile de tierces prise dans
une gamme, majeure ou mineure harmonique : la fondamentale, puis une lettre sur
deux. Chaque accord construit est ensuite analysé à partir de ses seules notes,
comme le ferait un lecteur : rangées en tierces, elles désignent la
fondamentale ; les intervalles qu'elle forme donnent la nature, la basse la
position et le chiffrage. L'analyse doit retrouver la construction. Le
générateur vérifie d'abord, sur les quinze tonalités majeures et mineures, ce
que le texte affirme : la nature de l'accord de chaque degré, la septième de
dominante seule sur V et identique en majeur et en mineur, les trois tierces
mineures de la septième diminuée et ses trois seules sonorités, le chiffrage
complet et abrégé de chaque renversement. Le symbole anglo-saxon de chaque
accord se déduit de la même analyse.

`outils/generer_cadences.py` réalise chaque enchaînement dans deux dispositions
courantes au clavier. À quatre voix, deux par main, le soprano reste près de la
tonique, le ténor peut rejoindre la basse à l'unisson, et sous la quarte et
sixte la basse descend à l'octave. En style clavier, la basse seule est à la
main gauche et trois sons serrés sont à la main droite, dans trois positions ;
la note commune reste en place, et de IV à V la main droite va à l'opposé de la
basse ; dans I–V7–I, V7 perd sa quinte et sa fondamentale est doublée par la
basse. Dans les deux cas, parmi les réalisations sans faute — ni quintes ni
octaves parallèles, ni mouvement augmenté, la sensible qui monte, la septième et
la quarte et sixte qui se résolvent en descendant —, le générateur retient celle
où les voix parcourent le moins de chemin. Chaque réalisation est relue à partir
de ses seules notes avec l'analyse de `generer_accords.py` : ses chiffres, puis
le nom de sa cadence. Le générateur vérifie ainsi, dans les trente tonalités, ce
que le texte affirme, et que chaque exemple du style clavier donne exactement
les accords gravés. Il grave aussi, ligne par ligne, les tableaux de I–IV–V–I et
I–V7–I dans toutes les tonalités, après avoir vérifié que chaque tonalité
usuelle y a sa case, que chaque case est sans faute dans ses trois positions, et
que les cases vides sont exactement les six tonalités à plus de sept
altérations.

`outils/musicxml.py` traite une subtilité qui mérite d'être nommée : `<alter>`
porte le *son*, `<accidental>` porte ce qui est *imprimé*. Une altération ne
s'écrit que si elle contredit l'état de la mesure à sa position — même
lettre, même octave —, lequel repart de l'armure à chaque barre de mesure — un bécarre apparaît donc là où elle s'annule, et nulle part
ailleurs.
Le même module écrit des notes de toute durée — points, liaisons, silences,
accords, groupes irréguliers, points d'orgue et articulations — pour les guides
qui ont besoin de rythme. Il écrit aussi une grande portée de piano, clé de sol et
clé de fa, pour les cadences.

### Dépendances

- LaTeX : `geometry`, `xcolor`, `titlesec`, `fancyhdr`, `booktabs`, `longtable`,
  `array`, `mdframed`, `enumitem`, `adjustbox`, `multicol`, `needspace`, `babel`
  (français), `lmodern`, `hyperref`, `amsmath` pour les guides des fréquences et
  des accords, et `tikz` pour ceux des fréquences, de la lecture des notes et des
  tonalités
- LilyPond 2.24 ou plus récent (seulement pour régénérer les gravures)
- Python 3 (bibliothèque standard uniquement)

## Licence

[Licence MIT](LICENSE).

---
Copyright (c) 2026 Fabian Bastin
