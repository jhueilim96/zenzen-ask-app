from fastapi import FastAPI
import typesense
import os
from dotenv import load_dotenv
import spacy

from app.models.model import (
    SearchResponseConsolidated,
    TypesenseSearchResult,
    SearchResultRow,
    SearchResultPage,
    KnowledgePanel,
)
from app.agents import (
    agent_executor
)

load_dotenv()
TYPESENSE_KEY = os.environ["typesense_key"]
# nlp = spacy.load("en_core_web_sm")

client = typesense.Client(
    {
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "api_key": TYPESENSE_KEY,
        "connection_timeout_seconds": 2,
    }
)
WEBPAGE_INDEX = os.environ["WEBPAGE_INDEX"]
ENTITY_INDEX = os.environ["ENTITY_INDEX"]

app = FastAPI()


@app.get("/search")
async def search(
    q: str,
    limit: int = 10,
) -> SearchResponseConsolidated:
    doc = nlp(q)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    filtered_string = " ".join(filtered_tokens)

    search_requests = {
        "searches": [
            {
                "collection": WEBPAGE_INDEX,
                "q": q,
                "query_by": "title, url, aka, entity_type",
            },
        ]
    }

    search_hits = client.collections[WEBPAGE_INDEX].documents.search(search_requests)
    webpage_result = TypesenseSearchResult(**search_hits)

    # Webpage Search Result Processing
    search_result_list = [
        SearchResultRow(
            title=hit.document.get("title"),
            url=hit.document.get("url"),
        )
        for hit in webpage_result.hits
    ]
    serp = SearchResultPage(
        result=search_result_list,
        found=webpage_result.found,
        page=webpage_result.page,
        search_time_ms=webpage_result.search_time_ms,
    )
    return SearchResponseConsolidated(serp=serp)


@app.get("/entity")
async def search_entity(
    q: str,
    limit: int = 5,
):
    query_entity = q  # filtered_string
    search_parameters = {
        "q": query_entity,
        "query_by": "title",
        # 'sort_by'   : 'num_employees:desc'
    }
    search_hits = client.collections[ENTITY_INDEX].documents.search(search_parameters)
    entity_result = TypesenseSearchResult(**search_hits)
    return entity_result.hits[0]


@app.post("/chat")
def chat(query:str):
    res = agent_executor.invoke({'input':query})
    return res

# asyncio.run(search('Naruto movie'))
