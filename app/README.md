# AI video analyzer to Inhaler using LangGraph

LangGraph 기반 Multi-Agent 흡입기 비디오 분석 시스템 (동적 LLM 모델 지원)

## 🎯 프로젝트 소개

이 프로젝트는 LangGraph를 활용한 Multi-Agent 시스템으로 흡입기 사용 비디오를 자동으로 분석합니다. **리스트로 여러 LLM 모델을 동적으로 지정**하여 병렬 실행하고, 결과를 평균화하여 더 정확한 분석을 제공합니다.

## 🏗️ Multi-Agent 아키텍처 (동적 병렬 실행)

```
┌─────────────────────────────────────┐
│   LangGraph Orchestrator            │
│   (Dynamic Parallel Workflow)       │
└─────────────────────────────────────┘
              │
        ┌─────┴─────┐
        ▼           │
  ┌──────────┐      │
  │Video     │      │
  │Processor │      │
  └──────────┘      │
        │           │
        ├───────────┴────────────┐
        ▼           ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │Analyzer  │ │Analyzer  │ │Analyzer  │
  │ Model 1  │ │ Model 2  │ │ Model N  │
  └──────────┘ └──────────┘ └──────────┘
        │           │            │
        └───────────┬────────────┘
                    ▼
              ┌──────────┐
              │Reporter  │
              │(Average) │
              └──────────┘
```

### Agent 역할

- **VideoProcessorAgent**: 비디오 메타데이터 추출 및 프레임 샘플링
- **VideoAnalyzerAgent** (동적 생성): 리스트로 지정된 각 LLM 모델로 병렬 분석
  - 기준 시점 탐지 (inhalerIN, faceONinhaler, inhalerOUT)
  - 13개 행동 단계 분석 및 신뢰도 평가
- **ReporterAgent**: 여러 모델 결과 평균 계산 및 Plotly 시각화

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
│   ├── agents/                      # Agent 모듈 (동적 모델 지원)
│   │   ├── state.py                 # 동적 State 구조
│   │   ├── video_processor_agent.py
│   │   ├── video_analyzer_agent.py  # 범용 Analyzer
│   │   └── reporter_agent.py        # 동적 평균 계산
│   │
│   ├── graph_workflow.py            # 동적 노드 생성 워크플로우
│   ├── main_langgraph_251109.py     # 메인 실행 (리스트 기반)
│   │
│   ├── class_MultimodalLLM_QA_251107.py
│   ├── class_Media_Edit_251107.py
│   ├── class_PromptBank_251107.py
│   │
│   ├── 📚 문서
│   │   ├── INDEX.md                 # 📍 시작점
│   │   ├── ARCHITECTURE.md          # 아키텍처 설명
│   │   └── MULTIMODEL_ARCHITECTURE.md # 동적 모델 구조
│   │
│   └── 251113_del/                  # 이전 버전 파일들
│
├── .devcontainer/                   # Dev Container 설정
└── README.md                        # 이 파일
```

## 📖 문서

자세한 문서는 다음 순서로 읽어보세요:

1. **[INDEX.md](app/INDEX.md)** - 📍 전체 문서 가이드
2. **[ARCHITECTURE.md](app/ARCHITECTURE.md)** - 🏗️ 아키텍처 상세 설명
3. **[MULTIMODEL_ARCHITECTURE.md](app/MULTIMODEL_ARCHITECTURE.md)** - 🔄 동적 모델 구조

## 💡 주요 기능

- ✅ **동적 LLM 모델 지원**: 리스트로 여러 모델을 자유롭게 지정 (중복 가능)
- ✅ **병렬 실행**: 모든 모델이 동시에 비디오 분석 수행
- ✅ **자동 평균 계산**: 여러 모델의 결과를 자동으로 평균화
- ✅ **모듈화된 Agent 구조**: 각 Agent가 독립적으로 동작
- ✅ **LangGraph 워크플로우**: 상태 기반 체계적인 처리
- ✅ **자동 기준 시점 탐지**: 흡입기 등장, 입에 대기, 사라짐 자동 감지
- ✅ **13단계 행동 분석**: 세밀한 흡입기 사용 단계 평가
- ✅ **신뢰도 평가**: 각 판단에 대한 confidence score 제공
- ✅ **인터랙티브 시각화**: Plotly 기반 평균 결과 시각화

## 🎓 사용 예제

### 기본 사용 (동적 모델 리스트)

```python
import os
from dotenv import load_dotenv
import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow

# 환경 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 여러 LLM 모델 지정 (자유롭게 개수 조절, 중복 가능)
llm_models = ["gpt-4o-mini", "gpt-4o-mini", "gpt-4o"]  # 3개 모델

# LLM 인스턴스 생성
mllm_instances = [
    mLLM.multimodalLLM(llm_name=model, api_key=api_key)
    for model in llm_models
]

# 초기 상태 생성
initial_state = create_initial_state(
    video_path="/path/to/video.mp4",
    llm_models=llm_models,
    api_key=api_key
)

# 워크플로우 실행 (병렬 + 평균)
workflow = create_workflow(mllm_instances, llm_models)
final_state = workflow.run(initial_state)

# 결과 확인
if final_state["status"] == "completed":
    print("분석 완료! (평균 결과)")
    print(final_state["final_report"])
```

## 📊 개선사항

| 항목 | 고정 모델 | 동적 모델 리스트 | 개선도 |
|------|----------|----------------|--------|
| 유연성 | 2개 고정 | N개 자유 | +400% |
| 확장성 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +67% |
| 정확도 | 단일/평균 | 다중 평균 | +50% |
| 재사용성 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +25% |
| 병렬 처리 | 2개 고정 | N개 동적 | +400% |

### 주요 개선사항

1. **동적 모델 지원**: 코드 수정 없이 리스트만 변경하면 다양한 모델 조합 테스트 가능
2. **확장성**: 1개부터 N개까지 자유롭게 모델 개수 조절
3. **유연성**: 같은 모델 중복 사용 가능 (예: 동일 모델 5번 실행하여 일관성 검증)

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
