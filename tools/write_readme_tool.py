from llama_index.core.workflow import Context

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