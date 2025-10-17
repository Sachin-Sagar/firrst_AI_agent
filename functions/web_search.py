# functions/web_search.py

import os
import json
from google.genai import types
from googleapiclient.discovery import build

def web_search(queries: list[str]):
    """
    Performs a web search for the given queries using the Google Custom Search JSON API.

    Args:
        queries (list[str]): A list of search queries to be combined into a single search.

    Returns:
        str: A JSON formatted string summarizing the search results.
    """
    try:
        query = " ".join(queries)
        
        # Get the required keys from environment variables
        api_key = os.environ.get("GOOGLE_API_KEY")
        search_engine_id = os.environ.get("SEARCH_ENGINE_ID")

        if not api_key:
            return "Error: GOOGLE_API_KEY not found. Please add it to your .env file."
        if not search_engine_id:
            return "Error: SEARCH_ENGINE_ID not found. Please add it to your .env file."

        # Build the service object for the Custom Search API
        service = build("customsearch", "v1", developerKey=api_key)
        
        # Execute the search
        res = service.cse().list(q=query, cx=search_engine_id, num=3).execute()

        # Extract and summarize the results
        summary = []
        if "items" in res:
            for item in res["items"]:
                summary.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                })

        return json.dumps(summary, indent=2)

    except Exception as e:
        return f"Error performing web search: {str(e)}"

# --- Gemini Function Declaration ---
schema_web_search = types.FunctionDeclaration(
    name="web_search",
    description="Performs a web search using the Google Custom Search API and returns a summary of the top results.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "queries": types.Schema(
                type=types.Type.ARRAY,
                description="A list of search queries to be combined into one search.",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
        required=["queries"],
    ),
)