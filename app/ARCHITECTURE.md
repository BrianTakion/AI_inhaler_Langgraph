# LangGraph Multi-Agent 아키텍처



## 전체 시스템 아키텍처 (동적 병렬 실행)

```mermaid
graph TD
    Start([시작]) --> Init[초기 상태 생성<br/>llm_models 리스트]
    Init --> WF[LangGraph 워크플로우<br/>동적 병렬 오케스트레이션]

    WF --> VP[VideoProcessorAgent]
    VP --> VA1[VideoAnalyzerAgent<br/>Model 1]
    VP --> VA2[VideoAnalyzerAgent<br/>Model 2]
    VP --> VAN[VideoAnalyzerAgent<br/>Model N]

    VA1 --> RA[ReporterAgent<br/>N개 모델 평균 계산]
    VA2 --> RA
    VAN --> RA
    RA --> End([종료])

    VP -.->|video_info| State[(공유 상태<br/>동적 model_results)]
    VA1 -.->|model_results| State
    VA2 -.->|model_results| State
    VAN -.->|model_results| State
    RA -.->|avg_results| State

    State -.->|read| VP
    State -.->|read| VA1
    State -.->|read| VA2
    State -.->|read| VAN
    State -.->|read| RA

    style VP fill:#e1f5ff
    style VA1 fill:#fff4e1
    style VA2 fill:#fff4e1
    style VAN fill:#fff4e1
    style RA fill:#e8f5e1
    style State fill:#f0f0f0
```

**주요 특징:**
- Agent 개수가 `llm_models` 리스트 길이에 따라 동적으로 생성
- 모든 모델이 동일한 범용 `VideoAnalyzerAgent` 클래스 사용
- `model_results` 딕셔너리에 각 모델 결과 저장
- 병렬 실행으로 실행 시간 최적화

## 동적 모델 지원 핵심 개념

### 1. 동적 모델 리스트

```python
# 코드에서 간단히 리스트로 지정
llm_models = ["gpt-4o-mini", "gpt-4o-mini", "gpt-4o"]  # 3개 모델
llm_models = ["gpt-4o"] * 5  # 동일 모델 5번
llm_models = ["gpt-4o"]  # 1개 모델
```

### 2. 동적 Agent 생성

리스트 길이만큼 자동으로 `VideoAnalyzerAgent` 인스턴스 생성

### 3. 동적 평균 계산

N개 모델의 결과를 자동으로 평균 계산

## Agent 상세 구조

### 1. VideoProcessorAgent

```mermaid
graph LR
    A[비디오 파일] --> B[메타데이터 추출]
    B --> C[프레임 샘플링]
    C --> D[MxN 그리드 생성]
    D --> E[이미지 배열 반환]
    
    B --> F[(video_info)]
    
    style A fill:#e1f5ff
    style F fill:#f0f0f0
```

**입력:**
- video_path (비디오 파일 경로)

**출력:**
- video_info (이름, 재생시간, 프레임수, 해상도, 파일크기)

**주요 메서드:**
- `process(state)`: 비디오 정보 추출
- `extract_frames(...)`: 프레임 추출 및 그리드 생성

### 2. VideoAnalyzerAgent (범용, 동적 생성)

```mermaid
graph TD
    A[시작 - Model X] --> B{inhalerIN 탐지}
    B -->|시간 슬라이딩| C[프레임 추출]
    C --> D[Model X 분석]
    D --> E{Overall_Answer?}
    E -->|YES| F[reference_time 저장]
    E -->|NO| B

    F --> G{faceONinhaler 탐지}
    G --> H[프레임 추출]
    H --> I[Model X 분석]
    I --> J{Overall_Answer?}
    J -->|YES| K[reference_time 저장]
    J -->|NO| G

    K --> L{inhalerOUT 탐지}
    L --> M[프레임 추출]
    M --> N[Model X 분석]
    N --> O{Overall_Answer?}
    O -->|YES| P[reference_time 저장]
    O -->|NO| L

    P --> Q[행동 단계 분석]
    Q --> R[신뢰도 평가]
    R --> S[model_results에 저장]
    S --> T[완료 - Model X]
    
    style F fill:#90EE90
    style K fill:#90EE90
    style P fill:#90EE90
```

