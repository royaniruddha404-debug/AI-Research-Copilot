from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(query, max_results=5):

    try:

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )

        return response["results"]

    except Exception as e:

        print(f"Web Search Error: {e}")

        return []


def format_web_results(results):

    formatted_results = []

    for result in results:

        content = result.get("content", "")[:1000]

        formatted_results.append(
            f"""
Title: {result.get('title', '')}

Content:
{content}

Source:
{result.get('url', '')}
"""
        )

    return "\n\n".join(formatted_results)