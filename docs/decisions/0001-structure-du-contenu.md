# 0001 — Structure du contenu : espèces et packages séparés

**Date** : 2026-11-16

## Contexte
L'apprentissage se fait par packages (« Arbres communs », puis « Arbres experts »…, certains payants). Une même espèce peut appartenir à plusieurs packages.

## Décision
- Tout le contenu vit dans le repo git (pas de Notion) : les fiches sont les données de l'app.
- Une fiche YAML par espèce dans `contenu/especes/`.
- Un dossier par package dans `contenu/packages/<id>/`, avec un `package.yaml` qui liste les espèces par identifiant.

## Conséquences
- Pas de doublon : une correction s'applique à tous les packages.
- Débloquer un package = débloquer une liste d'identifiants.
- Les fiches et les manifestes sont validés par les schémas de `schema/`.
