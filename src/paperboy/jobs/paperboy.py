import logging
from math import log

from notion_client import APIResponseError, Client
from paperboy.agents import news_fetcher
from paperboy.agents.news_fetcher import get_agent
from paperboy.config import NOTION_TOKEN


def run():
    # Prepare the agent
    logging.info("Starting Paperboy ...")
    
    fetcher = get_agent()
    # TODO: Once feedback work is done, add agent feedback
    
    logging.info(f"{fetcher.name} agent loaded")

    # Query news
    logging.info("fetching news ...")

    message = {"messages": [{"role": "user", "content": "Fetch the latest news on AI advancements. Use these RSS feeds: https://news.ycombinator.com/rss"}]}
    response = fetcher.invoke(message)

    # TODO: Prepared newspaper based on response
    newspaper: list[news_fetcher.Response] = [response["structured_response"]]

    # Send results
    send_report()

def send_report():
    logging.info("Sending report to Notion ...")
    notion = Client(auth=NOTION_TOKEN)
    logging.info("Notion client initialized.")

    page = {
        "parent": {"page_id": "2e02fdc5-c0a0-80d4-871d-c71fd0678677"},
        "properties": {
            "title": [
                {
                    "text": {
                        "content": "Daily AI News Report2"
                    }
                }
            ]
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Here is the summary of today's AI news..."
                            }
                        }
                    ]
                }
            }
        ]
    }

    try:
        response = notion.pages.create(**page)
        logging.info("Notion page created successfully.")
    except APIResponseError as error:
        logging.error(f"An error occurred while creating the Notion page: {error}")


if __name__ == "__main__":
    run()
