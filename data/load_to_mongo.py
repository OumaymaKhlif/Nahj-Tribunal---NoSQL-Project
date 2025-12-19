# load_to_mongo.py
"""
Importer un JSONL dans MongoDB SANS AUCUNE opération de nettoyage.
Toutes les transformations doivent déjà être faites dans clean_crimes.py.
Le script :
- lit les lignes JSONL,
- crée un champ geo si latitude/longitude existent,
- crée seulement les indexes utiles,
- insère dans MongoDB par batch.
"""
# python load_to_mongo.py --jsonl cleaned_crimes.jsonl --mongo "mongodb://localhost:27017" --db city_safety --coll crimes


import json
import argparse
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import BulkWriteError
from tqdm import tqdm

DEFAULT_BATCH_SIZE = 1000


# -------------------------------------------------
# Connexion MongoDB
# -------------------------------------------------
def connect_mongo(uri: str, db_name: str):
    client = MongoClient(uri)
    return client[db_name]


# -------------------------------------------------
# Indexes utiles pour visualisation / analytics
# -------------------------------------------------
def create_indexes(coll):
    print("🔧 Création des indexes...")

    try:
        coll.create_index([("case_number", ASCENDING)], background=True)
    except: pass

    try:
        coll.create_index([("primary_type", ASCENDING)], background=True)
    except: pass

    try:
        coll.create_index([("date", ASCENDING)], background=True)
    except: pass

    try:
        coll.create_index([("description", TEXT)], default_language="english")
    except: pass

    try:
        coll.create_index([("geo", "2dsphere")], background=True)
    except: pass

    try:
        coll.create_index([("risk_level", ASCENDING)], background=True)
        coll.create_index([("severity", ASCENDING)], background=True)
    except: pass

    print("✔ Indexes OK.")


# -------------------------------------------------
# Construire geo si possible (pas un nettoyage)
# -------------------------------------------------
def build_geo_field(doc: dict):
    lat = doc.get("latitude") or doc.get("Latitude")
    lon = doc.get("longitude") or doc.get("Longitude")

    try:
        if lat not in (None, "", 0) and lon not in (None, "", 0):
            lat = float(lat)
            lon = float(lon)

            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return {"type": "Point", "coordinates": [lon, lat]}
    except:
        pass

    # Si un champ "location" existe déjà (dict ou GeoJSON), on le laisse tel quel
    if isinstance(doc.get("location"), dict):
        loc = doc["location"]
        if "lat" in loc and "lon" in loc:
            try:
                return {"type": "Point", "coordinates": [float(loc["lon"]), float(loc["lat"])]}
            except:
                pass

    return None


# -------------------------------------------------
# Insertion JSONL → MongoDB
# -------------------------------------------------
def insert_jsonl(jsonl_path, mongo_uri="mongodb://localhost:27017",
                 db_name="city_safety", coll_name="crimes",
                 batch_size=DEFAULT_BATCH_SIZE):

    db = connect_mongo(mongo_uri, db_name)
    coll = db[coll_name]

    print(f"📥 Importation : {jsonl_path} → {db_name}.{coll_name}")
    create_indexes(coll)

    batch = []
    total = 0
    skipped = 0

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Lecture JSONL"):
            try:
                doc = json.loads(line)
            except:
                skipped += 1
                continue

            # Ajouter geo si possible (ce n’est PAS du cleaning)
            geo = build_geo_field(doc)
            if geo:
                doc["geo"] = geo

            batch.append(doc)

            if len(batch) >= batch_size:
                try:
                    coll.insert_many(batch, ordered=False)
                    total += len(batch)
                except BulkWriteError as e:
                    inserted = len(batch) - len(e.details.get("writeErrors", []))
                    total += max(0, inserted)
                    print(f"⚠ Erreurs batch ignorées ({len(e.details.get('writeErrors', []))}).")
                batch = []

        # Insérer dernier batch
        if batch:
            try:
                coll.insert_many(batch, ordered=False)
                total += len(batch)
            except BulkWriteError as e:
                inserted = len(batch) - len(e.details.get("writeErrors", []))
                total += max(0, inserted)
                print(f"⚠ Erreurs batch final ignorées.")

    print(f"✔ Import terminé. Total inséré ≈ {total}. Lignes invalides : {skipped}")


# -------------------------------------------------
# CLI
# -------------------------------------------------
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Importer un JSONL dans MongoDB (sans cleaning)")
    p.add_argument("--jsonl", required=True, help="Chemin du JSONL propre")
    p.add_argument("--mongo", default="mongodb://localhost:27017")
    p.add_argument("--db", default="city_safety")
    p.add_argument("--coll", default="crimes")
    p.add_argument("--batch", type=int, default=DEFAULT_BATCH_SIZE)
    args = p.parse_args()

    insert_jsonl(
        jsonl_path=args.jsonl,
        mongo_uri=args.mongo,
        db_name=args.db,
        coll_name=args.coll,
        batch_size=args.batch
    )
