# Scripts

Prérequis : Python 3 + pandas. Placer l'export CSV « Les arbres » dans `data/raw/les-arbres.csv`.

| Script | Entrée | Sortie | Rôle |
|---|---|---|---|
| `import_arbres.py` | `data/raw/les-arbres.csv` | `data/processed/taxons_arbres.csv`, `genres_arbres.csv`, `arbres_points.csv` (non versionné) | Comptage par espèce et par genre, répartition par milieu, niveaux de rareté |
| `export_carte.py` | `data/processed/*` | `app/carte/arbres.json` (non versionné) | Données compactes pour la carte d'exploration |
| `generer_fiches_genres.py` | `data/processed/*`, `contenu/genres/_modele/` | `contenu/genres/<genre>/` : `fiche.yaml`, `recherche.md`, `photos.md` (jamais réécrits) | Squelettes des dossiers genres d'un niveau de rareté |
| `verifier_contenu.py` | `contenu/` | rapport | Cohérence fiches / notes / photos / packages ; code de sortie 1 en cas d'erreur |
