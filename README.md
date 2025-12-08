# ReadmeAgent

## 📖 프로젝트 소개
ReadmeAgent는 **AI 기반 자동 README 생성 도구**입니다. 프로젝트 디렉터리를 분석하고, 파일 구조와 코드 내용을 바탕으로 고품질의 README.md 파일을 자동으로 작성합니다. 이 도구는 다음과 같은 핵심 기능을 제공합니다.

- **파일 탐색 및 분석**: 프로젝트 루트에서 파일을 탐색하고, 주요 코드와 설정을 추출합니다.
- **다중 에이전트 워크플로우**: `FileViewerAgent`, `SearchAgent`, `WriteAgent`, `ReviewAgent` 등 여러 에이전트가 순차적으로 협업하여 README를 완성합니다.
- **다국어 지원**: 현재 한국어와 영어를 기본으로 지원하며, 필요에 따라 다른 언어도 쉽게 추가할 수 있습니다.
- **예시 코드 자동 삽입**: 프로젝트 사용 예시를 자동으로 생성해 README에 포함합니다.

## 🛠️ 주요 구성 요소
| 디렉터리/파일 | 역할 |
|---|---|
| `agents/` | 각 에이전트(`FileViewerAgent`, `SearchAgent`, `WriteAgent`, `ReviewAgent`) 구현 |
| `tools/` | 에이전트가 사용하는 도구(`write_readme_tool`, `search_web_tool` 등) |
| `templates/` | README 템플릿 및 프롬프트 파일 |
| `main.py` | 프로그램 진입점, 에이전트 파이프라인 실행 |
| `cli.py` | 커맨드라인 인터페이스 제공 |
| `requirements.txt` | 프로젝트 의존성 목록 |
| `README.md` | 현재 파일 (자동 생성 대상) |

## 📦 설치 방법
```bash
# 1. 프로젝트 클론
git clone https://github.com/yourusername/ReadmeAgent.git
cd ReadmeAgent

# 2. 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. (선택) 패키지 형태로 설치
pip install -e .
```

## 🚀 실행 방법 및 예시 코드
### 1. 기본 사용법 (CLI)
```bash
# 프로젝트 루트에서 실행
python -m ReadmeAgent
```
위 명령을 실행하면 `README.md` 파일이 자동으로 생성·업데이트됩니다.

### 2. 파이썬 코드에서 직접 호출
```python
from ReadmeAgent.main import generate_readme

# 프로젝트 루트 경로 지정
project_root = "/path/to/your/project"

# README 생성 (기존 파일을 덮어씁니다)
generate_readme(project_root)
```

## 🧪 테스트 및 검증
```bash
# pytest 로 테스트 실행 (테스트 코드가 포함된 경우)
pytest
```

## 🤝 기여 방법
1. Fork 후 새로운 브랜치를 생성합니다.
2. 기능 추가 또는 버그 수정을 진행합니다.
3. PR을 열어 리뷰를 요청합니다.

## 📄 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

---
*이 README는 `WriteAgent`가 자동으로 생성했으며, `ReviewAgent`를 통해 최종 검수를 거쳤습니다.*