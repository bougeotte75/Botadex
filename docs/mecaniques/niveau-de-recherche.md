# Niveau de recherche par genre

**Statut** : spécifiée (v2)

## Hypothèse
1. **Dévoiler progressivement** évite la surcharge : on apprend d'abord à reconnaître un genre (« un tilleul »), et les espèces arrivent quand le genre est maîtrisé.
2. **Varier les tâches** (organes, saisons, sosies, terrain) multiplie les expositions différentes à un même genre, ce qui produit une reconnaissance robuste (apprentissage perceptif) plutôt qu'une mémorisation d'une photo.
3. **Rendre la progression visible par genre** (et non par session) motive à revenir vers les genres incomplets, y compris sur le terrain.

## Inspiration
*Pokémon Legends: Arceus* : chaque Pokémon a des tâches de recherche ; les accomplir fait monter son niveau de recherche jusqu'à compléter son entrée du Pokédex, puis la rendre « parfaite ». La somme des recherches fait monter le rang du joueur.

## Principes
- **Botadex est un jeu d'extérieur** : le terrain rapporte l'essentiel des points. Une fiche ne peut pas être complétée depuis le canapé.
- **Deux étapes** : d'abord le genre, ensuite les espèces. Une fois l'étape « genre » franchie, **toutes** les espèces du genre sont accessibles ; ce qu'on apprend dépend de ce qu'on rencontre, pas de la rareté.
- **Temps long** : certaines tâches sont liées à une saison. Compléter une fiche demande de revenir à plusieurs moments de l'année.

## Règles

### Points et niveaux
- Chaque genre a un compteur de **points de recherche**. **Niveau = points ÷ 10** (arrondi inférieur), de 0 à 10.
- **Étape « genre »** : niveaux 1 à 4. **Étape « espèces »** : à partir du niveau 5.
- **100 points = fiche complète.** **« Parfait »** quand toutes les tâches sont menées à leur dernier palier.

### Tâches de recherche (par genre)
Chaque palier franchi rapporte ses points une seule fois.

| Tâche | Type | Paliers | Points | Total | Disponible |
|---|---|---|---|---|---|
| Reconnaître le genre en quiz | app | 1 · 10 · 30 | 2 · 2 · 2 | 6 | dès le début |
| Reconnaître par organe (feuille, écorce, silhouette, bourgeon, fleur, fruit) | app | 1 réussite par organe | 1 par organe | 6 | dès le début |
| Départager du sosie (quiz en paire) | app | 5 · 20 | 2 · 2 | 4 | niveau 2 |
| Reconnaître l'espèce exacte en quiz | app | 5 · 20 | 2 · 2 | 4 | niveau 5 |
| **Capturer sur le terrain** | terrain | 1 · 3 · 10 · 25 | 10 · 10 · 10 · 10 | **40** | dès le début |
| **Capturer dans des milieux différents** (rue, jardin, cimetière, bois…) | terrain | 2 · 3 | 5 · 5 | **10** | dès le début |
| **Capturer en saison** (hiver, printemps, été, automne) | terrain, saisonnière | 1 par saison | 6 par saison | **24** | dès le début |
| **Capturer une espèce du genre** | terrain | chaque espèce différente | 5, × bonus de rareté | **variable** | niveau 5 |

- Quiz et app : **20 points au maximum**. Le terrain : **74 points + les espèces**.
- Conséquence : sans terrain, un genre plafonne au niveau 2. Sans au moins deux saisons, il est très difficile d'atteindre 100.

### Captures d'espèces et rareté
- À partir du niveau 5, chaque capture tente d'identifier l'**espèce** de l'arbre. Si l'arbre est recensé dans le jeu de données de Paris à l'endroit de la capture, l'app connaît son espèce : elle l'annonce et ouvre sa fiche.
- La première capture de chaque espèce rapporte **5 points × bonus de rareté** (rareté de l'espèce à Paris, d'après `data/processed/taxons_arbres.csv`) :

| Rareté de l'espèce | Bonus |
|---|---|
| commune | × 1 |
| peu commune | × 2 |
| rare | × 3 |
| très rare | × 4 |

- La rareté n'influence **que** les points, jamais l'ordre ni l'accès au contenu. Un tilleul très rare au coin de la rue s'apprend dès qu'on le rencontre.

### Tâches saisonnières
- Saisons calendaires : hiver (déc.–fév.), printemps (mars–mai), été (juin–août), automne (sept.–nov.).
- Chaque genre a quatre tâches « capturer en saison », avec un indice adapté : silhouette et bourgeons en hiver, fleurs au printemps, feuilles en été, fruits et couleurs en automne.
- Pour les persistants (Pin, If) ou les genres sans fleurs visibles, les indices saisonniers sont à adapter genre par genre (cônes, pollen, fruits…).
- Les tâches saisonnières alimentent le **calendrier** (voir `calendrier.md`).

### Anti-bachotage
- Une réussite en quiz ne compte pour la tâche que si la dernière réussite comptée pour ce genre date d'**au moins 20 heures** (répétition espacée).
- Une capture ne compte que si elle a lieu à plus de **30 mètres** des captures précédentes du même genre, ou un autre jour : on cherche des arbres différents.
- Les erreurs ne retirent pas de points : elles rapprochent la prochaine révision du genre.

### Contenu débloqué par niveau

| Niveau | Ce qui s'affiche |
|---|---|
| 1 | Nom, critère principal, une anecdote |
| 2 | Critères par organe ; le sosie et comment le distinguer |
| 3 | Critères saisonniers |
| 5 | **Étape « espèces »** : la liste de toutes les espèces du genre présentes à Paris ; la fiche d'une espèce s'ouvre à sa première capture ou à sa première réussite en quiz |
| 10 | Fiche complète, badge |

Chaque affirmation d'une fiche genre porte un champ `niveau` (voir `schema/genre.schema.json`). Les espèces ne portent pas de niveau.

### Rang de botaniste
- **Rang = somme des points de recherche de tous les genres**, par paliers (ex. tous les 150 points).
- Un nouveau rang débloque une zone ou un package.

### Paramètres
Points, paliers, bonus de rareté, distance minimale entre captures, délai anti-bachotage et seuils de rang sont à ajuster pendant les tests.

## Comment on teste
- **Prototype de développement** : web app, pour construire et régler les mécaniques.
- **Premier test avec de vrais testeurs** : sur **app mobile**, puisque l'essentiel du jeu se passe dehors (géolocalisation, appareil photo, notifications). 5 à 10 testeurs, au moins 6 semaines pour couvrir un changement de saison.
- **Mesure principale** : une **balade test** de 20 arbres, tirée de la carte, au début et à la fin (taux de genres correctement reconnus sur le terrain, et d'espèces pour les genres au niveau ≥ 5).
- **Mesures secondaires** : part des points venant du terrain, nombre de captures par semaine, distribution des niveaux par genre, tâches jamais tentées, abandons.
- **Ça marche si** : progression nette à la balade test, et la majorité des testeurs sortent capturer au moins une fois par semaine.
- **Signaux d'échec** : testeurs qui restent au niveau 2 faute de sortir, captures concentrées sur un seul arbre près de chez soi, lassitude avant le niveau 5.

## Résultats
—
