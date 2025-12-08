import os
import yaml
from llama_index.core.agent.workflow import ReActAgent
from model import load_llm_model
from tools.search_web_tool import search_web


agent_system_prompt_path = os.path.join(os.path.dirname(__file__), "../templates/agent_system_prompt.yaml")
with open(agent_system_prompt_path, 'r', encoding='utf-8') as f:
    agent_system_prompt = yaml.safe_load(f)

search_llm = load_llm_model(temperature=0.3, top_p=0.5, max_tokens=8192)

search_agent = ReActAgent(
    name="SearchAgent",
    description="Collects up-to-date external information about the technologies used in the project via web search.",
    tools=[search_web],
    system_prompt=agent_system_prompt["SearchAgent"],
    llm=search_llm,
    can_handoff_to=["WriteAgent", "ReviewAgent"],
)