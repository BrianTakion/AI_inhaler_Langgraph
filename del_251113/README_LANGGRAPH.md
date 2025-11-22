# LangGraph 기반 Multi-Agent 흡입기 비디오 분석기

## 개요

이 프로젝트는 LangGraph를 활용한 Multi-Agent 시스템으로 흡입기 사용 비디오를 자동 분석합니다. **GPT-4o와 GPT-4o-mini 두 모델을 병렬로 실행**하여 분석 정확도를 향상시키고 결과를 평균내어 안정적인 분석 결과를 제공합니다.

## 아키텍처

### 병렬 Multi-Agent 구조

```
┌─────────────────────────────────────┐
│   Orchestrator (LangGraph)           │
│   - 전체 워크플로우 관리              │
│   - Agent 간 상태 전달                │
│   - 병렬 실행 및 결과 평균화          │
└─────────────────────────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │VideoProcessor│
            │Agent         │
            └──────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
    ┌──────────────┐ ┌──────────────┐
    │VideoAnalyzer │ │VideoAnalyzer │
    │Agent (GPT-4o)│ │Agent(GPT-4o-│
    │              │ │mini)        │
    └──────────────┘ └──────────────┘
            │               │
            └───────┬───────┘
                    ▼
            ┌──────────────┐
            │   Reporter   │
            │   Agent      │
            │ (평균 계산 + │
            │ 시각화)      │
            └──────────────┘
```

### Agent 역할

1. **VideoProcessorAgent**: 비디오 메타데이터 추출 및 프레임 샘플링
2. **VideoAnalyzerAgent4o**: GPT-4o를 사용한 기준 시점 탐지 및 행동 단계 분석
3. **VideoAnalyzerAgent4oMini**: GPT-4o-mini를 사용한 기준 시점 탐지 및 행동 단계 분석
4. **ReporterAgent**: 두 모델의 결과 평균 계산 및 시각화

## 설치

```bash
# 패키지 설치
pip install -r requirements_langgraph.txt

# 환경 변수 설정
# .env 파일에 OPENAI_API_KEY 추가
echo "OPENAI_API_KEY=your-api-key" > .env
```

## 사용법

### 기본 실행

```bash
python main_langgraph_251109.py
```

이 명령어는 **GPT-4o와 GPT-4o-mini를 병렬로 실행**하여 비디오를 분석하고 결과를 평균내어 시각화합니다.

### 프로그래밍 방식으로 사용

```python
import os
from dotenv import load_dotenv
import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 두 개의 LLM 모델 초기화 (병렬 실행용)
mllm_4o = mLLM.multimodalLLM(llm_name="gpt-4o", api_key=api_key)
mllm_4o_mini = mLLM.multimodalLLM(llm_name="gpt-4o-mini", api_key=api_key)

# 초기 상태 생성
initial_state = create_initial_state(
    video_path="/path/to/video.mp4",
    llm_name="gpt-4o & gpt-4o-mini",
    api_key=api_key
)

# 워크플로우 생성 및 실행 (두 모델 전달)
workflow = create_workflow(mllm_4o, mllm_4o_mini)
final_state = workflow.run(initial_state)

# 결과 확인
if final_state["status"] == "completed":
    print("분석 완료!")
    print(final_state["final_report"])  # 평균 결과 출력
```

## 파일 구조

```
app/
├── agents/                              # Agent 모듈
│   ├── __init__.py                      # 패키지 초기화
│   ├── state.py                         # 공유 상태 정의 (병렬 처리용 reducer 포함)
│   ├── video_processor_agent.py         # 비디오 처리 Agent
│   ├── video_analyzer_agent_4o.py       # GPT-4o 비디오 분석 Agent
│   ├── video_analyzer_agent_4o_mini.py  # GPT-4o-mini 비디오 분석 Agent
│   └── reporter_agent.py                # 리포팅 Agent (평균 계산 + 시각화)
├── graph_workflow.py                    # LangGraph 워크플로우 정의 (병렬 실행)
├── main_langgraph_251109.py             # 메인 실행 파일 (병렬 처리)
├── class_MultimodalLLM_QA_251107.py     # LLM 래퍼 클래스
├── class_Media_Edit_251107.py           # 비디오 편집 유틸리티
├── class_PromptBank_251107.py           # 프롬프트 뱅크
├── requirements_langgraph.txt           # 패키지 요구사항
├── video_source/                        # 비디오 데이터
├── 251113_del/                         # 관련 없는 파일들 (삭제 예정)
└── README_LANGGRAPH.md                  # 이 파일
```

## 주요 기능

### 1. 모듈성
- 각 Agent는 독립적으로 개발/테스트 가능
- Agent 교체 및 업그레이드 용이

### 2. 상태 관리
- LangGraph의 TypedDict 기반 상태 관리
- Agent 간 안전한 데이터 전달

### 3. 확장성
- 새로운 Agent 추가 용이
- 워크플로우 수정 간편

### 4. 오류 처리
- Agent별 오류 격리
- 부분 결과 활용 가능

### 5. 시각화
- Plotly 기반 인터랙티브 그래프
- 기준 시점 및 행동 단계 시각화

## 장점

### 병렬 처리의 이점

1. **향상된 정확도**: GPT-4o와 GPT-4o-mini의 결과를 평균하여 더 안정적인 분석 결과
2. **속도 최적화**: 두 모델이 동시에 실행되어 분석 시간 단축
3. **Robustness**: 하나의 모델이 실패해도 다른 모델의 결과로 분석 가능

### 원본 대비 개선사항

1. **코드 구조**
   - 모듈화: 각 Agent가 독립적인 파일
   - 재사용성: Agent를 다른 프로젝트에서도 활용 가능

2. **유지보수**
   - 각 Agent별로 독립적인 수정 가능
   - 명확한 책임 분리

3. **확장성**
   - 새로운 흡입기 타입 추가 용이
   - 새로운 행동 단계 추가 간편
   - 새로운 LLM 모델 추가 용이

4. **테스트**
   - Agent별 단위 테스트 가능
   - 전체 워크플로우 통합 테스트 가능

5. **디버깅**
   - Agent별 로그 추적
   - 상태 기반 디버깅

## 성능 고려사항

- **병렬 처리**: ✅ **구현 완료** - GPT-4o와 GPT-4o-mini가 동시에 실행되어 분석 시간 단축
- **메모리 효율**: 비디오 프레임을 메모리에 로드하지 않고 필요시에만 추출
- **API 비용**: 두 모델의 결과를 평균하여 비용 효율성 향상
- **정확도 향상**: 멀티모델 앙상블을 통한 분석 결과 안정화

## 향후 개선 방향

1. **추가 모델 통합**: o1, Claude 등 더 다양한 모델 병렬 실행
2. **캐싱**: 반복적인 프레임 추출 결과 캐싱
3. **Quality Validator Agent**: 낮은 신뢰도 구간 재분석
4. **적응형 샘플링**: 중요한 구간은 더 세밀하게 분석
5. **동적 모델 선택**: 작업 난이도에 따라 모델 자동 선택
6. **실시간 분석**: 스트리밍 비디오 실시간 분석 기능

## 문의

문제가 발생하거나 개선 제안이 있으시면 이슈를 등록해주세요.

