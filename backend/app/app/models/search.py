from pydantic import BaseModel
from typing import Any

## BE only Model

class Hit(BaseModel):
    document: dict[str, Any]
    text_match: int
    highlights: list[dict[str, Any]]

class TypesenseSearchResult(BaseModel):
    found: int
    hits: list[Hit]
    page: int
    search_time_ms: int

class TypesenseMultiSearchResult(BaseModel):
    results: list[TypesenseSearchResult]

## Shares Model with FE

class KnowledgePanel(BaseModel):
    name: str
    type: list[str]
    description: str = ''
    image_url: str = None
    source: str = None
    properties: dict[str, Any] = {}

class SearchResultRow(BaseModel):
    title: str
    url: str
    description: str = "Lorem Ipsum"

class SearchResultPage(BaseModel):
    result: list[SearchResultRow]
    found: int
    page: int
    search_time_ms: int

class SearchResponseConsolidated(BaseModel):
    serp: SearchResultPage
    kp: KnowledgePanel = None