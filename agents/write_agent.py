from llama_index.core.agent.workflow import ReActAgent
from model import llm
from tools.write_readme_tool import write_readme
from prompts import WRITE_AGENT_SYSTEM_PROMPT

write_agent = ReActAgent(
    name="WriteAgent",
    description="Writes a structured README.md from notes.",
    tools=[write_readme],
    system_prompt = WRITE_AGENT_SYSTEM_PROMPT,
    llm=llm,
    can_handoff_to=["ReviewAgent"]
)