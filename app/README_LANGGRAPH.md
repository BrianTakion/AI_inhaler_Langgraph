# LangGraph 기반 Multi-Agent 흡입기 비디오 분석기

## 개요

이 프로젝트는 LangGraph를 활용한 Multi-Agent 시스템으로 흡입기 사용 비디오를 자동 분석합니다.

## 아키텍처

### Multi-Agent 구조

```
┌─────────────────────────────────────┐
│   Orchestrator (LangGraph)           │
│   - 전체 워크플로우 관리              │
│   - Agent 간 상태 전달                │
└─────────────────────────────────────┘
              ├─────────┬─────────┬─────────┐
              ▼         ▼         ▼         ▼
        ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
        │Video    │ │Reference│ │Action   │ │Reporter │
        │Processor│ │Detector │ │Analyzer │ │Agent    │
        │Agent    │ │Agent    │ │Agent    │ │         │
        └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### Agent 역할

1. **VideoProcessorAgent**: 비디오 메타데이터 추출 및 프레임 샘플링
2. **ReferenceDetectorAgent**: 기준 시점 탐지 (inhalerIN, faceONinhaler, inhalerOUT)
3. **ActionAnalyzerAgent**: 개별 행동 단계 분석 및 신뢰도 평가
4. **ReporterAgent**: 결과 취합 및 시각화

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

# LLM 초기화
mllm = mLLM.multimodalLLM(llm_name="gpt-4o", api_key=api_key)

# 초기 상태 생성
initial_state = create_initial_state(
    video_path="/path/to/video.mp4",
    llm_name="gpt-4o",
    api_key=api_key
)

# 워크플로우 생성 및 실행
workflow = create_workflow(mllm)
final_state = workflow.run(initial_state)

# 결과 확인
if final_state["status"] == "completed":
    print("분석 완료!")
    print(final_state["final_report"])
```

## 파일 구조

```
app/
├── agents/                          # Agent 모듈
│   ├── __init__.py
│   ├── state.py                     # 공유 상태 정의
│   ├── video_processor_agent.py     # 비디오 처리 Agent
│   ├── reference_detector_agent.py  # 기준 시점 탐지 Agent
│   ├── action_analyzer_agent.py     # 행동 분석 Agent
│   └── reporter_agent.py            # 리포팅 Agent
├── graph_workflow.py                # LangGraph 워크플로우 정의
├── main_langgraph_251109.py         # 메인 실행 파일
├── class_MultimodalLLM_QA_251107.py # LLM 래퍼 클래스
├── class_Media_Edit_251107.py       # 비디오 편집 유틸리티
├── class_PromptBank_251107.py       # 프롬프트 뱅크
├── requirements_langgraph.txt       # 패키지 요구사항
└── README_LANGGRAPH.md              # 이 파일
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

4. **테스트**
   - Agent별 단위 테스트 가능
   - 전체 워크플로우 통합 테스트 가능

5. **디버깅**
   - Agent별 로그 추적
   - 상태 기반 디버깅

## 성능 고려사항

- **병렬 처리**: 현재는 순차 실행, 향후 병렬 처리 가능
- **메모리 효율**: 비디오 프레임을 메모리에 로드하지 않고 필요시에만 추출
- **API 비용**: LLM 호출 최소화 전략 적용 가능

## 향후 개선 방향

1. **병렬 처리**: 여러 행동 단계를 동시에 분석
2. **캐싱**: 반복적인 프레임 추출 결과 캐싱
3. **Quality Validator Agent**: 낮은 신뢰도 구간 재분석
4. **적응형 샘플링**: 중요한 구간은 더 세밀하게 분석
5. **A/B 테스팅**: 여러 전략 동시 비교

## 문의

문제가 발생하거나 개선 제안이 있으시면 이슈를 등록해주세요.

