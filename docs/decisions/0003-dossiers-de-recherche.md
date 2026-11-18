# 0003 — Un dossier de recherche à côté de chaque fiche jeu

**Date** : 2026-11-18

## Contexte
Une fiche jeu intéressante demande de collecter beaucoup plus d'informations qu'elle n'en affiche. Il faut un endroit pour tout ce qui est collecté, sourcé, et un moyen de choisir ce qui entre dans le jeu sans perdre la trace de l'origine de chaque phrase.

## Décision
- Chaque genre a son dossier `contenu/genres/<genre>/` :
  - `fiche.yaml` — la fiche jeu, courte et sélectionnée (schéma `schema/genre.schema.json`) ;
  - `recherche.md` — le dossier de recherche : des **notes** numérotées (`TIL-001`…), une information chacune, avec source, date de consultation et statut (`à trier`, `retenu`, `écarté`, `à vérifier`), rangées par rubriques fixes ;
  - `photos.md` — les photos candidates (`TIL-P001`…), avec licence et usage commercial.
- La fiche jeu ne recopie pas les sources : chaque affirmation cite les **notes** qui la justifient et est rédigée avec nos mots.
- Les notes reformulent les sources ; citation exacte courte seulement quand la formulation compte.
- Les recherches sur une espèce vont dans le dossier du genre, rubrique « Espèce — *Nom scientifique* ».
- `scripts/verifier_contenu.py` contrôle la cohérence (schéma, notes citées existantes, sourcées et non écartées, photos licenciées, préfixes uniques).
- Support : Markdown et YAML dans le repo (une seule source de vérité, historique git).

## Conséquences
- Les squelettes sont générés par `scripts/generer_fiches_genres.py` à partir des modèles `contenu/genres/_modele/`.
- Le format des fiches espèces (`contenu/especes/`, `schema/espece.schema.json`) reste à aligner sur ce principe (notes plutôt que sources), quand on attaquera la première espèce.
