# tools/write_tools.py
from pathlib import Path
from typing import Literal
from llama_index.core.tools import FunctionTool


def _write_readme(
    content: str,
    path: str = "README.md",
    mode: Literal["overwrite", "append"] = "overwrite",
) -> str:
    p = Path(path)

    try:
        if mode == "append" and p.exists():
            existing = p.read_text(encoding="utf-8", errors="ignore")
            if existing.strip():
                new_content = existing.rstrip() + "\n\n" + content.lstrip()
            else:
                new_content = content
        else:
            # Always fully overwrite (delete previous content)
            new_content = content

        p.write_text(new_content, encoding="utf-8")
        return f"README successfully written to: {p.resolve()}"

    except Exception as e:
        return f"[ERROR] Failed to write README to {path}: {e}"


write_readme = FunctionTool.from_defaults(
    fn=_write_readme,
    name="write_readme",
    description=(
        "Write or update a README file on disk using the provided Markdown content.\n\n"
        "Mode behavior:\n"
        "  - overwrite: Always clears existing content and writes a completely new README.\n"
        "  - append: Appends the provided content to the end of the existing README.\n\n"
        "Args:\n"
        "  content (str): The Markdown content to write.\n"
        "  path (str, optional): Path to the README file. Defaults to 'README.md'.\n"
        "  mode (Literal['overwrite', 'append'], optional): Overwrite or append mode.\n\n"
        "Returns:\n"
        "  str: A success or error message.\n"
    ),
)
