# ReadmeAgent

## 📖 프로젝트 개요
ReadmeAgent는 **LLM 기반 자동 README 생성 도구**입니다. 프로젝트 구조와 의존성을 분석하고, 사용자 요구사항에 맞춰 고품질의 README 파일을 자동으로 작성합니다. 주요 기능은 다음과 같습니다.

- 프로젝트 디렉터리 구조 탐색
- `requirements.txt` 를 기반으로 한 의존성 파악
- LangChain, LlamaIndex, Llama‑Cloud 등 최신 LLM 프레임워크와 연동
- 한국어를 포함한 다국어 README 지원
- 설치·실행 예시 자동 삽입

## 🛠️ 주요 기술 스택
- **Python 3.11+**
- **LangChain** (버전 0.3.x) – LLM 체인 구성 및 프롬프트 관리
- **LlamaIndex** (버전 0.13.x) – 문서 인덱싱 및 검색
- **Llama‑Cloud** – 클라우드 기반 LLM 서비스 연동
- **aiohttp, httpx** – 비동기 HTTP 클라이언트
- **SQLAlchemy** – 메타데이터 저장소
- **pydantic** – 설정 및 데이터 검증
- 그 외 다수의 유틸리티 라이브러리 (click, tqdm, pandas 등)

## 📦 설치 방법
```bash
# 1. 가상 환경 생성 (권장)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt
```
> **Tip**: `requirements.txt` 에는 최신 버전의 라이브러리가 명시되어 있으므로, `pip install -U pip` 후 설치하는 것이 좋습니다.

## 🚀 사용 예시
### 1. CLI 로 README 생성
```bash
# 프로젝트 루트 디렉터리에서 실행
python -m ReadmeAgent.cli \
    --project-root . \
    --output README_NEW.md \
    --language ko
```
- `--project-root` : 분석할 프로젝트 경로 (기본값 `.`)
- `--output`      : 생성된 README 파일 경로 (기본값 `README.md`)
- `--language`    : 출력 언어 (예: `ko`, `en`)

### 2. 파이썬 API 로 직접 호출
```python
from ReadmeAgent.main import generate_readme

readme_md = generate_readme(
    project_root='.',
    language='ko',
    include_examples=True
)
print(readme_md)
```

## 📂 프로젝트 구조 (핵심 파일)
```
ReadmeAgent/
├─ agents/                # FileViewer, Write, Review, Search 에이전트
├─ tools/                 # 각 에이전트가 사용하는 도구들
├─ utils/                 # 런타임 로깅 및 설정
├─ main.py                # 엔트리 포인트 (generate_readme 함수)
├─ cli.py                 # 커맨드라인 인터페이스 구현
├─ model.py               # 데이터 모델 정의 (pydantic 기반)
├─ configs.py             # 기본 설정 파일
├─ requirements.txt       # 프로젝트 의존성
└─ README.md              # 현재 파일
```

## 🤝 기여 방법
1. Fork 후 새로운 브랜치를 생성합니다.
2. 기능 추가·버그 수정 후 Pull Request 를 보냅니다.
3. 코드 스타일은 `black` 과 `isort` 로 자동 포맷팅합니다.
4. 테스트는 `pytest` 로 실행합니다.
```bash
pytest -v
```

## 📄 라이선스
이 프로젝트는 **MIT License** 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

---
*이 README는 ReadmeAgent가 자동으로 생성한 예시이며, 실제 프로젝트에 맞게 자유롭게 수정·보완할 수 있습니다.*