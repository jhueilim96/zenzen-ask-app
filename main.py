from fastapi import FastAPI
import typesense
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any
import asyncio


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
    kp: KnowledgePanel


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
async def search(q:str, limit:int=10, )->SearchResponseConsolidated:
    search_requests = {
        'searches': [
        {
            'collection': 'webpage',
            'q': q,
            'query_by': 'title, url, aka, entity_type',
        },
        {
            'collection': 'entity',
            'q': q,
            'query_by': 'name, type, synonyms',
        }
        ]
    }

    # Search parameters that are common to all searches go here
    common_search_params =  {
        # 'query_by': 'name',
    }

    search_hits = client.multi_search.perform(search_requests, common_search_params)
    multi_search_result = TypesenseMultiSearchResult.model_validate(search_hits)
    webpage_result, kp_result = multi_search_result.results[0], multi_search_result.results[1]

    # Webpage Search Result Processing
    search_result_list = [
        SearchResultRow(
            title= hit.document.get('title'),
            url=hit.document.get('url'),
        )
        for hit in webpage_result.hits
    ]
    serp = SearchResultPage(
        result=search_result_list,
        found=webpage_result.found,
        page=webpage_result.page,
        search_time_ms=webpage_result.search_time_ms,
    )

    # Knowledge Panel Result Processing
    kg_entity = kp_result.hits[0].document.copy()
    for highlight in  kp_result.hits[0].highlights:
        highlight_field = highlight['field']
        content_to_highlight = kg_entity[highlight_field]

        if isinstance(content_to_highlight, str):
            for token in highlight['matched_tokens']:
                content_to_highlight = content_to_highlight.replace(token, f"<mark>{token}</mark>", 1)
            kg_entity[highlight_field] = content_to_highlight
        elif isinstance(content_to_highlight, list):
            pass
        pass

    kp_name = kg_entity.pop('name')
    kp_type = kg_entity.pop('type')
    kp_description = kg_entity.pop('description') if 'description' in kg_entity.keys() else ''
    kp_description = kp_description[:500] + '...' if len(kp_description) > 500 else kp_description
    kp_image_url =  kg_entity.pop('image_url') if 'image_url' in kg_entity.keys() else ''
    kp_source = kg_entity.pop('url') if 'url' in kg_entity.keys() else ''
    kp_properties =  kg_entity
    kp_data = KnowledgePanel(
        name=kp_name
        , type=kp_type
        , description=kp_description
        , image_url=kp_image_url
        , source=kp_source
        , properties=kp_properties
    )
    return SearchResponseConsolidated(serp=serp, kp=kp_data)


# asyncio.run(search('Naruto movie'))