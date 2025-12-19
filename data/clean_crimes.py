# clean_and_prepare.py
"""
Pipeline de nettoyage professionnel pour le dataset crimes enrichi.
Version mise à jour :
- Suppression de colonnes inutiles
- victim_type_breakdown converti en objet JSON
"""

# python clean_crimes.py --csv C:\path\to\Crimes.csv --out cleaned_crimes.jsonl
# -------------------------------------------------------

import pandas as pd
import numpy as np
import json
from dateutil import parser
from tqdm import tqdm
import argparse

# -------------------------------------------------------
# 1. Parsing robuste des dates
# -------------------------------------------------------
def parse_date_safe(value):
    if pd.isna(value):
        return pd.NaT
    try:
        return pd.to_datetime(value, utc=True)
    except Exception:
        try:
            return pd.to_datetime(parser.parse(value), utc=True)
        except Exception:
            return pd.NaT


# -------------------------------------------------------
# 2. Nettoyage d’un chunk
# -------------------------------------------------------
def clean_chunk(df):

    # Toutes les colonnes enrichies possibles
    expected_cols = df.columns.tolist()
    df = df.copy()

    # -------------------------------------------------------
    # 1) Normalisation des noms utiles
    # -------------------------------------------------------
    rename_map = {
        "ID": "id",
        "Case Number": "case_number",
        "Date": "date",
        "Block": "block",
        "Primary Type": "primary_type",
        "Primary Type_norm": "primary_type_norm",
        "Description": "description",
        "Location Description": "location_description",
        "Community Area": "community_area",
        "X Coordinate": "x_coord",
        "Y Coordinate": "y_coord",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "District": "district",
        "Ward": "ward",
        "Year": "year",
    }
    df.rename(columns=rename_map, inplace=True)

    # -------------------------------------------------------
    # 2) Nettoyage texte
    # -------------------------------------------------------
    text_cols = [
        "primary_type", "primary_type_norm", "description",
        "location_description", "block", "case_number", "IUCR",
        "FBI Code", "period_of_day", "risk_level"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .replace({"nan": None, "": None})
            )

    if "primary_type" in df.columns:
        df["primary_type"] = df["primary_type"].str.lower()

    # -------------------------------------------------------
    # 3) Parsing des dates
    # -------------------------------------------------------
    if "date" in df.columns:
        df["date"] = df["date"].apply(parse_date_safe)

    # -------------------------------------------------------
    # 4) Convertir victm_type_breakdown en JSON
    # -------------------------------------------------------
    if ("num_physical_victims" in df.columns and
        "num_psychological_victims" in df.columns and
        "num_property_victims" in df.columns):

        df["victim_type_breakdown"] = df.apply(
            lambda r: {
                "physical": int(r["num_physical_victims"]) if pd.notna(r["num_physical_victims"]) else 0,
                "psychological": int(r["num_psychological_victims"]) if pd.notna(r["num_psychological_victims"]) else 0,
                "property": int(r["num_property_victims"]) if pd.notna(r["num_property_victims"]) else 0,
            },
            axis=1
        )


    # -------------------------------------------------------
    # 6) Nettoyage numérique
    # -------------------------------------------------------
    numeric_cols = [
        "latitude", "longitude", "x_coord", "y_coord", "district",
        "year", "severity", "victims_count", "risk_location_score"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -------------------------------------------------------
    # 7) Nettoyage coordonnées invalides
    # -------------------------------------------------------
    if "latitude" in df.columns:
        df.loc[(df["latitude"] > 90) | (df["latitude"] < -90), "latitude"] = np.nan
    if "longitude" in df.columns:
        df.loc[(df["longitude"] > 180) | (df["longitude"] < -180), "longitude"] = np.nan

    # -------------------------------------------------------
    # 8) Ajouter champ géospatial
    # -------------------------------------------------------
    df["location"] = df.apply(
        lambda r: {"lat": r["latitude"], "lon": r["longitude"]}
        if pd.notna(r.get("latitude")) and pd.notna(r.get("longitude"))
        else None,
        axis=1
    )

    # -------------------------------------------------------
    # 9) Supprimer les lignes vides ou pleines de zéros
    # -------------------------------------------------------
    df = df[df.notna().sum(axis=1) >= 6]       # Trop de NaN
    df = df[(df == 0).sum(axis=1) < 8]         # Trop de zéros

    # -------------------------------------------------------
    # 10) Supprimer les doublons
    # -------------------------------------------------------
    if "id" in df.columns:
        df.drop_duplicates(subset="id", inplace=True)

# -------------------------------------------------------
    # 5) Suppression des colonnes obsolètes
# -------------------------------------------------------
    cols_to_drop = [
        "Arrest_bool", "Domestic_bool",
        "District_int", "District_group", "district_risk_norm",
        "primary_type_norm",
        "Beat", "ward","Location", "longitude", "latitude",
        "domestic_increase", "arrest_decrease",
        "num_physical_victims", "num_psychological_victims", "num_property_victims"
    ]

    df.drop(columns=[c for c in cols_to_drop if c in df.columns],
            inplace=True, errors="ignore")

    return df

# -------------------------------------------------------
# 11. Fonction principale
# -------------------------------------------------------
def main(csv_path, out_path, chunksize=20000):
    total = 0
    with open(out_path, "w", encoding="utf-8") as writer:
        for chunk in tqdm(pd.read_csv(csv_path, chunksize=chunksize, dtype=str, low_memory=False)):
            cleaned = clean_chunk(chunk)

            for record in cleaned.to_dict(orient="records"):
                if "date" in record and not isinstance(record["date"], str):
                    try:
                        record["date"] = record["date"].isoformat()
                    except:
                        record["date"] = None
                writer.write(json.dumps(record, ensure_ascii=False) + "\n")
                total += 1

    print(f"✔ Nettoyage terminé — {total} documents enregistrés dans {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default="cleaned_crimes.jsonl")
    parser.add_argument("--chunksize", type=int, default=20000)
    args = parser.parse_args()
    main(args.csv, args.out, args.chunksize)
