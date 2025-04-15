from llama_index.core.agent.workflow import ReActAgent
from model import llm
from tools.search_web_tool import search_web
from prompts import SEARCH_AGENT_SYSTEM_PROMPT

search_agent = ReActAgent(
    name="SearchAgent",
    description="Performs external web search to support README generation.",
    tools=[search_web],
    system_prompt = SEARCH_AGENT_SYSTEM_PROMPT,
    llm=llm,
    can_handoff_to=["WriteAgent"]
)