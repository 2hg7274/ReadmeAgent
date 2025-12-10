"""
Helper utilities to fetch MCP-exposed tools for local agents.

This module connects to the ReadmeAgent MCP server, converts the advertised
tools into LlamaIndex-compatible tool objects, and caches them for reuse.
"""
import asyncio
import os
from typing import Dict, Iterable, List, Optional

from llama_index.core.tools import BaseTool
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

MCP_SERVER_URL = os.environ.get("README_AGENT_MCP_SERVER_URL", "http://localhost:8000/sse")

_tool_cache: Dict[str, BaseTool] = {}
_client: Optional[BasicMCPClient] = None


async def _fetch_tools_async() -> Dict[str, BaseTool]:
    """
    Contact the MCP server, convert every tool into a LlamaIndex Tool, and
    return a mapping keyed by tool name.
    """
    global _client

    if _client is None:
        _client = BasicMCPClient(MCP_SERVER_URL)

    tool_spec = McpToolSpec(client=_client)
    tool_list = await tool_spec.to_tool_list_async()
    return {tool.metadata.name: tool for tool in tool_list}


def _ensure_tools_loaded() -> Dict[str, BaseTool]:
    global _tool_cache

    if not _tool_cache:
        _tool_cache = asyncio.run(_fetch_tools_async())

    return _tool_cache


def get_mcp_tool(name: str) -> BaseTool:
    """
    Retrieve a single MCP-backed tool by name.

    Raises:
        KeyError: if the tool is not exposed by the MCP server.
    """
    tools = _ensure_tools_loaded()

    if name not in tools:
        raise KeyError(f"Tool '{name}' not published by MCP server at {MCP_SERVER_URL}")

    return tools[name]


def get_mcp_tools(names: Iterable[str]) -> List[BaseTool]:
    """
    Retrieve a list of MCP-backed tools, preserving the requested order.
    """
    return [get_mcp_tool(name) for name in names]
