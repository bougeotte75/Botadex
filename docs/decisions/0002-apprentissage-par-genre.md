# 0002 — Le genre comme unité d'apprentissage

**Date** : 2026-11-18

## Contexte
L'analyse du jeu « Les arbres » montre que 16 genres couvrent 80 % des arbres recensés à Paris, mais que la plupart regroupent plusieurs espèces (5 tilleuls, 3 platanes, une dizaine d'érables…). Distinguer les espèces est nettement plus difficile que reconnaître le genre.

Première idée écartée : un package « Arbres communs » par genre, puis un package « Arbres experts » pour les espèces.

## Décision
- L'unité d'apprentissage est le **genre**. Les espèces s'apprennent **à l'intérieur du genre**, au fil d'un niveau de recherche (voir `docs/mecaniques/niveau-de-recherche.md`).
- **Les packages élargissent** (plus de genres, d'autres milieux) ; **les niveaux approfondissent** (du genre vers les espèces).
- Nouvelle fiche **genre** dans `contenu/genres/<genre>.yaml` : critères généraux, sosies, liste des espèces présentes à Paris, contenu étiqueté par niveau de déblocage. Les fiches espèces (`contenu/especes/`) restent la source de vérité pour chaque espèce.
- Les packages listent des **genres** (`schema/package.schema.json`).

## Conséquences
- Le package « Arbres communs » = les 16 genres « communs » de l'analyse.
- Deux étapes : le genre (niveaux 1 à 4), puis les espèces (niveau 5 et plus). À l'étape « espèces », **toutes** les espèces du genre sont accessibles : on apprend celles qu'on rencontre. La rareté ne joue que sur les points de capture.
- Il faudra une fiche pour chaque espèce présente à Paris dans les genres d'un package (y compris les rares), en commençant par les plus fréquentes.
