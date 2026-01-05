from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.state import CompiledStateGraph
from pydantic import Field
from pydantic.dataclasses import dataclass

from paperboy.agents.tools.rss_fetcher import fetch_rss
from paperboy.config import MODEL, NEWS_AGENT_FETCHER_PROMPT


def get_agent() -> CompiledStateGraph:
    model = ChatGoogleGenerativeAI(
        model=MODEL,
    )

    # TODO: Define tools for the news fetcher agents
    agent = create_agent(
        model=model,
        tools=[fetch_rss],
        system_prompt=NEWS_AGENT_FETCHER_PROMPT,
        response_format=ToolStrategy(Response),
        name="news_fetcher_agent",
    )

    return agent

@dataclass
class Response:
    title: str = Field(description="The title of the news article")
    url: str = Field(description="The URL of the news article")
    summary: str = Field(description="A brief summary of the news article")
