# Niveau de recherche par genre

**Statut** : spécifiée

## Hypothèse
1. **Dévoiler progressivement** évite la surcharge : on apprend d'abord à reconnaître un genre (« un tilleul »), et les espèces arrivent quand le genre est maîtrisé.
2. **Varier les tâches** (organes, saisons, sosies, terrain) multiplie les expositions différentes à un même genre, ce qui produit une reconnaissance robuste (apprentissage perceptif) plutôt qu'une mémorisation d'une photo.
3. **Rendre la progression visible par genre** (et non par session) motive à revenir vers les genres incomplets, y compris sur le terrain.

## Inspiration
*Pokémon Legends: Arceus* : chaque Pokémon a des tâches de recherche ; les accomplir fait monter son niveau de recherche jusqu'à compléter son entrée du Pokédex, puis la rendre « parfaite ». La somme des recherches fait monter le rang du joueur.

## Règles

### Points et niveaux
- Chaque genre a un compteur de **points de recherche** (0 à 100).
- **Niveau = points ÷ 10** (arrondi inférieur), de 0 à 10. Niveau 1 dès la première rencontre réussie.
- **100 points = fiche complète.** Statut **« parfait »** quand toutes les tâches sont menées à leur dernier palier (au-delà de 100 points).

### Tâches de recherche (par genre)
Chaque palier franchi rapporte ses points une seule fois.

| Tâche | Paliers | Points par palier | Débloquée au niveau |
|---|---|---|---|
| Reconnaître le genre en quiz | 1 · 5 · 20 · 50 | 5 · 5 · 5 · 5 | 0 |
| Reconnaître par organe (feuille, écorce, silhouette, hiver/bourgeon, fleur, fruit) | 1 réussite par organe | 3 par organe | 1 |
| Reconnaître à chaque saison | 1 réussite par saison | 3 par saison | 1 |
| Départager du sosie (quiz en paire) | 5 · 20 | 5 · 5 | 3 |
| Capturer sur le terrain | 1 · 5 · 20 | 10 · 5 · 5 | 1 |
| Capturer dans des milieux différents (rue, jardin, cimetière…) | 2 · 3 | 5 · 5 | 3 |
| Reconnaître l'espèce exacte | 5 · 20 | 5 · 5 | 5 |

Total des paliers : 113 points → 100 suffisent pour compléter la fiche, le reste mène au « parfait ».

### Anti-bachotage
- Une réussite en quiz ne compte pour la tâche que si la dernière réussite comptée pour ce genre date d'**au moins 20 heures** (répétition espacée).
- Les erreurs ne retirent pas de points : elles rapprochent la prochaine révision du genre.

### Contenu débloqué par niveau
Chaque affirmation d'une fiche genre porte un champ `niveau` (voir `schema/genre.schema.json`).

| Niveau | Ce qui s'affiche |
|---|---|
| 1 | Nom, critère principal, une anecdote |
| 3 | Critères par organe et par saison ; le sosie et comment le distinguer |
| 5 | Les espèces : la plus fréquente à Paris et comment la reconnaître |
| 7 | Les autres espèces courantes, quiz d'espèces |
| 10 | Fiche complète, badge |

L'ordre des espèces vient des données (`especes` de la fiche genre, triées par nombre d'arbres à Paris).

### Rang de botaniste
- **Rang = somme des points de recherche de tous les genres**, par paliers (ex. tous les 150 points).
- Un nouveau rang débloque une zone ou un package.

### Paramètres
Points, paliers, délai anti-bachotage et seuils de rang sont des paramètres à ajuster pendant les tests.

## Comment on teste
- **Prototype** : web app avec le package « Arbres communs » (16 genres), 5 à 10 testeurs, 4 semaines.
- **Mesure principale** : balade test de 20 arbres avant / après (taux de genres correctement reconnus sur le terrain, et d'espèces pour les genres au niveau ≥ 5).
- **Mesures secondaires** : distribution des niveaux par genre au fil du temps, tâches jamais tentées, abandons, nombre de sessions par semaine, part des points venant du terrain.
- **Ça marche si** : progression nette au test terrain, et au moins la moitié des testeurs atteignent le niveau 5 sur 5 genres.
- **Signaux d'échec** : points concentrés sur le quiz (le terrain est ignoré), plafonnement au niveau 3 (sosies trop difficiles), lassitude avant le niveau 5.

## Résultats
—
