# Botadex

Le « Duolingo du végétal » : une app pour apprendre à **reconnaître** les plantes les plus communes, en commençant par Paris.

Contrairement aux apps d'identification (on photographie, l'IA répond), Botadex entraîne l'œil de l'utilisateur : répétition espacée, espèces proches à départager, stades de la plante au fil des saisons, et « captures » sur le terrain.

## Organisation du repo

| Dossier | Contenu |
|---|---|
| `docs/` | Vision, mécaniques de jeu, inventaire des données, journal des décisions |
| `contenu/especes/` | Une fiche YAML par espèce (source de vérité unique) |
| `contenu/packages/` | Les packages d'apprentissage (« Arbres communs »…), qui référencent les espèces |
| `schema/` | Schémas JSON de validation des fiches et des packages |
| `data/raw/` | Données brutes téléchargées — **non versionnées** |
| `data/processed/` | Données dérivées, versionnées (comptages, fichiers légers pour l'app) |
| `scripts/` | Scripts d'import et de traitement |
| `app/` | La web app (POC) |

## Premier package

**Arbres communs de Paris** — espèces choisies d'après le jeu de données « Les arbres » de Paris Open Data.
