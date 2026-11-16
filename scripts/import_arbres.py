"""Import et analyse du jeu « Les arbres » (Paris Open Data).

Entrée  : data/raw/les-arbres.csv (export CSV, séparateur « ; »)
Sorties : data/processed/taxons_arbres.csv   — comptage par espèce (genre + espèce)
          data/processed/genres_arbres.csv   — comptage par genre
          data/processed/arbres_points.csv   — fichier léger (id, genre, espèce, lat, lon, domanialité) — non versionné

Usage : python scripts/import_arbres.py
"""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
BRUT = RACINE / "data" / "raw" / "les-arbres.csv"
SORTIE = RACINE / "data" / "processed"

# Seuils de rareté, sur la part cumulée des arbres (espèces triées de la plus à la moins fréquente).
# Une espèce est « commune » si elle fait partie des espèces qui couvrent ensemble les premiers 80 % des arbres, etc.
SEUILS_RARETE = [
    (0.80, "commune"),
    (0.95, "peu commune"),
    (0.99, "rare"),
    (1.00, "tres rare"),
]

# Regroupement des domanialités en milieux lisibles
MILIEUX = {
    "Alignement": "alignement",
    "PERIPHERIQUE": "alignement",
    "Jardin": "jardin",
    "CIMETIERE": "cimetiere",
}  # le reste (écoles, crèches, équipements sportifs…) → « equipement »

INTRA_MUROS = "PARIS "  # préfixe des arrondissements ; le reste = bois et cimetières extra-muros


def charger() -> pd.DataFrame:
    df = pd.read_csv(BRUT, sep=";", dtype=str, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={
        "IDBASE": "id", "DOMANIALITE": "domanialite", "ARRONDISSEMENT": "arrondissement",
        "LIBELLE FRANCAIS": "nom_fr", "GENRE": "genre", "ESPECE": "espece",
        "VARIETE OUCULTIVAR": "cultivar", "STADE DE DEVELOPPEMENT": "stade",
        "REMARQUABLE": "remarquable",
    })
    df = df[df["genre"].notna() & (df["genre"] != "Non spécifié")].copy()
    df["espece"] = df["espece"].fillna("sp.")
    df["taxon"] = df["genre"] + " " + df["espece"]
    df["milieu"] = df["domanialite"].map(MILIEUX).fillna("equipement")
    df["intra_muros"] = df["arrondissement"].fillna("").str.startswith(INTRA_MUROS)
    latlon = df["geo_point_2d"].str.split(",", expand=True)
    df["lat"] = pd.to_numeric(latlon[0], errors="coerce").round(6)
    df["lon"] = pd.to_numeric(latlon[1], errors="coerce").round(6)
    return df


def rarete(part_cumulee_avant: float) -> str:
    for seuil, nom in SEUILS_RARETE:
        if part_cumulee_avant < seuil:
            return nom
    return SEUILS_RARETE[-1][1]


def compter(df: pd.DataFrame, cle: list[str]) -> pd.DataFrame:
    t = df.groupby(cle).agg(
        nom_fr=("nom_fr", lambda s: s.mode().iat[0] if s.notna().any() else ""),
        n_total=("id", "size"),
        n_intra_muros=("intra_muros", "sum"),
    )
    par_milieu = pd.crosstab([df[c] for c in cle], df["milieu"]).add_prefix("n_")
    t = t.join(par_milieu).fillna(0)
    t = t.sort_values("n_total", ascending=False).reset_index()
    total = t["n_total"].sum()
    t["part"] = (t["n_total"] / total).round(5)
    t["part_cumulee"] = t["part"].cumsum().round(5)
    t["rang"] = range(1, len(t) + 1)
    t["rarete"] = (t["part_cumulee"] - t["part"]).apply(rarete)
    entiers = [c for c in t.columns if c.startswith("n_")]
    t[entiers] = t[entiers].astype(int)
    return t


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    df = charger()
    compter(df, ["genre", "espece"]).to_csv(SORTIE / "taxons_arbres.csv", index=False)
    compter(df, ["genre"]).to_csv(SORTIE / "genres_arbres.csv", index=False)
    df[["id", "genre", "espece", "nom_fr", "milieu", "lat", "lon"]].dropna(subset=["lat", "lon"]).to_csv(
        SORTIE / "arbres_points.csv", index=False
    )
    print(f"{len(df)} arbres, {df['taxon'].nunique()} taxons, {df['genre'].nunique()} genres")


if __name__ == "__main__":
    main()
