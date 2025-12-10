# ReadmeAgent

## 프로젝트 개요
ReadmeAgent는 **다중 에이전트 워크플로우**를 활용해 프로젝트 디렉터리를 자동으로 탐색하고, 사용자 요구사항에 맞는 고품질 README 파일을 생성·검수하는 시스템입니다.  
본 프로젝트는 다음 세 가지 에이전트로 구성됩니다:

| 에이전트 | 역할 |
|---|---|
| **FileViewerAgent** | 프로젝트 파일·디렉터리 구조를 탐색하고 정보를 수집 |
| **WriteAgent** | 수집된 정보를 바탕으로 README 초안을 작성 |
| **ReviewAgent** | 초안을 검토·수정하여 최종 README 완성 |

## 주요 기능
- 프로젝트 구조 자동 파악
- 사용자 요구사항(예: 한국어, 설치·실행 예제) 반영
- 다중 에이전트 협업을 통한 고품질 문서 생성
- 실패 시 자동 재시도 로직 포함

## 설치 방법
```bash
# 1. Python 3.9 이상 설치 (권장: 3.11)
python -V   # 확인
# 2. 가상 환경 생성 (선택)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.\.venv\Scripts\activate    # Windows
# 3. 의존성 설치
pip install -r requirements.txt
```

## 사용 예시
### 1. 프로젝트 디렉터리 구조 확인
```bash
tree -L 2 .
```
예시 출력:
```
.
├── agents
│   ├── __init__.py
│   ├── file_viewer_agent.py
│   ├── review_agent.py
│   └── write_agent.py
├── logs
│   ├── mcp_runtime.json
│   └── readme_agent.log
├── templates
│   └── agent_system_prompt.yaml
├── tools
│   ├── __init__.py
│   ├── file_viewer_tools.py
│   ├── mcp_server.py
│   ├── mcp_tool_registry.py
│   ├── review_readme_tool.py
│   ├── search_web_tool.py
│   └── write_readme_tool.py
├── .gitignore
├── cli.py
├── main.py
├── README.md
├── configs.py
├── model.py
└── requirements.txt
```

### 2. README 자동 생성
```bash
# 프로젝트 루트에서 실행
python -m ReadmeAgent.main --path .
```
또는 직접 `generate_readme_for_project` 함수를 호출:
```python
import asyncio
from main import generate_readme_for_project

async def run():
    result = await generate_readme_for_project(
        project_root=".",
        user_requirements="README는 한국어로 작성하고, 설치/실행 예제를 꼭 포함해주세요.",
        max_retries=3
    )
    print(result)

asyncio.run(run())
```

### 3. 결과 확인
위 명령을 실행하면 콘솔에 최종 README 내용이 출력되며, 필요 시 `README.md` 파일에 직접 저장할 수 있습니다.

## 프로젝트 구조
```
ReadmeAgent/
├─ agents/                # 에이전트 구현
│   ├─ file_viewer_agent.py
│   ├─ write_agent.py
│   └─ review_agent.py
├─ tools/                 # 에이전트가 사용하는 도구들
│   ├─ file_viewer_tools.py
│   ├─ write_readme_tool.py
│   └─ review_readme_tool.py
├─ templates/             # 시스템 프롬프트 템플릿
├─ logs/                  # 실행 로그
├─ utils/                 # 로깅·런타임 설정 유틸
├─ main.py                # 워크플로우 정의 및 실행 엔트리
├─ cli.py                 # 커맨드라인 인터페이스
├─ requirements.txt       # 의존성 목록
└─ README.md              # (이 파일)
```

## 기여 방법
1. Fork 저장소
2. 새로운 브랜치 생성 (`git checkout -b feature/your-feature`)
3. 코드 수정 및 테스트
4. Pull Request 제출

## 라이선스
이 프로젝트는 **MIT License** 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

---
*위 README는 WriteAgent가 자동으로 생성한 초안이며, ReviewAgent를 통해 최종 검수를 거칩니다.*