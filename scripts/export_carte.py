"""Export compact des arbres pour la carte d'exploration (app/carte/).

Entrée  : data/processed/arbres_points.csv, data/processed/taxons_arbres.csv, data/processed/genres_arbres.csv
Sortie  : app/carte/arbres.json — non versionné (régénérable)

Coordonnées encodées en entiers : x = (lon - 2.2) × 1e5, y = (lat - 48.8) × 1e5 (≈ 1 m de précision).
Usage : python scripts/export_carte.py
"""
import json
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
PROC = RACINE / "data" / "processed"
SORTIE = RACINE / "app" / "carte" / "arbres.json"
LON0, LAT0, ECHELLE = 2.2, 48.8, 1e5


def main() -> None:
    pts = pd.read_csv(PROC / "arbres_points.csv", dtype={"id": str})
    taxons = pd.read_csv(PROC / "taxons_arbres.csv")
    genres = pd.read_csv(PROC / "genres_arbres.csv")

    genres = genres.fillna({"nom_fr": ""}).reset_index(drop=True)
    idx_genre = {g: i for i, g in enumerate(genres["genre"])}
    taxons = taxons.fillna({"nom_fr": "", "espece": "sp."}).reset_index(drop=True)
    taxons["cle"] = taxons["genre"] + " " + taxons["espece"]
    idx_taxon = {k: i for i, k in enumerate(taxons["cle"])}

    pts["cle"] = pts["genre"] + " " + pts["espece"].fillna("sp.")
    pts = pts[pts["cle"].isin(idx_taxon)]

    data = {
        "origine": [LON0, LAT0, ECHELLE],
        "genres": [
            [r.genre, r.nom_fr, int(r.n_total), r.rarete, int(r.rang)] for r in genres.itertuples()
        ],
        "taxons": [
            [idx_genre[r.genre], r.espece, r.nom_fr, int(r.n_total), r.rarete] for r in taxons.itertuples()
        ],
        "x": ((pts["lon"] - LON0) * ECHELLE).round().astype(int).tolist(),
        "y": ((pts["lat"] - LAT0) * ECHELLE).round().astype(int).tolist(),
        "t": pts["cle"].map(idx_taxon).astype(int).tolist(),
    }
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(pts)} points → {SORTIE} ({SORTIE.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
