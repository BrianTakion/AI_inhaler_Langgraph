# LangGraph Multi-Agent 아키텍처

## 전체 시스템 아키텍처

```mermaid
graph TD
    Start([시작]) --> Init[초기 상태 생성]
    Init --> WF[LangGraph 워크플로우]
    
    WF --> VP[VideoProcessorAgent]
    VP --> RD[ReferenceDetectorAgent]
    RD --> AA[ActionAnalyzerAgent]
    AA --> RA[ReporterAgent]
    RA --> End([종료])
    
    VP -.->|video_info| State[(공유 상태)]
    RD -.->|reference_times| State
    AA -.->|action_analysis| State
    RA -.->|final_report| State
    
    State -.->|read| VP
    State -.->|read| RD
    State -.->|read| AA
    State -.->|read| RA
    
    style VP fill:#e1f5ff
    style RD fill:#fff4e1
    style AA fill:#e8f5e1
    style RA fill:#ffe1e1
    style State fill:#f0f0f0
```

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

### 2. ReferenceDetectorAgent

```mermaid
graph TD
    A[시작] --> B{inhalerIN 탐지}
    B -->|시간 슬라이딩| C[프레임 추출]
    C --> D[LLM 분석]
    D --> E{Overall_Answer?}
    E -->|YES| F[reference_time 저장]
    E -->|NO| B
    
    F --> G{faceONinhaler 탐지}
    G --> H[프레임 추출]
    H --> I[LLM 분석]
    I --> J{Overall_Answer?}
    J -->|YES| K[reference_time 저장]
    J -->|NO| G
    
    K --> L{inhalerOUT 탐지}
    L --> M[프레임 추출]
    M --> N[LLM 분석]
    N --> O{Overall_Answer?}
    O -->|YES| P[reference_time 저장]
    O -->|NO| L
    
    P --> Q[PromptBank 업데이트]
    Q --> R[완료]
    
    style F fill:#90EE90
    style K fill:#90EE90
    style P fill:#90EE90
```

**입력:**
- video_path
- video_info (play_time)

**출력:**
- reference_times (inhalerIN, faceONinhaler, inhalerOUT)
- q_answers_accumulated (Q&A 결과)
- promptbank_data (PromptBank 전체 데이터)

**주요 메서드:**
- `process(state)`: 모든 기준 시점 탐지
- `_detect_inhaler_in()`: inhalerIN 탐지
- `_detect_face_on_inhaler()`: faceONinhaler 탐지
- `_detect_inhaler_out()`: inhalerOUT 탐지
- `_search_reference_time()`: 시간 슬라이딩 탐색

### 3. ActionAnalyzerAgent

```mermaid
graph LR
    A[PromptBank 데이터] --> B[행동 단계별 분석]
    B --> C{각 행동}
    C --> D[YES 시간 추출]
    C --> E[NO 시간 추출]
    C --> F[Confidence 정보]
    
    D --> G[action_summary]
    E --> G
    F --> G
    
    G --> H[(action_analysis_results)]
    
    style G fill:#e8f5e1
    style H fill:#f0f0f0
```

**입력:**
- promptbank_data

**출력:**
- action_analysis_results (행동별 요약)

**주요 메서드:**
- `process(state)`: 행동 분석 실행
- `_create_action_summary()`: 행동 요약 생성

### 4. ReporterAgent

```mermaid
graph TD
    A[모든 결과 수집] --> B[최종 리포트 생성]
    B --> C[Plotly 시각화]
    
    C --> D[Reference Time 표시]
    C --> E[Action Steps 표시]
    C --> F[Confidence 색상 매핑]
    
    D --> G[그래프 출력]
    E --> G
    F --> G
    
    G --> H[요약 정보 출력]
    
    style B fill:#ffe1e1
    style G fill:#FFD700
```

**입력:**
- video_info
- reference_times
- action_analysis_results
- promptbank_data

**출력:**
- final_report (최종 리포트)
- visualization_path (시각화 결과)

