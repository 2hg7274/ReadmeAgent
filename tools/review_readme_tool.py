from typing import Dict, Any
from llama_index.core.tools import FunctionTool
from model import load_llm_model

review_tool_llm = load_llm_model(temperature=0.2, top_p=0.4, max_tokens=8192)


async def _review_readme(readme_text: str, file_notes: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
다음은 프로젝트 README 내용입니다:

[README]
{readme_text}

다음은 FileViewerAgent가 분석하여 기록한 프로젝트 구조 요약 노트입니다:

[FILE NOTES]
{file_notes}

README의 정확성과 완성도를 검토하고 다음 형식의 JSON 형태로 답변하세요:

{
  "missing_items": ["README에 포함되지 않은 중요한 항목들"],
  "incorrect_descriptions": ["잘못된 설명 또는 코드 구조와 맞지 않는 부분"],
  "unclear_sections": ["설명이 애매하거나 구체성이 부족한 부분"],
  "suggested_patches": [
      {
        "section": "섹션 이름 또는 위치",
        "before": "(기존 내용 요약)",
        "after": "(개선된 추천 내용)"
      }
  ]
}

반드시 JSON 형식만 출력하세요.
    """

    result = await review_tool_llm.apredict(prompt)
    return {"review": result}




# ==============================================================================================================
review_readme = FunctionTool.from_defaults(
    fn=_review_readme,
    name="review_readme",
    description=(
        "Evaluate the quality, accuracy, and completeness of a generated README by comparing it "
        "to the structured analysis notes produced by the FileViewerAgent.\n\n"
        "This tool identifies:\n"
        "  - Missing important information that should appear in the README\n"
        "  - Incorrect statements or mismatches with actual project structure\n"
        "  - Unclear or ambiguous sections\n"
        "  - Suggested improved text (patches) that can be directly used to modify the README\n\n"
        "Args:\n"
        "  readme_text (str): The full README content produced by the WriteAgent.\n"
        "  file_notes (dict): Structured project-analysis notes created by the FileViewerAgent.\n\n"
        "Returns:\n"
        "  dict: A JSON-like structured feedback object containing missing items, incorrect facts, "
        "unclear sections, and suggested patches.\n"
    ),
)