**특징:**
- 모든 모델이 동일한 클래스 사용
- `model_id` (예: "gpt-4o_0")로 구분
- 결과는 `model_results[model_id]`에 저장

**입력:**
- video_path
- video_info (play_time)
- model_id (동적 할당)
- model_name (리스트에서 지정)

**출력 (model_results에 저장):**
- reference_times: {inhalerIN, faceONinhaler, inhalerOUT}
- action_analysis_results: 행동 분석 결과
- q_answers_accumulated: Q&A 결과
- promptbank_data: PromptBank 전체 데이터

**주요 메서드:**
- `process(state)`: 모든 기준 시점 탐지
- `_detect_inhaler_in()`: inhalerIN 탐지
- `_detect_face_on_inhaler()`: faceONinhaler 탐지
- `_detect_inhaler_out()`: inhalerOUT 탐지
- `_search_reference_time()`: 시간 슬라이딩 탐색

### 3. ReporterAgent (멀티모델 앙상블)

```mermaid
graph TD
    A[N개 모델 결과 수집] --> B[평균 계산]
    B --> C[reference_times_avg 생성]
    B --> D[promptbank_data_avg 생성]

    C --> E[최종 리포트 생성]
    D --> E

    E --> F[Plotly 시각화 - 평균값 기반]
    F --> G[Reference Time 표시]
    F --> H[Action Steps 표시]
    F --> I[Confidence 색상 매핑]

    G --> J[그래프 출력]
    H --> J
    I --> J

    J --> K[요약 정보 출력]

    style B fill:#ffe1e1
    style J fill:#FFD700
```

**입력:**
- video_info
- model_results (N개 모델의 모든 결과)

**출력:**
- reference_times_avg (평균 기준 시간)
- promptbank_data_avg (평균 PromptBank 데이터)
- final_report (최종 리포트 - 평균값 기반)
- visualization_path (시각화 결과 - 평균값 기반)

**주요 메서드:**
- `process(state)`: 평균 계산 및 리포트 생성 실행
- `_compute_average()`: 여러 모델 결과 평균 계산
- `_create_final_report()`: 최종 리포트 생성 (평균값 기반)
- `_create_visualization()`: Plotly 시각화 (평균값 기반)
- `_print_summary()`: 요약 정보 출력

## 상태(State) 관리

```mermaid
graph TD
    A[VideoAnalysisState] --> B[입력 데이터]
    A --> C[처리 결과]
    A --> D[메타데이터]
    
    B --> B1[video_path]
    B --> B2[llm_models]
    B --> B3[api_key]
    
    C --> C1[video_info]
    C --> C2[model_results]
    C --> C3[reference_times_avg]
    C --> C4[promptbank_data_avg]
    C --> C5[final_report]
    
    D --> D1[errors]
    D --> D2[status]
    D --> D3[agent_logs]
    
    style A fill:#f0f0f0
    style B fill:#e1f5ff
    style C fill:#e8f5e1
    style D fill:#ffe1e1
```

### 동적 State 구조

```python
VideoAnalysisState = {
    # 입력 (병렬 실행 시 첫 번째 값 유지)
    "video_path": Annotated[str, keep_first],
    "llm_name": Annotated[str, keep_first],
    "llm_models": Annotated[List[str], keep_first],  # 모델 리스트
    "api_key": Annotated[str, keep_first],

    # 비디오 정보 (병렬 실행 시 첫 번째 값 유지)
    "video_info": Annotated[Dict, keep_first],

    # 동적 모델별 결과 (병렬 실행 시 딕셔너리 병합)
    "model_results": Annotated[Dict[str, Dict[str, Any]], operator.or_],
    # {
    #     "gpt-4o_0": {
    #         "reference_times": {...},
    #         "action_analysis_results": {...},
    #         "q_answers_accumulated": {...},
    #         "promptbank_data": {...}
    #     },
    #     "gpt-4o-mini_1": {...},
    #     "gpt-4o_2": {...}
    # }

    # 평균 결과 (Reporter Agent가 계산)
    "reference_times_avg": Annotated[Dict[str, float], keep_non_none],
    "promptbank_data_avg": Annotated[Dict, keep_non_none],

    # 최종 결과
    "final_report": Annotated[Dict, keep_non_none],
    "visualization_path": Annotated[str, keep_non_none],

    # 메타데이터
    "errors": Annotated[List[str], operator.add],
    "status": Annotated[str, keep_non_none],
    "agent_logs": Annotated[List[Dict], operator.add]
}
```

