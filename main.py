import os
from typing import Optional
import asyncio

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context

# 이미 만들어둔 에이전트들 import
from agents.file_viewer_agent import file_viewer_agent
from agents.search_agent import search_agent
from agents.write_agent import write_agent
from agents.review_agent import review_agent
from utils.logging_config import setup_logger

from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)
logger = setup_logger(name="readme_agent", log_dir="./logs")

# 1) 멀티 에이전트 워크플로우 인스턴스 생성
readme_workflow = AgentWorkflow(
    # 모든 에이전트 등록
    agents=[
        file_viewer_agent,
        search_agent,
        write_agent,
        review_agent,
    ],
    # 루트 에이전트: README 생성을 요청하면 제일 먼저 프로젝트 코드를 읽는 역할
    root_agent="FileViewerAgent",

    # (선택) 워크플로우 공용 상태 초기값
    # 여기서는 최소한으로만 사용하고, 실제 세부 정보는 각 tool(record_notes 등)에서 관리하게 둠
    initial_state={
        "project_root": None,     # 분석 대상 디렉토리 경로
        "user_requirements": "",  # 사용자가 README에 꼭 넣고 싶은 요구사항 텍스트
    }
)


# 2) 편하게 쓰기 위한 헬퍼 함수
async def generate_readme_for_project(
    project_root: str,
    user_requirements: Optional[str] = None,
    existing_readme_path: str = "README.md",
) -> str:
    """
    프로젝트 디렉토리만 넘기면,
    FileViewer → Search → Write → Review까지 한 번에 돌려 README를 생성/검수하는 함수.

    Args:
        project_root (str):
            분석할 프로젝트 루트 디렉토리 경로.
            FileViewerAgent의 get_directory_structure / read_file가 이 경로를 기준으로 동작한다고 가정.
        user_requirements (str, optional):
            README에 반드시 포함되었으면 하는 요구사항 또는 설명.
            예: "한국어 README로 작성, 설치/실행 예제를 꼭 넣어줘" 등.
        existing_readme_path (str, optional):
            기존 README 경로. 있으면 FileViewerAgent/WriteAgent가 참고할 수 있음.
            기본값은 "README.md".

    Returns:
        str: 워크플로우 최종 응답(대개 ReviewAgent 또는 WriteAgent의 자연어 요약 응답)
    """
    # 워크플로우 컨텍스트
    ctx = Context(readme_workflow)

    # 공용 상태에 기본 정보 저장
    state = {
        "project_root": os.path.abspath(project_root),
        "user_requirements": user_requirements or "",
        "existing_readme_path": os.path.abspath(existing_readme_path),
    }
    await ctx.store.set("state", state)

    # 루트 에이전트(FileViewerAgent)에게 넘길 첫 유저 메시지
    user_msg = (
        "다음 프로젝트 디렉토리에 대해 README를 새로 작성하고, "
        "최종적으로 검수까지 완료해줘.\n\n"
        f"- project_root: {state['project_root']}\n"
        f"- existing_readme_path: {state['existing_readme_path']}\n"
        f"- user_requirements: {state['user_requirements'] or '없음'}\n\n"
        "FileViewerAgent → SearchAgent → WriteAgent → ReviewAgent 순서로, "
        "필요한 만큼 handoff를 수행하면서 최종 완성도 높은 README를 만들어줘."
    )

    # ✅ 여기서는 await 하지 않음 (스트리밍 핸들러를 받기 위함)
    handler = readme_workflow.run(user_msg=user_msg, ctx=ctx, max_iterations=None)

    current_agent = None

    logger.info(f">>>>>>>>>>[START]<<<<<<<<<")
    async for event in handler.stream_events():
        if (
            hasattr(event, "current_agent_name")
            and event.current_agent_name != current_agent
        ):
            current_agent = event.current_agent_name
            logger.info(f"{'='*50}")
            logger.info(f"🤖 Agent: {current_agent}")
            logger.info(f"{'='*50}\n\n")

        if isinstance(event, AgentOutput):
            if event.response.content:
                logger.info(f"📤 Output: {event.response.content}")
            if event.tool_calls:
                logger.info(
                    f"🛠️ Planning to use tools: {[call.tool_name for call in event.tool_calls]}"
                )

        elif isinstance(event, ToolCallResult):
            logger.info(f"🔧 Tool Result ({event.tool_name}):")
            logger.info(f"  Arguments: {event.tool_kwargs}")
            logger.info(f"  Output: {event.tool_output}")

        elif isinstance(event, ToolCall):
            logger.info(f"🔨 Calling Tool: {event.tool_name}")
            logger.info(f"  With arguments: {event.tool_kwargs}")

    # ✅ 스트리밍이 끝나면 최종 결과를 await 로 한 번 더 받음
    final_response = await handler  # AgentOutput
    logger.info(f">>>>>>>>>>[END]<<<<<<<<<<\n\n")
    # 최종 응답을 문자열로 반환
    return str(final_response)




async def main():
    from cli import args
    result = await generate_readme_for_project(
        project_root=args.path,
        user_requirements="README는 한국어로 작성하고, 설치/실행 방법을 예시 코드와 함께 꼭 포함해줘.",
    )
    print("=== Workflow Result ===")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())