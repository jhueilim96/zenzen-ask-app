import streamlit as st
import httpx
from pydantic import BaseModel
from typing import Any
from jinja2 import Template

# Model
# class Hit(BaseModel):
#     document: dict[str, Any]
#     text_match: int
#     highlights: list[dict[str, Any]]

# class TypesenseSearchResult(BaseModel):
#     found: int
#     hits: list[Hit]
#     page: int
#     search_time_ms: int

# class TypesenseMultiSearchResult(BaseModel):
#     results: list[TypesenseSearchResult]

class KnowledgePanel(BaseModel):
    name: str
    type: list[str]
    description: str = None
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

# Function
@st.cache_data
def search(query:str)->SearchResponseConsolidated:
    URL = 'http://127.0.0.1:8000/search'
    r = httpx.get(URL, params={'q':query})
    multi_search_result = SearchResponseConsolidated.model_validate(r.json())
    return multi_search_result


def create_serp(serp_data:list[SearchResultRow], container):
    for search_result_row in serp_data:
        container.markdown(f"""##### [{search_result_row.title}]({search_result_row.url})
{search_result_row.url}

{search_result_row.description}
""")


def create_knowledge_panel(entity:KnowledgePanel, container):
    kp_template = Template("""
# {{entity.name}}
**{{entity.type[0]}}**
## About
{{entity.description}}


[Source]({{entity.source}})

{% for key, val in entity.properties.items() %}
*{{key}}*: {{val}}
{% endfor %}
""")

    if entity.image_url:
        container.image(entity.image_url)
    container.markdown(kp_template.render({'entity':entity.model_dump()}), unsafe_allow_html=True)


# Main
st.title('Zenzen')
query = st.text_input("Search something", value="naruto movie")

serp_col, kp_col = st.columns([1, 1])

# Search Result Page Processing
search_response = search(query)
webpage_result = search_response.serp
kp_data = search_response.kp

# search_result_list = [
#     SearchResultRow(
#         title= hit.document.get('title'),
#         url=hit.document.get('url'),
#     )
#     for hit in webpage_result.hits
# ]

# Knowledge Panel Process
# kg_entity = kp_result.hits[0].document.copy()
# kp_data = KnowledgePanel(
#     name = kg_entity.pop('name') ,
#     type = kg_entity.pop('type') ,
#     description = kg_entity.pop('description')[:300]+'...' if 'description' in kg_entity.keys() else '',
#     image_url =  kg_entity.pop('image_url') if 'image_url' in kg_entity.keys() else '',
#     source = kg_entity.pop('url') if 'url' in kg_entity.keys() else '',
#     properties =  kg_entity
# )

# Search Result View
serp_col.text(f"{webpage_result.found} results is found in {webpage_result.search_time_ms} millisecons")
create_serp(webpage_result.result, serp_col)

# Knowledge Panel View
kp_col.text("Knowledge Panel")
create_knowledge_panel(kp_data, kp_col)