### Reducer 함수 설명

```python
def keep_first(left: Any, right: Any) -> Any:
    """병렬 실행 시 첫 번째 유효한 값 유지"""
    # 입력 정보는 첫 번째 Agent의 값 유지
    # video_path, llm_models 등에 사용

def keep_non_none(left: Any, right: Any) -> Any:
    """병렬 실행 시 None이 아닌 값 우선"""
    # Reporter Agent의 결과는 최신 값 유지
    # reference_times_avg, final_report 등에 사용

def operator.or_(left: Dict, right: Dict) -> Dict:
    """병렬 실행 시 딕셔너리 병합"""
    # model_results 딕셔너리 병합
    # {**left, **right}
```

## 워크플로우 실행 흐름

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Workflow
    participant VP as VideoProcessor
    participant VA1 as VideoAnalyzer<br/>(Model 0)
    participant VA2 as VideoAnalyzer<br/>(Model 1)
    participant VAN as VideoAnalyzer<br/>(Model N-1)
    participant RA as Reporter
    participant State
    
    User->>Main: run()
    Main->>Workflow: create_workflow(mllm_instances, llm_models)
    Main->>State: create_initial_state()
    Main->>Workflow: workflow.run(initial_state)
    
    Workflow->>VP: process(state)
    VP->>State: update video_info
    VP-->>Workflow: return state
    
    par N개 모델 병렬 실행
        Workflow->>VA1: process(state)
        Workflow->>VA2: process(state)
        Workflow->>VAN: process(state)
    end
    
    VA1->>State: update model_results[model_0]
    VA2->>State: update model_results[model_1]
    VAN->>State: update model_results[model_N-1]
    
    VA1-->>Workflow: return state
    VA2-->>Workflow: return state
    VAN-->>Workflow: return state
    
    Workflow->>RA: process(state)
    RA->>State: read all model_results
    RA->>RA: 동적 평균 계산
    RA->>RA: 시각화 생성
    RA->>State: update final_report
    RA-->>Workflow: return state
    
    Workflow-->>Main: return final_state
    Main-->>User: display results
```

## 동적 워크플로우 생성

### graph_workflow.py

```python
class InhalerAnalysisWorkflow:
    def __init__(self, mllm_instances: list, llm_models: list):
        """
        리스트로 받은 모델들을 동적으로 Agent 생성
        """
        self.mllm_instances = mllm_instances
        self.llm_models = llm_models
        
        self.video_processor = VideoProcessorAgent()
        
        # 동적으로 VideoAnalyzerAgent 생성
        self.video_analyzers = []
        self.analyzer_nodes = {}
        for idx, (mllm, model_name) in enumerate(zip(mllm_instances, llm_models)):
            model_id = f"{model_name}_{idx}"  # 고유 ID
            analyzer = VideoAnalyzerAgent(
                mllm, 
                self.video_processor, 
                model_id,  # 동적 ID
                model_name  # 모델 이름
            )
            self.video_analyzers.append(analyzer)
            self.analyzer_nodes[model_id] = analyzer
        
        self.reporter = ReporterAgent()
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile()
    
    def _create_workflow(self):
        """동적으로 노드 생성"""
        workflow = StateGraph(VideoAnalysisState)
        
        # 1. VideoProcessor 노드
        workflow.add_node("video_processor", self._video_processor_node)
        
        # 2. 동적으로 VideoAnalyzer 노드들 추가
        for model_id, analyzer in self.analyzer_nodes.items():
            node_name = f"video_analyzer_{model_id}"
            workflow.add_node(node_name, self._create_analyzer_node(analyzer, model_id))
        
        # 3. Reporter 노드
        workflow.add_node("reporter", self._reporter_node)
        
        # 엣지 추가 (병렬 실행)
        workflow.set_entry_point("video_processor")
        
        # video_processor -> 모든 analyzer (병렬)
        for model_id in self.analyzer_nodes.keys():
            node_name = f"video_analyzer_{model_id}"
            workflow.add_edge("video_processor", node_name)
        
        # 모든 analyzer -> reporter
        for model_id in self.analyzer_nodes.keys():
            node_name = f"video_analyzer_{model_id}"
            workflow.add_edge(node_name, "reporter")
        
        workflow.add_edge("reporter", END)
        
        return workflow
