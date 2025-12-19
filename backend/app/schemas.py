# schemas.py
from pydantic import BaseModel
from typing import Optional, Dict

class CrimeResult(BaseModel):
    id: str
    source: Dict

class SearchResponse(BaseModel):
    total: int
    hits: list
