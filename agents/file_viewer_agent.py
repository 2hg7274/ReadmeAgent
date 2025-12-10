import os
import yaml
from llama_index.core.agent.workflow import ReActAgent
from model import load_llm_model
from tools.mcp_tool_registry import get_mcp_tools


agent_system_prompt_path = os.path.join(os.path.dirname(__file__), "../templates/agent_system_prompt.yaml")
with open(agent_system_prompt_path, 'r', encoding='utf-8') as f:
    agent_system_prompt = yaml.safe_load(f)

file_viewer_llm = load_llm_model(temperature=0.1, top_p=0.1, max_tokens=8192)

file_viewer_tools = get_mcp_tools(
    ["get_directory_structure", "read_file", "read_file_chunk", "record_notes"]
)


file_viewer_agent = ReActAgent(
    name="FileViewerAgent",
    description="Analyzes the project directory and source files to produce structured notes for README generation.",
    tools=file_viewer_tools,
    system_prompt=agent_system_prompt["FileViewerAgent"],
    llm=file_viewer_llm,
    can_handoff_to=["SearchAgent", "WriteAgent"],
)