**주요 메서드:**
- `process(state)`: 리포트 생성 실행
- `_create_final_report()`: 최종 리포트 생성
- `_create_visualization()`: Plotly 시각화
- `_print_summary()`: 요약 정보 출력

## 상태(State) 관리

```mermaid
graph TD
    A[VideoAnalysisState] --> B[입력 데이터]
    A --> C[처리 결과]
    A --> D[메타데이터]
    
    B --> B1[video_path]
    B --> B2[llm_name]
    B --> B3[api_key]
    
    C --> C1[video_info]
    C --> C2[reference_times]
    C --> C3[action_analysis_results]
    C --> C4[promptbank_data]
    C --> C5[final_report]
    
    D --> D1[errors]
    D --> D2[status]
    D --> D3[agent_logs]
    
    style A fill:#f0f0f0
    style B fill:#e1f5ff
    style C fill:#e8f5e1
    style D fill:#ffe1e1
```

### 상태 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `video_path` | str | 비디오 파일 경로 |
| `llm_name` | str | LLM 모델 이름 |
| `api_key` | str | OpenAI API 키 |
| `video_info` | Dict | 비디오 메타데이터 |
| `reference_times` | Dict | 기준 시간들 |
| `reference_detection_results` | Dict | 탐지 결과 |
| `action_analysis_results` | Dict | 행동 분석 결과 |
| `q_answers_accumulated` | Dict | Q&A 누적 결과 |
| `promptbank_data` | Dict | PromptBank 데이터 |
| `final_report` | Dict | 최종 리포트 |
| `visualization_path` | str | 시각화 경로 |
| `errors` | List[str] | 오류 목록 |
| `status` | str | 현재 상태 |
| `agent_logs` | List[Dict] | Agent 로그 |

## 워크플로우 실행 흐름

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Workflow
    participant VP as VideoProcessor
    participant RD as ReferenceDetector
    participant AA as ActionAnalyzer
    participant RA as Reporter
    participant State
    
    User->>Main: run()
    Main->>Workflow: create_workflow(mllm)
    Main->>State: create_initial_state()
    Main->>Workflow: workflow.run(initial_state)
    
    Workflow->>VP: process(state)
    VP->>State: update video_info
    VP-->>Workflow: return state
    
    Workflow->>RD: process(state)
    RD->>State: read video_info
    RD->>RD: detect inhalerIN
    RD->>RD: detect faceONinhaler
    RD->>RD: detect inhalerOUT
    RD->>State: update reference_times
    RD-->>Workflow: return state
    
    Workflow->>AA: process(state)
    AA->>State: read promptbank_data
    AA->>AA: analyze actions
    AA->>State: update action_analysis
    AA-->>Workflow: return state
    
    Workflow->>RA: process(state)
    RA->>State: read all results
    RA->>RA: create report
    RA->>RA: create visualization
    RA->>State: update final_report
    RA-->>Workflow: return state
    
    Workflow-->>Main: return final_state
    Main-->>User: display results
```

## 데이터 흐름

```mermaid
graph LR
    A[비디오 파일] --> B[VideoProcessor]
    B --> C[video_info]
    
    C --> D[ReferenceDetector]
    A --> D
    D --> E[reference_times]
    D --> F[q_answers]
    
    E --> G[PromptBank]
    F --> G
    G --> H[promptbank_data]
    
    H --> I[ActionAnalyzer]
    I --> J[action_analysis]
    
    C --> K[Reporter]
    E --> K
    H --> K
    J --> K
    K --> L[final_report]
    K --> M[visualization]
    
    style A fill:#e1f5ff
    style C fill:#fff4e1
    style E fill:#e8f5e1
    style H fill:#ffe1e1
    style L fill:#FFD700
    style M fill:#FFD700
```

## 확장 가능성

### 병렬 처리 예제

```mermaid
graph TD
    A[VideoProcessor] --> B{분기}
    B -->|병렬 1| C[ReferenceDetector]
    B -->|병렬 2| D[QualityValidator]
    
    C --> E[수렴]
    D --> E
    
    E --> F[ActionAnalyzer]
    F --> G[Reporter]
    
    style B fill:#FFD700
    style E fill:#FFD700
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

