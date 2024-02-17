from app.core.config import settings
from app.models.search import TypesenseSearchResult
from app.utils.typesense_func import client
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.tools import BaseTool, tool
from serpapi import GoogleSearch
from typing import Any, Optional
import httpx
import os

unsplash_api_url = f"https://api.unsplash.com/search/photos?client_id={settings.UNSPLASH_API_KEY}&query="

@tool
def anime_search_tool(input: str) -> dict[str, Any]:
    """use this tools when you need to lookup information about anime. parameter are input. input should the name of the keyword to search"""
    WEBPAGE_INDEX = os.environ.get("WEBPAGE_INDEX")
    search_parameters = {
        "q": input,
        "query_by": "title",
        "per_page": 2,
    }
    search_hits = client.collections[WEBPAGE_INDEX].documents.search(search_parameters)
    entity_result = TypesenseSearchResult(**search_hits)
    hits = entity_result.hits
    return hits[0].document if hits else []


class GeneralKnowledgeTool(BaseTool):
    name = "Search"
    description = "useful for when you need to answer questions about current events"

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        chat = ChatOpenAI()
        response = await chat.agenerate([[HumanMessage(content=query)]])
        message = response.generations[0][0].text
        return message


class ImageSearchTool(BaseTool):
    name = "search_image"
    description = " Useful when asked to answer information about find images URL"
    return_direct = True

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        async with httpx.AsyncClient() as client:
            if settings.UNSPLASH_API_KEY == "":
                return "You need to set a UNSPLASH_API_KEY"

            unsplash_url = unsplash_api_url + query.lower()
            response = await client.get(unsplash_url)
            body = response.json()
            results = body["results"]
            images_urls = []
            for result in results:
                image_url = result["urls"]["small"]
                images_urls.append(image_url)
            image_list_string = "\n".join(
                [f"{i+1}. ![Image {i+1}]({url})" for i, url in enumerate(images_urls)]
            )
            return image_list_string


class YoutubeSearchTool(BaseTool):
    name = "search_videos"
    description = " Useful when asked to answer information about find videos"
    return_direct = True

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        async with httpx.AsyncClient() as client:
            if not settings.SERP_API_KEY or settings.SERP_API_KEY == "":
                return "You need to set a SERP_API_KEY"

            params = {
                "engine": "youtube",
                "search_query": query,
                "api_key": settings.SERP_API_KEY,
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            videos = results["video_results"]
            video_list_string = "\n".join(
                [
                    f"{i+1}. [{video['title']}]({video['link']})"
                    for i, video in enumerate(videos)
                ]
            )
            return video_list_string
