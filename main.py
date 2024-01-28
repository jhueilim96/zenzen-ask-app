from fastapi import FastAPI
import typesense
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any


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


load_dotenv()
TYPESENSE_KEY = os.environ['typesense_key']

client = typesense.Client({
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'api_key': TYPESENSE_KEY,
  'connection_timeout_seconds': 2
})


app = FastAPI()


@app.get("/search")
async def search(q:str, limit:int=10, ):
    search_requests = {
        'searches': [
        {
            'collection': 'webpage',
            'q': q,
            'query_by': 'title, url, aka',
        },
        {
            'collection': 'entity',
            'q': q,
            'query_by': 'name, type, description',
        }
        ]
    }

    # Search parameters that are common to all searches go here
    common_search_params =  {
        # 'query_by': 'name',
    }

    search_hits = client.multi_search.perform(search_requests, common_search_params)
    return TypesenseMultiSearchResult.model_validate(search_hits)
