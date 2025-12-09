from pathlib import Path
from typing import Dict, Any, List
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context

EXCLUDED_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "env",
    "build",
    "dist",
    "node_modules",
    ".git",
    ".github",
}

def _get_directory_structure(root_path: str) -> Dict[str, Any]:
    root = Path(root_path).resolve()

    def _walk(dir_path: Path) -> Dict[str, Any]:
        dirs: List[Dict[str, Any]] = []
        files: List[str] = []
        file_paths: List[str] = []

        for p in dir_path.iterdir():
            # ⛔ 불필요한 디렉토리 제외
            if p.is_dir() and p.name in EXCLUDED_DIRS:
                continue
            if p.name.startswith(".") and p.is_dir():
                continue

            if p.is_dir():
                dirs.append(_walk(p))
            else:
                files.append(p.name)
                file_paths.append(str(p))  # ✅ 각 파일의 full path 저장

        return {
            "path": str(dir_path),
            "dirs": dirs,
            "files": files,
            "file_paths": file_paths,  # ✅ 새로 추가
        }

    return _walk(root)

def _read_file(file_path: str, max_chars: int = 8000) -> str:
    p = Path(file_path)

    # ✅ README.md는 읽지 않도록 차단 (대소문자 무시)
    if p.name.lower() == "readme.md":
        return "[SKIPPED] README.md is excluded from FileViewerAgent file reading."

    if not p.exists():
        return f"[ERROR] File not found: {file_path}"

    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[ERROR] Failed to read file {file_path}: {e}"

    if len(content) > max_chars:
        return content[:max_chars] + "\n\n[TRUNCATED]"
    return content

def _read_file_chunk(
    file_path: str,
    offset: int = 0,
    max_chars: int = 8000,
) -> Dict[str, Any]:
    """
    Read a slice of the file starting at `offset` with length `max_chars`.
    Returns both the content slice and the next offset if more content remains.
    """
    p = Path(file_path)

    # README.md는 스킵
    if p.name.lower() == "readme.md":
        return {
            "content": "",
            "skipped": True,
            "message": "README.md is excluded from FileViewerAgent file reading.",
            "next_offset": None,
            "has_more": False,
        }

    if not p.exists():
        return {
            "content": "",
            "error": f"File not found: {file_path}",
            "next_offset": None,
            "has_more": False,
        }

    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {
            "content": "",
            "error": f"Failed to read file {file_path}: {e}",
            "next_offset": None,
            "has_more": False,
        }

    total_len = len(text)

    if offset >= total_len:
        return {
            "content": "",
            "next_offset": None,
            "has_more": False,
        }

    end = min(offset + max_chars, total_len)
    slice_text = text[offset:end]

    has_more = end < total_len
    next_offset = end if has_more else None

    return {
        "content": slice_text,
        "next_offset": next_offset,
        "has_more": has_more,
        "length": total_len,
    }


async def _record_notes(ctx: Context, notes: str, notes_title: str = "project_overview") -> str:
    async with ctx.store.edit_state() as ctx_state:
        state = ctx_state["state"]

        if "file_viewer_notes" not in state:
            state["file_viewer_notes"] = {}

        state["file_viewer_notes"][notes_title] = notes

    return "Notes successfully recorded."





# ==============================================================================================================
get_directory_structure = FunctionTool.from_defaults(
    fn=_get_directory_structure,
    name="get_directory_structure",
    description=(
        "Recursively scan the given directory and return the full folder/file structure, "
        "excluding unnecessary system/cache folders such as '__pycache__', '.git', '.venv', etc.\n\n"
        "For each directory, the tool returns:\n"
        "  - 'path': the directory path\n"
        "  - 'dirs': a list of child directory structures (same schema)\n"
        "  - 'files': a list of file names directly under that directory\n"
        "  - 'file_paths': a list of full file paths directly under that directory\n\n"
        "The 'file_paths' field is intended to make it easy for the FileViewerAgent to call "
        "`read_file(file_path=...)` on every discovered file, if desired.\n\n"
        "Args:\n"
        "  root_path (str): The directory path to scan.\n\n"
        "Returns:\n"
        "  dict: A JSON-like mapping containing directories, local file names, and full file paths.\n"
    ),
)


read_file = FunctionTool.from_defaults(
    fn=_read_file,
    name="read_file",
    description=(
        "Read and return the content of a given file as plain UTF-8 text, "
        "except for 'README.md', which is intentionally skipped because it is the "
        "target document to be (re)generated.\n\n"
        "This tool is primarily used by the FileViewerAgent to inspect key source files such as "
        "entrypoints (e.g., `main.py`, `app.py`), core modules, configuration files, or initialization scripts. "
        "It is especially important when analyzing a project’s architecture, identifying business logic, "
        "understanding dependency patterns, or extracting execution flows from code.\n\n"
        "If the file is very large, the text will be truncated to avoid overwhelming the LLM. "
        "The truncated indicator `[TRUNCATED]` will be appended so the agent knows additional content exists.\n\n"
        "Args:\n"
        "  file_path (str): Path to the file to read.\n"
        "  max_chars (int, optional): Maximum characters to return. Defaults to 8000.\n\n"
        "Returns:\n"
        "  str: The text content of the file, a skip message for README.md, or an error message if reading fails.\n"
    ),
)


read_file_chunk = FunctionTool.from_defaults(
    fn=_read_file_chunk,
    name="read_file_chunk",
    description=(
        "Read a chunk of a file starting from a given character offset, up to `max_chars` characters.\n\n"
        "This tool is designed for large files that exceed the size limit of a single LLM context. "
        "Instead of truncating the file, the agent can call this tool multiple times with increasing "
        "`offset` values until all relevant parts of the file have been processed.\n\n"
        "The tool returns a JSON-like structure containing:\n"
        "  - 'content': the text slice read from the file\n"
        "  - 'next_offset': the next offset to use for reading the subsequent chunk (or null if no more data)\n"
        "  - 'has_more': a boolean flag indicating whether more content is available\n"
        "  - 'length': the total length of the file in characters\n\n"
        "Args:\n"
        "  file_path (str): Path to the file to read.\n"
        "  offset (int, optional): Character offset from which to start reading. Defaults to 0.\n"
        "  max_chars (int, optional): Maximum number of characters to read in this chunk. Defaults to 8000.\n\n"
        "Returns:\n"
        "  dict: A JSON-like object containing the 'content' slice and pagination info.\n"
    ),
)


record_notes = FunctionTool.from_defaults(
    fn=_record_notes,
    name="record_notes",
    description=(
        "Store structured project-analysis notes into the workflow state for later use by other agents.\n\n"
        "This tool should be invoked AFTER the FileViewerAgent completes its analysis of the project.\n\n"
        "The stored notes may include:\n"
        "  - Directory structure interpretation\n"
        "  - Key modules and their responsibilities\n"
        "  - Entrypoints and execution flow\n"
        "  - Configuration or environment dependencies\n"
        "  - Relationships between files or modules\n"
        "  - Any inferred insights that support README generation\n\n"
        "These notes will be consumed by downstream agents such as SearchAgent (for enrichment), "
        "WriteAgent (for README drafting), and ReviewAgent (for validation). "
        "This tool ensures that multi-agent workflows share a consistent understanding of the project.\n\n"
        "Args:\n"
        "  ctx (Context): LlamaIndex workflow context; required for editing workflow state.\n"
        "  notes (str): The full text of the analysis to store.\n"
        "  notes_title (str, optional): A category or label for the notes. Defaults to 'project_overview'.\n\n"
        "Returns:\n"
        "  str: A confirmation message indicating that notes were saved successfully.\n"
    ),
)