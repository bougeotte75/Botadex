"""Vérifie la cohérence du contenu : fiches jeu, dossiers de recherche, photos, packages.

Erreurs (bloquantes) :
- fiche.yaml non conforme à schema/genre.schema.json
- note citée par la fiche absente du dossier de recherche, écartée, ou sans source
- photo citée absente de photos.md, écartée, sans licence, ou non commerciale dans un package payant
- identifiant de note ou de photo en double ; préfixe utilisé par deux genres
- package qui liste un genre sans dossier

Avertissements : notes citées « à vérifier » ou « à trier », statistiques de tri.

Usage : python scripts/verifier_contenu.py [genre ...]
"""
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

RACINE = Path(__file__).resolve().parents[1]
GENRES = RACINE / "contenu" / "genres"
PACKAGES = RACINE / "contenu" / "packages"
STATUTS = {"à trier", "retenu", "écarté", "à vérifier"}

RE_NOTE = re.compile(r"^### ([A-Z]{3}-\d{3}) · (.+?)\s*$")
RE_SOURCE = re.compile(r"^- Source : \[.+?\]\(https?://\S+?\)")


def lire_notes(chemin: Path, erreurs: list) -> dict:
    """Retourne {id: {"statut", "source": bool, "rubrique"}}."""
    notes, courante, rubrique, dans_code = {}, None, None, False
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("```"):
            dans_code = not dans_code
            continue
        if dans_code:
            continue
        if ligne.startswith("## "):
            rubrique, courante = ligne[3:].strip(), None
            continue
        m = RE_NOTE.match(ligne)
        if m:
            nid, statut = m.groups()
            if nid in notes:
                erreurs.append(f"{chemin.parent.name}: note {nid} en double")
            if statut not in STATUTS:
                erreurs.append(f"{chemin.parent.name}: note {nid} — statut inconnu « {statut} »")
            notes[nid] = {"statut": statut, "source": False, "rubrique": rubrique}
            courante = nid
            continue
        if courante and RE_SOURCE.match(ligne):
            notes[courante]["source"] = True
    return notes


def lire_photos(chemin: Path, erreurs: list) -> dict:
    photos = {}
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) != 10 or not re.match(r"^[A-Z]{3}-P\d{3}$", cellules[0]):
            continue
        pid = cellules[0]
        if pid in photos:
            erreurs.append(f"{chemin.parent.name}: photo {pid} en double")
        photos[pid] = {"licence": cellules[7], "commercial": cellules[8].lower(), "statut": cellules[9]}
    return photos


def notes_citees(fiche: dict) -> list:
    citees = []

    def parcourir(objet):
        if isinstance(objet, dict):
            for cle, val in objet.items():
                if cle == "notes" and isinstance(val, list):
                    citees.extend(val)
                else:
                    parcourir(val)
        elif isinstance(objet, list):
            for val in objet:
                parcourir(val)

    parcourir(fiche)
    return citees


def main() -> int:
    erreurs, avertissements = [], []
    validateur = Draft202012Validator(json.loads((RACINE / "schema" / "genre.schema.json").read_text(encoding="utf-8")))

    payants = set()
    for p in PACKAGES.glob("*/package.yaml"):
        pkg = yaml.safe_load(p.read_text(encoding="utf-8"))
        for g in pkg.get("genres", []):
            if not (GENRES / g / "fiche.yaml").exists():
                erreurs.append(f"package {pkg['id']}: genre « {g} » sans dossier")
            if pkg.get("acces") == "payant":
                payants.add(g)

    demandes = set(sys.argv[1:])
    prefixes = {}
    for dossier in sorted(d for d in GENRES.iterdir() if d.is_dir() and not d.name.startswith("_")):
        if demandes and dossier.name not in demandes:
            continue
        nom = dossier.name
        fiche = yaml.safe_load((dossier / "fiche.yaml").read_text(encoding="utf-8"))
        for e in validateur.iter_errors(fiche):
            erreurs.append(f"{nom}: fiche.yaml {'/'.join(map(str, e.path)) or '(racine)'} — {e.message}")
        prefixe = fiche.get("prefixe_notes", "")
        if prefixe in prefixes:
            erreurs.append(f"{nom}: préfixe {prefixe} déjà utilisé par {prefixes[prefixe]}")
        prefixes[prefixe] = nom

        notes = lire_notes(dossier / "recherche.md", erreurs)
        for nid in notes:
            if not nid.startswith(prefixe + "-"):
                erreurs.append(f"{nom}: note {nid} n'a pas le préfixe {prefixe}")
        for nid, n in notes.items():
            if not n["source"] and n["statut"] != "écarté":
                avertissements.append(f"{nom}: note {nid} sans ligne « - Source : [titre](url) »")
        for nid in notes_citees(fiche):
            n = notes.get(nid)
            if n is None:
                erreurs.append(f"{nom}: la fiche cite {nid}, absente du dossier de recherche")
            elif n["statut"] == "écarté":
                erreurs.append(f"{nom}: la fiche cite {nid}, note écartée")
            elif not n["source"]:
                erreurs.append(f"{nom}: la fiche cite {nid}, note sans source")
            elif n["statut"] != "retenu":
                avertissements.append(f"{nom}: la fiche cite {nid}, note « {n['statut']} »")

        photos = lire_photos(dossier / "photos.md", erreurs)
        for pid in fiche.get("photos") or []:
            p = photos.get(pid)
            if p is None:
                erreurs.append(f"{nom}: la fiche cite la photo {pid}, absente de photos.md")
            elif p["statut"] == "écarté":
                erreurs.append(f"{nom}: la fiche cite la photo {pid}, écartée")
            elif not p["licence"]:
                erreurs.append(f"{nom}: photo {pid} sans licence")
            elif nom in payants and p["commercial"] != "oui":
                erreurs.append(f"{nom}: photo {pid} non commerciale dans un package payant")

        compte = {s: sum(1 for n in notes.values() if n["statut"] == s) for s in STATUTS}
        print(f"{nom:<14} notes : {len(notes):>3}  (retenu {compte['retenu']}, à trier {compte['à trier']}, "
              f"à vérifier {compte['à vérifier']}, écarté {compte['écarté']})  ·  photos : {len(photos)}  ·  "
              f"citées par la fiche : {len(set(notes_citees(fiche)))}")

    for a in avertissements:
        print("  ⚠", a)
    for e in erreurs:
        print("  ✗", e)
    print(f"\n{len(erreurs)} erreur(s), {len(avertissements)} avertissement(s)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
