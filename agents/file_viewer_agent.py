from llama_index.core.agent.workflow import ReActAgent
from model import llm
from tools.file_viewer_tools import get_directory_structure, read_file, record_notes
from prompts import FILE_VIEWER_AGENT_SYSTEM_PROMPT

file_viewer_agent = ReActAgent(
    name="FileViewerAgent",
    description="Extracts content from project files and writes notes.",
    tools=[get_directory_structure, read_file, record_notes],
    system_prompt = FILE_VIEWER_AGENT_SYSTEM_PROMPT,
    llm=llm,
    can_handoff_to=["WriteAgent"]
)