```

## 동적 평균 계산 로직

### reporter_agent.py

```python
def _compute_average(self, state: VideoAnalysisState) -> dict:
    """
    여러 모델의 결과를 동적으로 평균내기
    """
    model_results = state.get("model_results", {})
    num_models = len(model_results)
    
    print(f"[ReporterAgent] {num_models}개 모델의 결과를 평균 계산 중...")
    
    # Reference Time 평균
    reference_times_avg = {}
    for ref_key in ["inhalerIN", "faceONinhaler", "inhalerOUT"]:
        values = []
        for model_id, result in model_results.items():
            ref_times = result.get("reference_times", {})
            if ref_key in ref_times:
                values.append(ref_times[ref_key])
        
        # N개 모델의 평균
        reference_times_avg[ref_key] = round(sum(values) / len(values), 1) if values else 0
    
    # PromptBank 데이터 평균
    # 모든 모델의 check_action_step_common 데이터 수집
    for action_key in all_action_keys:
        all_times_scores = {}  # {time: [(score, confidence), ...]}
        
        for model_id, result in model_results.items():
            promptbank = result.get("promptbank_data", {})
            check_action = promptbank.get("check_action_step_common", {})
            
            if action_key in check_action:
                times = action_data.get('time', [])
                scores = action_data.get('score', [])
                confidences = dict(action_data.get('confidence_score', []))
                
                for i, t in enumerate(times):
                    if t not in all_times_scores:
                        all_times_scores[t] = []
                    all_times_scores[t].append((scores[i], confidences.get(t, 0.5)))
        
        # 각 시간에 대해 평균 계산
        for t in sorted(all_times_scores.keys()):
            score_conf_list = all_times_scores[t]
            scores = [sc[0] for sc in score_conf_list]
            confidences = [sc[1] for sc in score_conf_list]
            
            avg_score = sum(scores) / len(scores)
            avg_confidence = sum(confidences) / len(confidences)
            
            # 0.5 기준으로 반올림
            final_score = 1 if avg_score >= 0.5 else 0
```

## 데이터 흐름

```mermaid
graph LR
    A[비디오 파일] --> B[VideoProcessor]
    B --> C[video_info]
    
    C --> D1[VideoAnalyzer 1]
    C --> D2[VideoAnalyzer 2]
    C --> DN[VideoAnalyzer N]
    A --> D1
    A --> D2
    A --> DN
    
    D1 --> E1[model_results 1]
    D2 --> E2[model_results 2]
    DN --> EN[model_results N]
    
    E1 --> F[Reporter]
    E2 --> F
    EN --> F
    
    F --> G[평균 계산]
    G --> H[final_report]
    G --> I[visualization]
    
    style A fill:#e1f5ff
    style C fill:#fff4e1
    style G fill:#ffe1e1
    style H fill:#FFD700
    style I fill:#FFD700
