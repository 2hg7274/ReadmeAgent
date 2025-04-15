from tavily import AsyncTavilyClient
from configs import TAVILY_API

async def search_web(query: str) -> str:
    """
    Performs a web search using the Tavily API to retrieve relevant information 
    based on a given query.

    This tool is useful for obtaining additional context or technical explanations 
    that are not present in the codebase but are required to enhance the README 
    or clarify complex terms during review.

    Input should be a clear natural language query string.
    """
    client = AsyncTavilyClient(api_key=TAVILY_API)
    return str(await client.search(query))