import os
import yaml
from llama_index.core.agent.workflow import ReActAgent
from model import load_llm_model
from tools.review_readme_tool import review_readme


agent_system_prompt_path = os.path.join(os.path.dirname(__file__), "../templates/agent_system_prompt.yaml")
with open(agent_system_prompt_path, "r", encoding="utf-8") as f:
    agent_system_prompt = yaml.safe_load(f)

review_llm = load_llm_model(temperature=0.2, top_p=0.6, max_tokens=8192)


review_agent = ReActAgent(
    name="ReviewAgent",
    description="Reviews the generated README against the project analysis notes and suggests corrections and improvements.",
    tools=[review_readme],
    system_prompt=agent_system_prompt["ReviewAgent"],
    llm=review_llm,
    can_handoff_to=["WriteAgent"],
)