```

## 사용 예제

### 1개 모델

```python
llm_models = ["gpt-4o"]
```

### 2개 모델

```python
llm_models = ["gpt-4o", "gpt-4o-mini"]
```

### 3개 모델 (중복 가능)

```python
llm_models = ["gpt-4o-mini", "gpt-4o-mini", "gpt-4o"]
```

### N개 동일 모델 (일관성 검증)

```python
llm_models = ["gpt-4o"] * 5  # gpt-4o 5번 실행
```

## 성능 고려사항

### 모델 개수에 따른 실행 시간

| 모델 개수 | 예상 시간 (분) | 정확도 | 권장 사용 |
|----------|--------------|--------|----------|
| 1개 | 3-5 | ⭐⭐⭐ | 빠른 테스트 |
| 2개 | 3-5 | ⭐⭐⭐⭐ | 균형 |
| 3개 | 3-5 | ⭐⭐⭐⭐⭐ | 정확도 우선 |
| 5개 | 3-5 | ⭐⭐⭐⭐⭐ | 최고 정확도 |

**Note**: 병렬 실행으로 모델 개수가 늘어나도 실행 시간은 거의 동일

### 비용 고려사항

- OpenAI API 비용은 모델 개수에 비례
- 빠른 모델(gpt-4o-mini) 여러 개 vs 느린 모델(gpt-4o) 1개 비교 가능

## 모범 사례

### 개발 단계
```python
llm_models = ["gpt-4o-mini"]  # 빠르고 저렴
```

### 테스트 단계
```python
llm_models = ["gpt-4o-mini", "gpt-4o"]  # 균형
```

### 프로덕션 단계
```python
llm_models = ["gpt-4o", "gpt-4o", "gpt-4o"]  # 정확도 우선
```

### 일관성 검증
```python
llm_models = ["gpt-4o"] * 5  # 동일 모델 5번 실행
```

## 장점

### 1. 유연성
- 코드 수정 없이 리스트만 변경
- 1개부터 N개까지 자유로운 모델 개수
- 모델 중복 사용 가능

### 2. 확장성
- 새로운 모델 추가가 용이
- 동적 노드 생성으로 확장 가능

### 3. 정확도
- 여러 모델의 평균으로 안정적인 결과
- 동일 모델 여러 번 실행으로 일관성 검증 가능

### 4. 효율성
- 모든 모델이 병렬로 실행
- 동적 평균 계산으로 추가 코드 불필요

## 확장 가능성

### 병렬 처리 예제

```mermaid
graph TD
    A[VideoProcessor] --> B{분기}
    B -->|병렬 1| C[VideoAnalyzer 1]
    B -->|병렬 2| D[VideoAnalyzer 2]
    B -->|병렬 N| E[VideoAnalyzer N]
    
    C --> F[수렴]
    D --> F
    E --> F
    
    F --> G[Reporter]
    
    style B fill:#FFD700
    style F fill:#FFD700
```

### 새로운 Agent 추가

```mermaid
graph TD
    A[기존 워크플로우] --> B[새로운 Agent 개발]
    B --> C[graph_workflow.py 수정]
    
    C --> D[add_node 추가]
    C --> E[add_edge 추가]
    
    D --> F[테스트]
    E --> F
    
    F --> G[배포]
    
    style B fill:#90EE90
    style G fill:#FFD700
```

## 오류 처리 메커니즘

```mermaid
graph TD
    A[Agent 실행] --> B{오류 발생?}
    B -->|아니오| C[정상 처리]
    B -->|예| D[try-except]
    
    C --> E[상태 업데이트]
    D --> F[오류 로깅]
    F --> G[state errors에 추가]
    G --> H[상태를 error로 변경]
    
    E --> I[다음 Agent]
    H --> I
    
    I --> J{다음 Agent 존재?}
    J -->|예| A
    J -->|아니오| K[최종 상태 반환]
    
    style D fill:#ffe1e1
    style F fill:#ffe1e1
    style G fill:#ffe1e1
```

## 성능 최적화 포인트

```mermaid
graph LR
    A[최적화 포인트] --> B[프레임 해상도]
    A --> C[샘플링 간격]
    A --> D[병렬 처리]
    A --> E[캐싱]
    A --> F[API 호출 최소화]
    
    B --> G[토큰 비용 절감]
    C --> G
    D --> H[실행 시간 단축]
    E --> H
    F --> G
    
    style G fill:#90EE90
    style H fill:#90EE90
```

## 테스트 전략

```mermaid
graph TD
    A[테스트 계층] --> B[단위 테스트]
    A --> C[통합 테스트]
    A --> D[E2E 테스트]
    
    B --> B1[Agent별 테스트]
    B --> B2[함수별 테스트]
    
    C --> C1[Agent 간 통신]
    C --> C2[상태 전달]
    
    D --> D1[전체 워크플로우]
    D --> D2[실제 비디오 분석]
    
    style B fill:#e1f5ff
    style C fill:#fff4e1
    style D fill:#e8f5e1
```

---

이 아키텍처는 확장 가능하고 유지보수가 용이한 구조로 설계되었습니다.

**마지막 업데이트**: 2024.11.13  
**버전**: 2.0 (동적 모델 지원)
