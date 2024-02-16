from typing import Any
import os

from langchain.prompts import SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, PromptTemplate, ChatPromptTemplate
from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI
from langchain.agents  import create_openai_functions_agent, AgentExecutor, initialize_agent
from langchain.tools.retriever import create_retriever_tool
from langchain.callbacks import StdOutCallbackHandler

