import os
from pathlib import Path
from typing import Literal
from llama_index.core.workflow import Context
from llama_index.core.tools import FunctionTool


async def _write_readme(
    ctx: Context,
    content: str,
    relative_path: str = "README.md",
    mode: Literal["overwrite", "append"] = "overwrite",
) -> str:
    state = await ctx.store.get("state") or {}
    project_root = state.get("project_root") or os.getcwd()

    base = Path(project_root)
    base.mkdir(parents=True, exist_ok=True)

    p = base / relative_path

    try:
        if mode == "append" and p.exists():
            existing = p.read_text(encoding="utf-8", errors="ignore")
            if existing.strip():
                new_content = existing.rstrip() + "\n\n" + content.lstrip()
            else:
                new_content = content
        else:
            # overwrite: 기존 내용 무조건 날리고 새로 작성
            new_content = content

        p.write_text(new_content, encoding="utf-8")
        return f"README successfully written to: {p.resolve()}"

    except Exception as e:
        return f"[ERROR] Failed to write README to {p}: {e}"





# ==============================================================================================================
write_readme = FunctionTool.from_defaults(
    fn=_write_readme,
    name="write_readme",
    description=(
        "Write or update a README file inside the current project's root directory.\n\n"
        "The project root directory is taken from the workflow state ('project_root'), "
        "so the agent only needs to provide a relative path such as 'README.md'.\n\n"
        "Args:\n"
        "  content (str): Markdown content to write.\n"
        "  relative_path (str, optional): Path relative to project_root. Defaults to 'README.md'.\n"
        "  mode (Literal['overwrite', 'append'], optional): Overwrite or append mode. Defaults to 'overwrite'.\n\n"
        "Returns:\n"
        "  str: A success or error message including the absolute path of the written README.\n"
    ),
)