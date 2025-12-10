"""
Expose all ReadmeAgent_test tools through a single MCP server.

This server wraps the existing LlamaIndex-focused tool logic so external clients
can call them over the MCP protocol.
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

CURRENT_DIR = Path(__file__).resolve().parent      # ReadmeAgent_test/tools
PROJECT_ROOT = CURRENT_DIR.parent                 # ReadmeAgent_test

# 프로젝트 루트 & tools 경로 모두 등록
for p in [PROJECT_ROOT, CURRENT_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from tools.file_viewer_tools import (
    _get_directory_structure as get_directory_structure_impl,
    _read_file as read_file_impl,
    _read_file_chunk as read_file_chunk_impl,
)
from tools.review_readme_tool import _review_readme as review_readme_impl
from tools.search_web_tool import _search_web as search_web_impl
from utils.mcp_runtime import read_runtime_config

mcp = FastMCP("readme-agent-tools", host="localhost")

LOGS_DIR = PROJECT_ROOT / "logs"
NOTES_STORE_PATH = LOGS_DIR / "mcp_notes.json"
NOTES_CACHE: Dict[str, Dict[str, Any]] = {}


def _load_notes_from_disk() -> None:
    if not NOTES_STORE_PATH.exists():
        return

    try:
        NOTES_CACHE.update(json.loads(NOTES_STORE_PATH.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        pass


def _persist_notes_to_disk() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_STORE_PATH.write_text(
        json.dumps(NOTES_CACHE, indent=2, ensure_ascii=True), encoding="utf-8"
    )


def _resolve_project_root(project_root: Optional[str]) -> Path:
    if project_root:
        return Path(project_root).expanduser().resolve()
    env_root = os.environ.get("README_AGENT_PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    runtime = read_runtime_config()
    runtime_root = runtime.get("project_root")
    if runtime_root:
        return Path(runtime_root).expanduser().resolve()
    return Path.cwd()


_load_notes_from_disk()


@mcp.tool(
    name="get_directory_structure",
    title="Inspect Directory Structure",
    description=(
        "Recursively scan a directory (skipping temporary/cache folders) "
        "and return the nested folder/file layout."
    ),
)
def get_directory_structure(path: str) -> Dict[str, Any]:
    return get_directory_structure_impl(path)


@mcp.tool(
    name="read_file",
    title="Read File",
    description=(
        "Read up to max_chars from the target file (README.md is skipped). "
        "Returns UTF-8 text or an error message."
    ),
)
def read_file(file_path: str, max_chars: int = 8000) -> str:
    return read_file_impl(file_path=file_path, max_chars=max_chars)


@mcp.tool(
    name="read_file_chunk",
    title="Read File Chunk",
    description=(
        "Read a slice of a large file by passing an offset and max_chars. "
        "Returns the content chunk plus pagination metadata."
    ),
)
def read_file_chunk(file_path: str, offset: int = 0, max_chars: int = 8000) -> Dict[str, Any]:
    return read_file_chunk_impl(file_path=file_path, offset=offset, max_chars=max_chars)


@mcp.tool(
    name="record_notes",
    title="Record Project Notes",
    description=(
        "Persist project-analysis notes under a title so other agents can reuse them. "
        "Notes are cached in-memory and in logs/mcp_notes.json."
    ),
)
def record_notes(
    notes: str,
    notes_title: str = "project_overview",
    project_root: Optional[str] = None,
    persist: bool = True,
) -> Dict[str, Any]:
    base = _resolve_project_root(project_root)
    NOTES_CACHE[notes_title] = {"notes": notes, "project_root": str(base)}

    if persist:
        _persist_notes_to_disk()

    return {
        "stored_title": notes_title,
        "project_root": str(base),
        "notes_count": len(NOTES_CACHE),
    }


@mcp.tool(
    name="write_readme",
    title="Write README",
    description=(
        "Write markdown content to a README. Provide the project root (or rely on "
        "README_AGENT_PROJECT_ROOT env / current working dir). Mode can be 'overwrite' or 'append'."
    ),
)
def write_readme(
    content: str,
    relative_path: str = "README.md",
    mode: str = "overwrite",
    project_root: Optional[str] = None,
) -> Dict[str, Any]:
    if mode not in {"overwrite", "append"}:
        return {"error": f"Unsupported mode: {mode}"}

    base = _resolve_project_root(project_root)
    base.mkdir(parents=True, exist_ok=True)
    target = base / relative_path

    try:
        if mode == "append" and target.exists():
            existing = target.read_text(encoding="utf-8", errors="ignore")
            if existing.strip():
                new_content = existing.rstrip() + "\n\n" + content.lstrip()
            else:
                new_content = content
        else:
            new_content = content

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_content, encoding="utf-8")
        return {"message": "README written successfully", "path": str(target.resolve())}
    except Exception as exc:
        return {"error": f"Failed to write README: {exc}"}


@mcp.tool(
    name="search_web",
    title="Search Web (Tavily)",
    description="Proxy to the Tavily async client used by the SearchAgent.",
)
async def search_web(query: str, max_results: int = 5) -> Dict[str, Any]:
    return await search_web_impl(query=query, max_results=max_results)


@mcp.tool(
    name="review_readme",
    title="Review README",
    description="Call the ReviewAgent LLM to evaluate a README against stored file notes.",
)
async def review_readme(readme_text: str, file_notes: Dict[str, Any]) -> Dict[str, Any]:
    return await review_readme_impl(readme_text=readme_text, file_notes=file_notes)


if __name__ == "__main__":
    print("Starting ReadmeAgent MCP server...")
    mcp.run(transport="sse")
