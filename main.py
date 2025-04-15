import os
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.agent.workflow import (
    AgentOutput,
    ToolCall,
    ToolCallResult,
)
from agents.file_viewer_agent import file_viewer_agent
from agents.write_agent import write_agent
from agents.review_agent import review_agent
from agents.search_agent import search_agent

import asyncio




agent_workflow = AgentWorkflow(
    agents=[file_viewer_agent, write_agent, review_agent, search_agent],
    root_agent=file_viewer_agent.name,
    initial_state={
        "notes": {},
        "readme": "",
        "feedback": "Feedback required."
    }
)


async def main(project_dir_path):
    user_msg = (
        f"Analyze the following project directory: {project_dir_path}. "
        "Generate a professional README.md file based on the analysis. "
        "If a README.md file already exists, compare its current contents with the summary of the project's files, "
        "and incorporate any missing or updated information into the README. "
        "Ensure that the final README clearly reflects any previous valuable content along with new updates."
    )
    print("\n📂 Starting multi-agent README generation workflow...\n")
    handler = agent_workflow.run(user_msg=user_msg)

    current_agent = None
    async for event in handler.stream_events():
        # 에이전트가 바뀔 때 표시
        if hasattr(event, "current_agent_name") and event.current_agent_name != current_agent:
            current_agent = event.current_agent_name
            print(f"\n{'='*60}")
            print(f"🤖 Current Agent: {current_agent}")
            print(f"{'='*60}\n")
        # LLM 응답 출력
        elif isinstance(event, AgentOutput):
            if event.response.content:
                print(f"\n📤 Agent Output:\n{event.response.content}\n")
            if event.tool_calls:
                print(f"🛠️  Planned Tool Calls: {[call.tool_name for call in event.tool_calls]}")


        # 툴 결과 반환
        elif isinstance(event, ToolCallResult):
            print(f"\n🔧 Tool Result: {event.tool_name}")
            print(f"    Arguments: {event.tool_kwargs}")
            print(f"    Output: {event.tool_output}")

        # 툴 호출
        elif isinstance(event, ToolCall):
            print(f"\n🔨 Calling Tool: {event.tool_name}")
            print(f"    Arguments: {event.tool_kwargs}")

    # 최종 상태 확인 및 README 저장
    state = await handler.ctx.get("state")
    readme = state.get("readme", "No README generated.")
    readme_path = os.path.join(project_dir_path, "README.md")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"\n✅ README.md has been successfully saved to: {readme_path}")



if __name__=="__main__":
    from cli import args
    asyncio.run(main(args.path))