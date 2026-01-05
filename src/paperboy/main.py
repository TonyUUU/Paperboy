from paperboy.agents.news_fetcher import get_agent


def main():
    fetcher = get_agent()
    # Example usage of the agents
    response = fetcher.invoke(
        input={"messages": [{"role": "user", "content": "Fetch the latest news on AI advancements. Use these RSS feeds: https://news.ycombinator.com/rss"}]}
    )
    print(response['structured_response'])

if __name__ == "__main__":
    main()
