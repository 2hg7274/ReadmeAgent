import os
import yaml
from llama_index.core.agent.workflow import ReActAgent
from model import load_llm_model
from tools.mcp_tool_registry import get_mcp_tools


agent_system_prompt_path = os.path.join(
    os.path.dirname(__file__),
    "../templates/agent_system_prompt.yaml",
)

with open(agent_system_prompt_path, "r", encoding="utf-8") as f:
    agent_system_prompt = yaml.safe_load(f)

write_llm = load_llm_model(
    temperature=0.3, 
    top_p=0.9,
    max_tokens=8192,
)

write_tools = get_mcp_tools(["write_readme"])

write_agent = ReActAgent(
    name="WriteAgent",
    description="Generates or updates the project README using internal analysis notes and external web information.",
    tools=write_tools,
    system_prompt=agent_system_prompt["WriteAgent"],
    llm=write_llm,
    can_handoff_to=["ReviewAgent"],
)
