import os
from typing import Optional
import asyncio
import traceback

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from workflows.errors import WorkflowRuntimeError

from agents.file_viewer_agent import file_viewer_agent
from agents.search_agent import search_agent
from agents.write_agent import write_agent
from agents.review_agent import review_agent
from utils.logging_config import setup_logger
from utils.mcp_runtime import write_runtime_config

from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)

logger = setup_logger(name="readme_agent", log_dir="./logs")


# 워크플로우 정의
readme_workflow = AgentWorkflow(
    agents=[file_viewer_agent, search_agent, write_agent, review_agent],
    root_agent="FileViewerAgent",
    initial_state={
        "project_root": None,
        "user_requirements": "",
    },
)


# -------------------------------------------------------------------
# 🔥 안전하게 워크플로우 실행하는 모듈형 함수
# -------------------------------------------------------------------
async def _run_workflow_single_attempt(ctx: Context, user_msg: str) -> str:
    """단일 워크플로우 실행 (한 번의 attempt)
       실패 시 예외를 던짐 (상위에서 retry 처리)
    """
    handler = readme_workflow.run(
        user_msg=user_msg,
        ctx=ctx,
        max_iterations=50,
    )

    current_agent = None

    async for event in handler.stream_events():
        # Agent change log
        if hasattr(event, "current_agent_name"):
            if event.current_agent_name != current_agent:
                current_agent = event.current_agent_name
                logger.info(f"\n========== AGENT: {current_agent} ==========\n")

        # AgentOutput
        if isinstance(event, AgentOutput):
            if event.response and event.response.content:
                logger.info(f"📤 Output: {event.response.content}")
            else:
                logger.warning("⚠️ AgentOutput 가 비어 있음 (빈 메시지 위험)")

        # ToolCallResult
        elif isinstance(event, ToolCallResult):
            logger.info(f"🔧 Tool Result ({event.tool_name})")
            logger.info(f"Args: {event.tool_kwargs}")
            logger.info(f"Output: {str(event.tool_output)[:800]}")

    final_response = await handler

    # final_response 검증
    if (
        final_response is None
        or final_response.response is None
        or not getattr(final_response.response, "content", "").strip()
    ):
        raise ValueError("Final response was empty")

    return final_response.response.content


# -------------------------------------------------------------------
# 🔥 Retry logic 적용된 최종 호출 함수
# -------------------------------------------------------------------
async def generate_readme_for_project(
    project_root: str,
    user_requirements: Optional[str] = None,
    existing_readme_path: str = "README.md",
    max_retries: int = 3,  # 🔥 실패하면 자동 재시도 횟수
) -> str:

    state = {
        "project_root": os.path.abspath(project_root),
        "user_requirements": user_requirements or "",
        "existing_readme_path": os.path.abspath(existing_readme_path),
    }

    # root 프롬프트
    base_user_msg = (
        "다음 프로젝트 디렉토리에 대해 README를 새로 작성하고, "
        "최종적으로 검수까지 완료해줘.\n\n"
        f"- project_root: {state['project_root']}\n"
        f"- existing_readme_path: {state['existing_readme_path']}\n"
        f"- user_requirements: {state['user_requirements'] or '없음'}\n\n"
        "FileViewerAgent → SearchAgent → WriteAgent → ReviewAgent 순서로, "
        "필요한 만큼 handoff를 수행해서 최종 완성도 높은 README를 만들어줘."
    )

    
    
    # 재시도 루프
    for attempt in range(1, max_retries + 1):
        logger.info(f"\n\n🚀 [ATTEMPT {attempt}/{max_retries}] 워크플로우 실행 시작\n")

        ctx = Context(readme_workflow)
        await ctx.store.set("state", state)
        write_runtime_config(project_root=state["project_root"])

        try:
            result = await _run_workflow_single_attempt(ctx, base_user_msg)
            logger.info("🎉 워크플로우 성공적으로 완료!")
            return result

        except WorkflowRuntimeError as e:
            logger.error(f"❌ WorkflowRuntimeError 발생: {e}")
            logger.error(traceback.format_exc())

            if "Got empty message" in str(e):
                logger.error("⚠️ LLM 빈 응답 문제. 재시도 진행.")
                continue

        except ValueError as e:
            logger.error(f"❌ ValueError: {e}")
            if "empty" in str(e).lower():
                logger.error("⚠️ 빈 응답 감지 → 재시도")
                continue

        except Exception as e:
            logger.error(f"❌ 예상 외 예외 발생: {e}")
            logger.error(traceback.format_exc())
            continue

    # 🔥 모든 재시도 실패 시 최종 메시지 반환
    return (
        "워크플로우가 여러 번 실패하여 README 생성에 실패했습니다.\n"
        "하지만 에이전트가 가능한 모든 재시도를 수행했습니다.\n"
        "입력 데이터 또는 모델 설정을 점검해 주세요."
    )


# -------------------------------------------------------------------
async def main():
    from cli import args
    result = await generate_readme_for_project(
        project_root=args.path,
        user_requirements="README는 한국어로 작성하고, 설치/실행 예제를 꼭 포함해주세요.",
        max_retries=3,
    )
    print("=== Workflow Result ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
