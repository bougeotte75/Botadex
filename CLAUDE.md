# Botadex — contexte pour Claude

## Le projet
App d'apprentissage de la reconnaissance des plantes communes (« pokédex » + « Duolingo » du végétal), en commençant par Paris. POC en web app. À terme : packages gratuits et payants (DLC).

Langue du projet : **français** (docs, contenu, messages de commit).

## Principes
- **Fiabilité du contenu avant tout.** Chaque affirmation d'une fiche espèce est sourcée (Tela Botanica/eFlore, INPN, Flora Gallica, Sauvages de ma rue…). Les connaissances de Claude ne sont jamais une source. Une fiche n'est `verifie` qu'après recoupement des sources.
- **Le genre est l'unité d'apprentissage** (décision 0002) : une fiche par genre dans `contenu/genres/<genre>.yaml`, une fiche par espèce enseignée dans `contenu/especes/<nom-scientifique-en-kebab>.yaml`. Les packages (`contenu/packages/<id>/package.yaml`) *listent des genres* ; les espèces s'apprennent dans le genre via le niveau de recherche (`docs/mecaniques/niveau-de-recherche.md`).
- Chaque affirmation d'une fiche genre porte un `niveau` de déblocage (1 à 10).
- **Licences** : chaque photo et chaque source porte sa licence et un champ `usage_commercial` (oui/non). Pas de contenu « NC » dans un package payant.
- **Mécaniques de jeu = expériences** : chaque fiche dans `docs/mecaniques/` suit le modèle hypothèse / règles / test / résultats.
- **Données brutes** dans `data/raw/` (ignoré par git). Tout ce qui est dérivé est reproductible via `scripts/` et rangé dans `data/processed/`.
- Décisions structurantes consignées dans `docs/decisions/` (une note numérotée par décision).

## État d'avancement
- [x] Nom choisi : Botadex
- [x] Squelette du repo
- [x] Import et analyse du jeu « Les arbres » (Paris Open Data) → `scripts/import_arbres.py`, comptages dans `data/processed/` ; carte d'exploration `app/carte/` (`scripts/export_carte.py`)
- [x] Package « Arbres communs » : 16 genres ; squelettes des fiches genres générés (`scripts/generer_fiches_genres.py`)
- [x] Mécanique « Niveau de recherche par genre » spécifiée
- [ ] Rédiger et sourcer les fiches genres (critères, sosies, anecdotes, photos)
- [ ] Spécifier les autres mécaniques (répétition espacée, quiz de sosies, capture terrain)
- [ ] POC web app

## Notes techniques
- Chaîne de données : `python scripts/import_arbres.py` puis `python scripts/export_carte.py` (pandas requis).
- Résultat clé : 16 genres = 80 % des arbres recensés (Platane, Marronnier, Tilleul, Érable, Sophora…).
- opendata.paris.fr coupe les connexions depuis l'environnement cloud de Claude : le CSV « Les arbres » est téléchargé en local par l'utilisatrice et placé dans `data/raw/`.
