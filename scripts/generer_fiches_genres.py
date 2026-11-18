"""Génère le squelette des fiches genres d'un package à partir des données Paris Open Data.

Remplit uniquement ce que les données établissent (chiffres parisiens, espèces et leur ordre d'apprentissage).
Les critères de reconnaissance, sosies et anecdotes restent à rédiger à partir de sources botaniques.
Ne réécrit jamais une fiche existante.

Usage : python scripts/generer_fiches_genres.py [rarete]   (par défaut : commune)
"""
import re
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
PROC = RACINE / "data" / "processed"
GENRES = RACINE / "contenu" / "genres"

PART_MIN = 0.03        # une espèce est enseignée si elle pèse au moins 3 % du genre à Paris
NB_MAX_ESPECES = 6
NIVEAUX_ESPECES = [5, 7, 7, 9, 9, 9]   # niveau de recherche auquel chaque espèce (par rang) est enseignée
ESPECES_IGNOREES = {"sp.", "n. sp.", "?"}
# Le libellé du jeu de données est parfois celui d'une espèce ou d'un usage (« Noisetier de Byzance », « Pommier à fruits ») :
# on retient un nom de genre générique, à valider.
CORRECTIONS_NOMS = {
    "Erable": "Érable", "Fevier": "Févier", "Noisetier de Byzance": "Noisetier",
    "Pommier à fruits": "Pommier", "Poirier à fleurs": "Poirier", "Cerisier à fleurs": "Cerisier, prunier",
}


def kebab(texte: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", texte.lower()).strip("-")


def yaml_str(s) -> str:
    return '"' + str(s).replace('"', '\\"') + '"'


def fiche(g: pd.Series, especes: pd.DataFrame) -> str:
    nom = CORRECTIONS_NOMS.get(g.nom_fr, g.nom_fr)
    milieux = {m: int(g[f"n_{m}"]) for m in ["alignement", "jardin", "cimetiere", "equipement"] if f"n_{m}" in g}
    lignes = [
        f"id: {kebab(g.genre)}",
        f"nom_scientifique: {g.genre}",
        f"noms_vernaculaires: [{yaml_str(nom)}]",
        "famille: null              # à sourcer",
        "type: arbre",
        "statut: brouillon",
        "paris:                     # source : paris-opendata (data/processed/genres_arbres.csv)",
        f"  n_arbres: {int(g.n_total)}",
        f"  rang: {int(g.rang)}",
        f"  rarete: {g.rarete}",
        "  milieux: {" + ", ".join(f"{k}: {v}" for k, v in milieux.items()) + "}",
        "especes:                   # ordre d'apprentissage = fréquence à Paris",
    ]
    if especes.empty:
        lignes[-1] = "especes: []  # aucune espèce ne dépasse le seuil : à décider"
    for i, e in enumerate(especes.itertuples()):
        nom_sci = f"{g.genre} {e.espece}"
        lignes += [
            f"  - id: {kebab(nom_sci)}",
            f"    nom_scientifique: {yaml_str(nom_sci)}",
            "    nom_vernaculaire: null   # à sourcer",
            f"    n_paris: {int(e.n_total)}",
            f"    part_du_genre: {e.part_genre:.2f}",
            f"    niveau: {NIVEAUX_ESPECES[i]}",
        ]
    lignes += [
        "reconnaissance:            # chaque critère : texte, sources, niveau",
        "  principal: []            # niveau 1",
        "  feuille: []",
        "  ecorce: []",
        "  silhouette: []",
        "  hiver: []",
        "  fleur: []",
        "  fruit: []",
        "sosies: []                 # niveau 3",
        "anecdotes: []",
        "photos: []",
        "sources:",
        "  - id: paris-opendata",
        "    titre: Ville de Paris — jeu de données « Les arbres »",
        "    url: https://opendata.paris.fr/explore/dataset/les-arbres/",
        "    licence: ODbL",
        "    usage_commercial: true",
        "    consulte_le: 2026-11-16",
    ]
    return "\n".join(lignes) + "\n"


def main() -> None:
    rarete = sys.argv[1] if len(sys.argv) > 1 else "commune"
    genres = pd.read_csv(PROC / "genres_arbres.csv")
    taxons = pd.read_csv(PROC / "taxons_arbres.csv")
    taxons["espece"] = taxons["espece"].fillna("sp.")
    # Les sous-espèces, variétés et formes sont regroupées sous l'espèce (ex. Pinus nigra subsp. laricio → Pinus nigra)
    taxons["espece"] = taxons["espece"].str.replace(r"\s+(subsp\.|var\.|f\.).*$", "", regex=True)
    taxons = taxons.groupby(["genre", "espece"], as_index=False)["n_total"].sum()
    GENRES.mkdir(parents=True, exist_ok=True)
    ids = []
    for g in genres[genres["rarete"] == rarete].itertuples(index=False):
        g = pd.Series(g._asdict())
        t = taxons[(taxons["genre"] == g.genre) & ~taxons["espece"].isin(ESPECES_IGNOREES)].copy()
        t["part_genre"] = t["n_total"] / g.n_total
        t = t[t["part_genre"] >= PART_MIN].sort_values("n_total", ascending=False).head(NB_MAX_ESPECES)
        chemin = GENRES / f"{kebab(g.genre)}.yaml"
        ids.append(kebab(g.genre))
        if chemin.exists():
            print(f"existe déjà : {chemin.name}")
            continue
        chemin.write_text(fiche(g, t), encoding="utf-8")
        print(f"créée : {chemin.name} ({len(t)} espèces)")
    print("genres :", ", ".join(ids))


if __name__ == "__main__":
    main()
