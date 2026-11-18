"""Génère le dossier de chaque genre d'un package : fiche jeu (fiche.yaml), dossier de recherche (recherche.md), photos (photos.md).

La fiche jeu ne contient que ce que les données établissent (chiffres parisiens, espèces et leur ordre d'apprentissage).
Les critères de reconnaissance, sosies et anecdotes restent à rédiger à partir de sources botaniques.
Ne réécrit jamais un fichier existant.

Usage : python scripts/generer_fiches_genres.py [rarete]   (par défaut : commune)
"""
import re
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
PROC = RACINE / "data" / "processed"
GENRES = RACINE / "contenu" / "genres"
MODELE = GENRES / "_modele"

PART_MIN = 0          # toutes les espèces du genre présentes à Paris (décision : pas de filtre par rareté)
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


def prefixe(genre: str) -> str:
    return genre[:3].upper()


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
        f"prefixe_notes: {prefixe(g.genre)}",
        "paris:                     # source : jeu « Les arbres », Ville de Paris (ODbL) — data/processed/genres_arbres.csv",
        f"  n_arbres: {int(g.n_total)}",
        f"  rang: {int(g.rang)}",
        f"  rarete: {g.rarete}",
        "  milieux: {" + ", ".join(f"{k}: {v}" for k, v in milieux.items()) + "}",
        "especes:                   # toutes les espèces présentes à Paris, par fréquence (ordre indicatif)",
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
        ]
    lignes += [
        "# Chaque affirmation : texte (nos mots), notes (ids du dossier de recherche), niveau (1 à 10). Ex. :",
        f"#   - texte: \"...\"\n#     notes: [{prefixe(g.genre)}-001]\n#     niveau: 1",
        "reconnaissance:",
        "  principal: []            # niveau 1",
        "  silhouette: []",
        "  feuille: []",
        "  ecorce: []",
        "  bourgeon: []",
        "  fleur: []",
        "  fruit: []",
        "sosies: []                 # niveau 2",
        "phenologie: {notes: [], feuillage: [], floraison: [], fructification: []}",
        "anecdotes: []",
        f"photos: []                 # ids de photos.md ({prefixe(g.genre)}-P001…)",
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
        t = t[t["part_genre"] >= PART_MIN].sort_values("n_total", ascending=False)
        dossier = GENRES / kebab(g.genre)
        dossier.mkdir(exist_ok=True)
        ids.append(kebab(g.genre))
        nom = CORRECTIONS_NOMS.get(g.nom_fr, g.nom_fr)
        fichiers = {"fiche.yaml": fiche(g, t)}
        for modele in ["recherche.md", "photos.md"]:
            fichiers[modele] = (MODELE / modele).read_text(encoding="utf-8").replace(
                "{NOM}", nom).replace("{GENRE}", g.genre).replace("{PREFIXE}", prefixe(g.genre))
        for nom_fichier, texte in fichiers.items():
            chemin = dossier / nom_fichier
            if chemin.exists():
                continue
            chemin.write_text(texte, encoding="utf-8")
        print(f"{dossier.name}/ ({len(t)} espèces, préfixe {prefixe(g.genre)})")
    prefixes = [i[:3].upper() for i in ids]
    assert len(set(prefixes)) == len(prefixes), f"préfixes en double : {prefixes}"
    print("genres :", ", ".join(ids))


if __name__ == "__main__":
    main()
