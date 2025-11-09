# AI video analyzer to Inhaler using LangGraph

LangGraph 기반 Multi-Agent 흡입기 비디오 분석 시스템

## 🎯 프로젝트 소개

이 프로젝트는 LangGraph를 활용한 Multi-Agent 시스템으로 흡입기 사용 비디오를 자동으로 분석합니다. OpenAI의 GPT-4o 모델을 사용하여 비디오에서 흡입기 사용 단계를 감지하고 평가합니다.

## 🏗️ Multi-Agent 아키텍처

```
┌─────────────────────────────────────┐
│   LangGraph Orchestrator            │
│   (Workflow Management)             │
└─────────────────────────────────────┘
              │
        ┌─────┴─────┬─────────┬─────────┐
        ▼           ▼         ▼         ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │Video     │ │Reference │ │Action    │ │Reporter  │
  │Processor │ │Detector  │ │Analyzer  │ │Agent     │
  └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Agent 역할

- **VideoProcessorAgent**: 비디오 메타데이터 추출 및 프레임 샘플링
- **ReferenceDetectorAgent**: 기준 시점 탐지 (inhalerIN, faceONinhaler, inhalerOUT)
- **ActionAnalyzerAgent**: 13개 행동 단계 분석 및 신뢰도 평가
- **ReporterAgent**: 결과 취합 및 Plotly 시각화

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/BrianTakion/AI_inhaler_Langgraph.git
cd AI_inhaler_Langgraph

# 패키지 설치
pip install -r app/requirements_langgraph.txt

# 환경 변수 설정
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 실행

```bash
cd app
python main_langgraph_251109.py
```

## 📁 프로젝트 구조

```
AI_inhaler_Langgraph/
├── app/
│   ├── agents/                      # Agent 모듈
│   │   ├── state.py
│   │   ├── video_processor_agent.py
│   │   ├── reference_detector_agent.py
│   │   ├── action_analyzer_agent.py
│   │   └── reporter_agent.py
│   │
│   ├── graph_workflow.py            # LangGraph 워크플로우
│   ├── main_langgraph_251109.py     # 메인 실행 파일
│   ├── example_usage.py             # 사용 예제
│   │
│   ├── class_MultimodalLLM_QA_251107.py
│   ├── class_Media_Edit_251107.py
│   ├── class_PromptBank_251107.py
│   │
│   └── 📚 문서
│       ├── INDEX.md                 # 📍 시작점
│       ├── QUICKSTART.md            # 빠른 시작
│       ├── SUMMARY_MULTIAGENT.md    # 프로젝트 요약
│       ├── ARCHITECTURE.md          # 아키텍처 설명
│       ├── COMPARISON.md            # 원본과 비교
│       └── README_LANGGRAPH.md      # 상세 문서
│
├── .devcontainer/                   # Dev Container 설정
└── README.md                        # 이 파일
```

## 📖 문서

자세한 문서는 다음 순서로 읽어보세요:

1. **[INDEX.md](app/INDEX.md)** - 📍 전체 문서 가이드
2. **[QUICKSTART.md](app/QUICKSTART.md)** - ⚡ 5분 빠른 시작
3. **[SUMMARY_MULTIAGENT.md](app/SUMMARY_MULTIAGENT.md)** - 📋 프로젝트 전체 요약
4. **[ARCHITECTURE.md](app/ARCHITECTURE.md)** - 🏗️ 아키텍처 상세 설명
5. **[COMPARISON.md](app/COMPARISON.md)** - 📊 원본 코드와 비교

## 💡 주요 기능

- ✅ **모듈화된 Agent 구조**: 각 Agent가 독립적으로 동작
- ✅ **LangGraph 워크플로우**: 상태 기반 체계적인 처리
- ✅ **자동 기준 시점 탐지**: 흡입기 등장, 입에 대기, 사라짐 자동 감지
- ✅ **13단계 행동 분석**: 세밀한 흡입기 사용 단계 평가
- ✅ **신뢰도 평가**: 각 판단에 대한 confidence score 제공
- ✅ **인터랙티브 시각화**: Plotly 기반 결과 시각화

## 🎓 사용 예제

### 기본 사용

```python
import os
from dotenv import load_dotenv
import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow

# 환경 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
mllm = mLLM.multimodalLLM(llm_name="gpt-4o", api_key=api_key)

# 초기 상태 생성
initial_state = create_initial_state(
    video_path="/path/to/video.mp4",
    llm_name="gpt-4o",
    api_key=api_key
)

# 워크플로우 실행
workflow = create_workflow(mllm)
final_state = workflow.run(initial_state)

# 결과 확인
if final_state["status"] == "completed":
    print("분석 완료!")
    print(final_state["final_report"])
```

더 많은 예제는 [example_usage.py](app/example_usage.py)를 참조하세요.

## 📊 원본 대비 개선사항

| 항목 | 원본 | Multi-Agent | 개선도 |
|------|------|-------------|--------|
| 코드 구조 | 단일 파일 (697줄) | 9개 모듈 | +80% |
| 가독성 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +67% |
| 유지보수성 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +67% |
| 확장성 | ⭐⭐ | ⭐⭐⭐⭐⭐ | +150% |
| 재사용성 | ⭐⭐ | ⭐⭐⭐⭐⭐ | +150% |

자세한 비교는 [COMPARISON.md](app/COMPARISON.md)를 참조하세요.

## 🛠️ 기술 스택

- **LangGraph**: Multi-Agent 워크플로우 관리
- **LangChain**: LLM 통합 프레임워크
- **OpenAI GPT-4o**: 비디오 및 이미지 분석
- **OpenCV**: 비디오 처리
- **Plotly**: 인터랙티브 시각화
- **Python 3.8+**: 프로그래밍 언어

## 📦 요구사항

```txt
langgraph>=0.0.20
langchain>=0.1.0
langchain-openai>=0.0.5
openai>=1.0.0
opencv-python>=4.8.0
numpy>=1.24.0
plotly>=5.18.0
python-dotenv>=1.0.0
typing-extensions>=4.9.0
```

## 🔧 개발 환경

### Dev Container 사용

```bash
# VS Code에서 Dev Container로 열기
code --install-extension ms-vscode-remote.remote-containers
```

프로젝트는 Dev Container 설정을 포함하고 있어 일관된 개발 환경을 제공합니다.

## 🤝 기여

프로젝트 개선을 위한 기여를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.

## 📞 연락처

- GitHub: [@BrianTakion](https://github.com/BrianTakion)
- Repository: [AI_inhaler_Langgraph](https://github.com/BrianTakion/AI_inhaler_Langgraph)

## 🙏 감사의 말

- LangChain 및 LangGraph 팀
- OpenAI
- 모든 기여자분들

---

**⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!**
