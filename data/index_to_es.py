# index_to_es.py
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
import argparse
from tqdm import tqdm
import math

ES_INDEX = "crimes_index"

def connect_mongo(uri, db_name):
    client = MongoClient(uri)
    return client[db_name]

def connect_es(es_host):
    es = Elasticsearch(es_host, verify_certs=False, ssl_show_warn=False)
    if not es.ping():
        raise RuntimeError("Impossible de se connecter à Elasticsearch")
    return es

def create_es_index(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "case_number": {"type": "keyword"},
                "primary_type": {"type": "keyword"},
                "description": {"type": "text"},
                "location_description": {"type": "keyword"},
                "district": {"type": "keyword"},
                "community_area": {"type": "keyword"},
                "date": {"type": "date"},
                "year": {"type": "integer"},
                "geo": {"type": "geo_point"},

                # ➕ CHAMPS AJOUTÉS
                "id": {"type": "keyword"},
                "block": {"type": "keyword"},
                "IUCR": {"type": "keyword"},
                "Arrest": {"type": "keyword"},
                "Domestic": {"type": "keyword"},
                "fbi_code": {"type": "keyword"},
                "x_coord": {"type": "float"},
                "y_coord": {"type": "float"},
                "Updated_On": {"type": "text"},
                "Date_parsed": {"type": "text"},
                "hour": {"type": "keyword"},
                "period_of_day": {"type": "keyword"},
                "severity": {"type": "float"},
                "victims_count": {"type": "integer"},
                "severity_norm_row": {"type": "float"},
                "risk_raw": {"type": "float"},
                "risk_location_score": {"type": "float"},
                "risk_level": {"type": "keyword"},
                "victim_type_breakdown": {
                    "properties": {
                        "physical": {"type": "integer"},
                        "psychological": {"type": "integer"},
                        "property": {"type": "integer"}
                    }
                }
            }
        }
    }

    if es.indices.exists(index=index_name):
        print(f"Index {index_name} existe déjà.")
    else:
        es.indices.create(index=index_name, body=mapping)
        print(f"Index {index_name} créé.")

def mongo_to_es(mongo_uri, db_name, coll_name, es_host, index_name, batch_size=500):
    db = connect_mongo(mongo_uri, db_name)
    coll = db[coll_name]
    es = connect_es(es_host)
    create_es_index(es, index_name)

    total = coll.count_documents({})
    print(f"Documents à indexer : {total}")

    cursor = coll.find({}, no_cursor_timeout=True).batch_size(batch_size)
    actions = []
    count = 0

    for doc in tqdm(cursor, total=total):

        es_doc = {
            "_index": index_name,
            "_id": str(doc.get("_id")),
            "_source": {
                "id": doc.get("id"),
                "case_number": doc.get("case_number"),
                "date": doc.get("date"),
                "block": doc.get("block"),
                "IUCR": doc.get("IUCR"),
                "primary_type": doc.get("primary_type"),
                "description": doc.get("description"),
                "location_description": doc.get("location_description"),
                "Arrest": doc.get("Arrest"),
                "Domestic": doc.get("Domestic"),
                "district": doc.get("district"),
                "community_area": doc.get("community_area"),
                "fbi_code": doc.get("FBI Code"),
                "x_coord": doc.get("x_coord"),
                "y_coord": doc.get("y_coord"),
                "year": doc.get("year"),
                "Updated_On": doc.get("Updated On"),
                "Date_parsed": doc.get("Date_parsed"),
                "hour": doc.get("hour"),
                "period_of_day": doc.get("period_of_day"),
                "severity": doc.get("severity"),
                "victims_count": doc.get("victims_count"),
                "victim_type_breakdown": doc.get("victim_type_breakdown"),
                "severity_norm_row": float(doc.get("severity_norm_row") or 0),
                "risk_raw": float(doc.get("risk_raw") or 0),
                "risk_location_score": doc.get("risk_location_score"),
                "risk_level": doc.get("risk_level"),
            }
        }

        # ➕ Mapping GEO (inchangé)
        if doc.get("geo") and isinstance(doc["geo"], dict) and doc["geo"].get("coordinates"):
            lon, lat = doc["geo"]["coordinates"]
            es_doc["_source"]["geo"] = {"lat": lat, "lon": lon}

        elif doc.get("location") and isinstance(doc["location"], dict):
            lat = doc["location"].get("lat")
            lon = doc["location"].get("lon")
            if lat is not None and lon is not None:
                es_doc["_source"]["geo"] = {"lat": float(lat), "lon": float(lon)}

        actions.append(es_doc)

        if len(actions) >= batch_size:
            helpers.bulk(es, actions, raise_on_error=False)
            count += len(actions)
            actions = []

    if actions:
        helpers.bulk(es, actions, raise_on_error=False)
        count += len(actions)

    print(f"Total indexing done: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo", default="mongodb://localhost:27017")
    parser.add_argument("--db", default="city_safety")
    parser.add_argument("--coll", default="crime")
    parser.add_argument("--es", default="http://localhost:9200")
    parser.add_argument("--index", default=ES_INDEX)
    args = parser.parse_args()

    mongo_to_es(args.mongo, args.db, args.coll, args.es, args.index)
