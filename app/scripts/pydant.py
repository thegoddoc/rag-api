from pydantic import BaseModel
from typing import Literal

class QueryRequest(BaseModel):
    query: str
    k: int = 4

class QueryMode(BaseModel):
    moode : Literal["retrive", "rerank", "report"]
    