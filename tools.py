import os
from llama_index.core.workflow import Context
from tavily import AsyncTavilyClient
from configs import TAVILY_API




async def extract_files_from_directory(directory_path: str) -> dict:
    """
    Scans a given project directory recursively and extracts the textual content 
    of supported files including .py, .ipynb, .md, .json, and .txt formats.
    
    This tool is useful for agents that need to analyze the source code or documentation 
    of a project in order to understand its structure and functionality.
    """
    supported_extensions = [".py", ".ipynb", ".md", ".json", ".txt"]
    extracted = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in supported_extensions:
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    extracted[file] = f.read()
    return extracted




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



async def record_notes(ctx: Context, notes: str, title: str) -> str:
    """
    Stores extracted and summarized notes into the shared state context under a given title.
    
    This tool helps the agent to save its analysis of the project files, which will be 
    used by other agents (like the WriteAgent) to generate meaningful documentation.
    
    Input should include both the notes content and the title to be saved under.
    """
    state = await ctx.get("state")
    state.setdefault("notes", {})[title] = notes
    await ctx.set("state", state)
    return "Notes recorded."


async def write_readme(ctx: Context, content: str) -> str:
    """
    Saves the generated README content into the shared state context.

    This tool is used to store a markdown-formatted README based on notes 
    gathered from the project files. The content will be later reviewed 
    and possibly revised based on feedback.

    Input should be a fully written README in markdown format.
    """
    state = await ctx.get("state")
    state["readme"] = content
    await ctx.set("state", state)
    return "README written."



async def review_readme(ctx: Context, feedback: str):
    """
    Records feedback or review comments about the generated README content.

    This tool allows the agent to provide constructive criticism or 
    suggestions for improvement, which will be handled by the WriteAgent 
    in later phases of the workflow.

    Input should be textual feedback related to the current README.
    """
    state = await ctx.get("state")
    state["feedback"] = feedback
    await ctx.set("state", state)
    return "Feedback recorded."