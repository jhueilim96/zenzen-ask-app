import os
from typing import Any
from langchain.prompts import (
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
)
from langchain.tools import tool
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    AgentExecutor,
    initialize_agent,
    create_react_agent,
)
from langchain.callbacks import StdOutCallbackHandler
from langchain import hub

from app.utils.typesense_func import client
from app.models.search import TypesenseSearchResult


# @tool
# def anime_search_tool(input: str) -> dict[str, Any]:
#     """use this tools when you need to lookup information about anime. parameter are inputs and input_type. input should the name of the keyword to search, type should the input_type of the things"""
#     WEBPAGE_INDEX = os.environ.get("WEBPAGE_INDEX")
#     search_parameters = {
#         "q": input,
#         "query_by": "title",
#         "per_page": 2,
#     }
#     search_hits = client.collections[WEBPAGE_INDEX].documents.search(search_parameters)
#     entity_result = TypesenseSearchResult(**search_hits)
#     hits = entity_result.hits
#     return hits[0].document if hits else []


# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are an assistant to take care children below 12 years old. ')),
#     MessagesPlaceholder(variable_name='chat_history', optional=True),
#     HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['anime_title'], template='Tell me a story about a {anime_title}')),
#     MessagesPlaceholder(variable_name='agent_scratchpad')
# ])

# tools = [anime_search_tool]
# prompt = hub.pull("hwchase17/react")

# llm = ChatOpenAI(
#     openai_api_key=os.environ.get("OPENAI_API_KEY"),
#     temperature=0.3,
#     model_name="gpt-3.5-turbo",
#     max_tokens=50,
# )


# agent = create_react_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(
#     agent=agent, tools=tools, verbose=True, callbacks=[StdOutCallbackHandler()]
# )
