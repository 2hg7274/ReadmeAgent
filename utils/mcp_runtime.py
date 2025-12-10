"""
Utility helpers for sharing runtime metadata with the MCP server.
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
RUNTIME_PATH = LOGS_DIR / "mcp_runtime.json"


def write_runtime_config(**entries: Any) -> None:
    """
    Persist runtime metadata (e.g., project_root) so the MCP server can pick it up.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    payload: Dict[str, Any] = {}

    if RUNTIME_PATH.exists():
        try:
            payload = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}

    payload.update(entries)
    RUNTIME_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def read_runtime_config() -> Dict[str, Any]:
    if not RUNTIME_PATH.exists():
        return {}

    try:
        return json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
