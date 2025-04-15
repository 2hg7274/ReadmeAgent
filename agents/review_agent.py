from llama_index.core.agent.workflow import ReActAgent
from model import llm
from tools.review_readme_tool import review_readme
from prompts import WRITE_AGENT_SYSTEM_PROMPT

review_agent = ReActAgent(
    name="ReviewAgent",
    description="Reviews the README and gives constructive feedback.",
    tools=[review_readme],
    system_prompt = WRITE_AGENT_SYSTEM_PROMPT,
    llm=llm,
    can_handoff_to=["WriteAgent", "SearchAgent"]
)