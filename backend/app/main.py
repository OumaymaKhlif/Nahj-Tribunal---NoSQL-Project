# main.py
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from es_client import get_es_client
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from datetime import datetime

def parse_date(d, start=True):
    if not d:
        return None
    dt = datetime.strptime(d, "%Y-%m-%d")
    if start:
        return dt.isoformat() + "Z"  # UTC début de journée
    else:
        dt = dt.replace(hour=23, minute=59, second=59)
        return dt.isoformat() + "Z"  # UTC fin de journée

# Connexion MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
mongo_db = mongo_client["city_safety"]
mongo_collection = mongo_db["crime"]


load_dotenv()
ES_INDEX = os.getenv("ES_INDEX", "crimes_index")

es = get_es_client()

app = FastAPI(title="CitySafety API")

# Allow local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility: convert severity numeric -> label
SEVERITY_LABEL = {
    5: "Very High",
    4: "High",
    3: "Medium",
    2: "Low",
    1: "Very Low"
}
def severity_label(v):
    try:
        return SEVERITY_LABEL.get(int(v), str(v))
    except:
        return v

@app.get("/")
def health():
    return {"ok": True}

@app.get("/api/count")
def count_index(index: str = ES_INDEX):
    if not es.indices.exists(index=index):
        raise HTTPException(status_code=404, detail="Index not found")
    c = es.count(index=index)
    return {"count": c.get("count", 0)}

@app.get("/api/crime/{doc_id}")
def get_crime(doc_id: str, index: str = ES_INDEX):
    try:
        res = es.get(index=index, id=doc_id)
        src = res.get("_source", {})
        # nicer severity label
        if "severity" in src:
            src["severity_label"] = severity_label(src["severity"])
        return {"id": res.get("_id"), "source": src}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/search")
def search(
    q: Optional[str] = Query(None, description="text search on primary_type/description"),
    primary_type: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
    size: int = 20,
    page: int = 0,
    index: str = ES_INDEX
):
    if not es.indices.exists(index=index):
        raise HTTPException(status_code=404, detail="Index not found")

    must = []

    # Nettoyage q
    if q:
        q_clean = q.strip()
        if q_clean:
            must.append({
                "multi_match": {
                    "query": q_clean,
                    "fields": ["primary_type^3", "description", "location_description"]
                }
            })

    # Filter primary_type
    if primary_type:
        pt_clean = primary_type.strip()
        if pt_clean:
            must.append({"term": {"primary_type.keyword": pt_clean}})

    # Filter district
    if district:
        try:
            dval = int(district)
            must.append({"term": {"district": dval}})
        except:
            pass

    # Filter date range
    # Filter date range
    # Dans ta fonction search()
    if date_from or date_to:
        range_q = {}
        if date_from:
            range_q["gte"] = parse_date(date_from, start=True)
        if date_to:
            range_q["lte"] = parse_date(date_to, start=False)
        must.append({"range": {"date": range_q}})

    body = {"query": {"bool": {"must": must}}} if must else {"query": {"match_all": {}}}
    body["size"] = size
    body["from"] = page * size

    res = es.search(index=index, body=body)
    hits = []
    for h in res["hits"]["hits"]:
        src = h["_source"]
        if "severity" in src:
            src["severity_label"] = severity_label(src["severity"])
        vt = src.get("victim_type_breakdown", {})
        if isinstance(vt, dict):
            chosen = None
            for k in ["physical", "psychological", "property"]:
                if vt.get(k) and int(vt.get(k)) > 0:
                    chosen = k
                    break
            src["victim_type_selected"] = chosen
        hits.append({"id": h["_id"], "score": h["_score"], "source": src})

    return {"total": res["hits"]["total"]["value"], "hits": hits}


@app.get("/api/aggregations/summary")
def summary(index: str = ES_INDEX):
    # some useful aggregates: incidents per hour, per type, arrests %
    if not es.indices.exists(index=index):
        raise HTTPException(status_code=404, detail="Index not found")
    body = {
        "size": 0,
        "aggs": {
            "by_hour": {"terms": {"field": "hour", "size": 24, "order": {"_key": "asc"}}},
            "by_type": {"terms": {"field": "primary_type", "size": 20}},
            "arrest_stats": {
                "terms": {"field": "Arrest"}
            }
        }
    }
    res = es.search(index=index, body=body)
    return res["aggregations"]

@app.get("/api/mongo_summary")
def mongo_summary():
    """Total de districts et types de crimes uniques depuis MongoDB"""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "uniqueTypes": {"$addToSet": "$primary_type"},
                "uniqueDistricts": {"$addToSet": "$district"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "totalTypes": {"$size": "$uniqueTypes"},
                "totalDistricts": {"$size": "$uniqueDistricts"}
            }
        }
    ]
    result = list(mongo_collection.aggregate(pipeline))
    if result:
        return result[0]
    else:
        return {"totalTypes": 0, "totalDistricts": 0}

