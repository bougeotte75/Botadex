# Botadex — contexte pour Claude

## Le projet
App d'apprentissage de la reconnaissance des plantes communes (« pokédex » + « Duolingo » du végétal), en commençant par Paris. POC en web app. À terme : packages gratuits et payants (DLC).

Langue du projet : **français** (docs, contenu, messages de commit).

## Principes
- **Fiabilité du contenu avant tout.** Chaque affirmation d'une fiche espèce est sourcée (Tela Botanica/eFlore, INPN, Flora Gallica, Sauvages de ma rue…). Les connaissances de Claude ne sont jamais une source. Une fiche n'est `verifie` qu'après recoupement des sources.
- **Une espèce = une fiche**, dans `contenu/especes/<nom-scientifique-en-kebab>.yaml`. Les packages (`contenu/packages/<id>/package.yaml`) *référencent* les espèces, ils ne les contiennent pas.
- **Licences** : chaque photo et chaque source porte sa licence et un champ `usage_commercial` (oui/non). Pas de contenu « NC » dans un package payant.
- **Mécaniques de jeu = expériences** : chaque fiche dans `docs/mecaniques/` suit le modèle hypothèse / règles / test / résultats.
- **Données brutes** dans `data/raw/` (ignoré par git). Tout ce qui est dérivé est reproductible via `scripts/` et rangé dans `data/processed/`.
- Décisions structurantes consignées dans `docs/decisions/` (une note numérotée par décision).

## État d'avancement
- [x] Nom choisi : Botadex
- [x] Squelette du repo
- [ ] Import et analyse du jeu « Les arbres » (Paris Open Data) → comptage par espèce, niveaux de rareté
- [ ] Liste des espèces du package « Arbres communs »
- [ ] Premières fiches espèces
- [ ] Spécification des premières mécaniques (répétition espacée, paires de confusion)
- [ ] POC web app

## Notes techniques
- opendata.paris.fr coupe les connexions depuis l'environnement cloud de Claude : le CSV « Les arbres » est téléchargé en local par l'utilisatrice et placé dans `data/raw/`.
