import os
import pathspec
from llama_index.core.workflow import Context

async def get_directory_structure(directory_path: str, root: str = None) -> dict:
    """
    Recursively scans the given project directory using os.listdir and returns
    a nested dictionary representing the directory structure. It excludes:
    - Hidden files and directories (names starting with a dot)
    - Directories named '__pycache__'
    - Files/directories that match the patterns in the .gitignore file located at the project root
    
    Args:
        directory_path (str): The current directory to scan.
        root (str): The project root against which .gitignore patterns are evaluated.
                    On the first call, if None, it is set to directory_path.
        
    Returns:
        dict: A nested dictionary where keys are directory names and a special key "files"
              lists the files directly contained in that directory.
              
    Example output:
    {
        "src": {
            "models": {
                "files": ["model.py"]
            },
            "files": ["main.py", "utils.py"]
        },
        "files": ["setup.py", "requirements.txt"]
    }
    """
    if root is None:
        root = directory_path

    # Load .gitignore patterns from the root (if available)
    gitignore_file = os.path.join(root, ".gitignore")
    spec = None
    if os.path.exists(gitignore_file):
        try:
            with open(gitignore_file, "r", encoding="utf-8", errors="ignore") as f:
                patterns = f.read().splitlines()
            spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        except Exception as e:
            # .gitignore 읽기 실패 시 무시하고 진행할 수 있습니다.
            spec = None

    structure = {}
    files_list = []
    
    try:
        items = os.listdir(directory_path)
    except Exception as e:
        return {"error": f"Error accessing directory: {e}"}
    
    for item in items:
        # Skip hidden items
        if item.startswith("."):
            continue

        # Calculate the relative path from the project root
        relative_item = os.path.relpath(os.path.join(directory_path, item), root)

        # If .gitignore patterns exist and the item matches, skip it.
        if spec and spec.match_file(relative_item):
            continue

        full_path = os.path.join(directory_path, item)
        if os.path.isdir(full_path):
            if item == '__pycache__':
                continue
            structure[item] = await get_directory_structure(full_path, root)
        else:
            files_list.append(item)
    
    if files_list:
        structure["files"] = files_list
    return structure


async def read_file(project_root: str, relative_file_path: str) -> str:
    """
    Reads the content of the file located at the given relative file path within the project.

    Args:
        project_root (str): The base directory (root) of the project.
        relative_file_path (str): The file's path relative to the project root.
        
    Returns:
        str: The content of the file, or an error message in case of failure.
        
    Example:
        If project_root is "/path/to/project" and relative_file_path is
        "function_calling/openai/functions.py", then the file is read from:
        "/path/to/project/function_calling/openai/functions.py".
    """
    full_path = os.path.join(project_root, relative_file_path)
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"



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