# ReadmeAgent

## 프로젝트 소개
ReadmeAgent는 **멀티‑에이전트 워크플로우**를 활용해 프로젝트 디렉터리를 자동으로 분석하고, 최신 기술 정보를 웹 검색으로 수집한 뒤, 한국어로 고품질 README를 자동 생성·검수하는 도구입니다. 주요 흐름은 다음과 같습니다.

1. **FileViewerAgent** – 프로젝트 파일 구조와 소스 코드를 스캔하여 구조화된 노트를 기록합니다.
2. **SearchAgent** – 사용된 기술(Python, LlamaIndex 등)에 대한 최신 정보를 웹 검색으로 수집합니다.
3. **WriteAgent** – 수집된 노트와 외부 정보를 바탕으로 한국어 README를 생성합니다.
4. **ReviewAgent** – 생성된 README를 검수하고 최종 수정 사항을 제안합니다.

## 주요 기능
- 프로젝트 구조 자동 분석
- 최신 기술 정보 자동 수집
- 한국어 README 자동 생성
- 자동 검수 및 피드백 제공

## 설치 방법
```bash
# 1. 레포지토리 클론
git clone https://github.com/yourusername/ReadmeAgent.git
cd ReadmeAgent

# 2. Python 3.11 이상 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt
```

## 사용법 (예시 코드)
아래 예시는 `generate_readme_for_project` 함수를 이용해 특정 프로젝트에 대한 README를 자동으로 생성하고 검수까지 진행하는 방법을 보여줍니다.

```python
import asyncio
from pathlib import Path
from ReadmeAgent.main import generate_readme_for_project

async def main():
    project_path = Path("/path/to/your/project")
    user_requirements = "README는 한국어로 작성하고, 설치/실행 방법을 예시 코드와 함께 꼭 포함해줘."
    result = await generate_readme_for_project(
        project_root=str(project_path),
        user_requirements=user_requirements,
        existing_readme_path=str(project_path / "README.md"),
    )
    print("✅ README 생성 완료")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 기술 스택
- **Python 3.11+**
- **LlamaIndex** – 에이전트와 워크플로우 구현
- **AsyncIO** – 비동기 흐름 관리
- **YAML** – 시스템 프롬프트 정의

## 기여 방법
1. Fork 후 새로운 브랜치를 생성합니다.
2. 기능 추가 또는 버그 수정을 진행합니다.
3. Pull Request를 열어 리뷰를 요청합니다.

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---
*이 README는 ReadmeAgent가 자동으로 생성한 초안이며, ReviewAgent가 최종 검수를 수행합니다.*