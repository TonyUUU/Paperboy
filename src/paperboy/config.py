import logging
import os

from dotenv import load_dotenv


load_dotenv()

MODEL = os.getenv("MODEL")

# TODO: Define the prompt for the news fetcher agents
NEWS_AGENT_FETCHER_PROMPT = """
You are a news fetching agents. Your task is to get me one latest news article based on my query.
"""

NOTION_TOKEN = os.getenv("NOTION_TOKEN")

logging.basicConfig(level=logging.INFO)
