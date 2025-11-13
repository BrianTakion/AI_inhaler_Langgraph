# LangGraph Multi-Agent 흡입기 비디오 분석기 - 인덱스

## 📖 문서 가이드

프로젝트를 처음 접하시나요? 다음 순서로 문서를 읽어보세요:

### 🚀 시작하기 (5-10분)

1. **[README.md](../README.md)** ⭐⭐⭐⭐⭐
   - 프로젝트 개요 및 빠른 시작
   - 동적 LLM 모델 리스트 기반 구조
   - 설치 및 기본 실행 방법

### 📚 이해하기 (20-30분)

2. **[ARCHITECTURE.md](ARCHITECTURE.md)** ⭐⭐⭐⭐⭐
   - 시스템 아키텍처 상세 설명
   - Agent별 구조 및 역할
   - 데이터 흐름 다이어그램
   - Mermaid 시각화

3. **[MULTIMODEL_ARCHITECTURE.md](MULTIMODEL_ARCHITECTURE.md)** ⭐⭐⭐⭐
   - 동적 모델 리스트 아키텍처
   - 병렬 실행 메커니즘
   - State 구조 및 Reducer 함수 상세
   - 평균 계산 로직

### 🔧 사용하기 (30분-1시간)

4. **코드 예제**
   - `main_langgraph_251109.py`: 동적 모델 리스트 사용 예제
   - `graph_workflow.py`: 동적 워크플로우 구현 예제

## 📁 파일 구조

### 핵심 파일 (동적 모델 지원)

```
app/
├── 📖 문서
│   ├── README.md                      # 📍 프로젝트 개요
│   ├── INDEX.md                       # 📍 이 파일
│   ├── ARCHITECTURE.md                # 🏗️ 아키텍처 설명
│   └── MULTIMODEL_ARCHITECTURE.md     # 🏗️ 동적 모델 구조
│
├── 🤖 Agent 모듈 (동적 모델 지원)
│   └── agents/
│       ├── state.py                   # 동적 State 정의
│       ├── video_processor_agent.py   # 비디오 처리
│       ├── video_analyzer_agent.py    # 범용 분석 Agent
│       └── reporter_agent.py          # 동적 평균 계산
│
├── 🔄 워크플로우 (동적 노드 생성)
│   └── graph_workflow.py              # LangGraph 동적 워크플로우
│
├── 🚀 실행 파일 (리스트 기반)
│   └── main_langgraph_251109.py       # 메인 실행
│
├── 🛠️ 유틸리티
│   ├── class_MultimodalLLM_QA_251107.py
│   ├── class_Media_Edit_251107.py
│   └── class_PromptBank_251107.py
│
├── 📦 설정
│   └── requirements_langgraph.txt
│
└── 🎬 데이터
    └── video_source/
```

### 참고용 파일

```
app/
└── 251113_del/                      # 🗑️ 이전 버전 파일들
    ├── video_analyzer_agent.py      # 원본 통합 Agent
    ├── video_analyzer_agent_4o.py   # 고정 GPT-4o Agent
    └── video_analyzer_agent_4o_mini.py # 고정 GPT-4o-mini Agent
```

## 🎯 사용 시나리오별 가이드

### 시나리오 1: 처음 사용하는 경우

```
1. README.md 읽기 (5분)
2. 환경 설정 및 패키지 설치
3. llm_models 리스트 설정
4. main_langgraph_251109.py 실행
5. 결과 확인
```

### 시나리오 2: 다양한 모델 조합 테스트

```
1. main_langgraph_251109.py 열기
2. llm_models 리스트 수정
   예: ["gpt-4o-mini", "gpt-4o-mini", "gpt-4o"]
3. 실행 및 결과 비교
4. 다른 조합으로 반복
```

### 시나리오 3: 코드 이해가 필요한 경우

```
1. ARCHITECTURE.md 읽기 (15분)
2. MULTIMODEL_ARCHITECTURE.md 읽기 (10분)
3. agents/state.py 확인 (동적 구조)
4. graph_workflow.py 확인 (동적 노드)
5. agents/video_analyzer_agent.py 확인 (범용 Agent)
```

### 시나리오 4: 커스터마이징이 필요한 경우

```
1. ARCHITECTURE.md의 커스터마이징 섹션
2. 동적 구조 활용
3. 필요한 경우에만 Agent 파일 수정
4. 테스트 및 검증
```

## 🔍 주요 개념 찾기

### 동적 모델 관련
- **모델 리스트 설정** → [main_langgraph_251109.py](main_langgraph_251109.py#L43)
- **동적 Agent 생성** → [graph_workflow.py](graph_workflow.py#L47-51)
- **평균 계산** → [agents/reporter_agent.py](agents/reporter_agent.py#L84-207)

### Agent 관련
- **범용 Agent 구조** → [agents/video_analyzer_agent.py](agents/video_analyzer_agent.py#L36-49)
- **Agent 초기화** → [graph_workflow.py](graph_workflow.py#L27-51)
- **Agent 실행** → [ARCHITECTURE.md](ARCHITECTURE.md#agent-상세-구조)

### 워크플로우 관련
- **동적 노드 생성** → [graph_workflow.py](graph_workflow.py#L68-71)
- **병렬 실행** → [graph_workflow.py](graph_workflow.py#L79-87)
- **실행 흐름** → [ARCHITECTURE.md](ARCHITECTURE.md#전체-시스템-아키텍처)

### 상태 관리
- **동적 State 구조** → [agents/state.py](agents/state.py#L35-93)
- **model_results 필드** → [agents/state.py](agents/state.py#L80)
- **Reducer 함수** → [agents/state.py](agents/state.py#L14-32)

## 💡 빠른 참조

### 코드 스니펫

#### LLM 모델 리스트 설정
```python
# 1개 모델
llm_models = ["gpt-4o"]

# 2개 모델
llm_models = ["gpt-4o", "gpt-4o-mini"]

# 3개 모델 (중복 가능)
llm_models = ["gpt-4o-mini", "gpt-4o-mini", "gpt-4o"]

# N개 동일 모델
llm_models = ["gpt-4o"] * 5
```

#### 기본 실행
```python
# LLM 인스턴스 생성
mllm_instances = [
    mLLM.multimodalLLM(llm_name=model, api_key=api_key)
    for model in llm_models
]

# 워크플로우 생성 및 실행
workflow = create_workflow(mllm_instances, llm_models)
final_state = workflow.run(initial_state)
```

### 주요 명령어

```bash
# 설치
pip install -r requirements_langgraph.txt

# 실행
python main_langgraph_251109.py

# 환경 변수 설정
echo "OPENAI_API_KEY=your-key" > .env
```

## 📞 도움말

### 문제 해결

| 문제 | 해결 방법 |
|------|-----------|
| API 키 오류 | .env 파일에 OPENAI_API_KEY 설정 확인 |
| 비디오 파일 오류 | video_path 경로 및 파일 존재 확인 |
| 모델 추가 방법 | llm_models 리스트에 모델 이름 추가 |
| 성능 최적화 | 모델 개수 조절 (많을수록 정확하지만 느림) |

### 추가 학습 자료

1. **LangGraph 공식 문서**
   - https://langchain-ai.github.io/langgraph/

2. **LangChain 공식 문서**
   - https://python.langchain.com/

3. **OpenAI API 문서**
   - https://platform.openai.com/docs

## 🎓 학습 경로

### 초급 (1-2일)
1. ✅ README.md 읽고 실행
2. ✅ llm_models 리스트 다양하게 테스트
3. ✅ 간단한 비디오로 테스트
4. ✅ 결과 시각화 확인

### 중급 (3-5일)
1. ✅ ARCHITECTURE.md로 구조 이해
2. ✅ 동적 Agent 생성 로직 파악
3. ✅ 평균 계산 로직 이해
4. ✅ State 구조 분석

### 고급 (1-2주)
1. ✅ 새로운 Reducer 함수 개발
2. ✅ 커스텀 평균 계산 로직
3. ✅ 성능 최적화
4. ✅ 프로덕션 배포

## 🗺️ 주요 개선사항

### 완료 ✅
- [x] Multi-Agent 아키텍처 구현
- [x] LangGraph 워크플로우 구성
- [x] 동적 LLM 모델 리스트 지원
- [x] 동적 노드 생성 워크플로우
- [x] 범용 VideoAnalyzerAgent
- [x] 동적 평균 계산
- [x] 포괄적인 문서 작성

### 주요 특징 🌟
- **유연성**: 1개부터 N개까지 자유로운 모델 개수
- **확장성**: 코드 수정 없이 리스트만 변경
- **정확도**: 여러 모델 평균으로 안정적인 결과
- **효율성**: 모든 모델이 병렬로 실행

## 📊 통계

- **총 코드 라인 수**: ~1,000 줄
- **Agent 수**: 3개 (동적 생성)
- **문서 파일 수**: 4개
- **지원 모델 수**: 무제한 (리스트로 지정)
- **지원 비디오 형식**: mp4, mov, avi, mkv 등

## 🏆 베스트 프랙티스

### 모델 선택
- [ ] 빠른 테스트: `["gpt-4o-mini"]` 1개
- [ ] 균형: `["gpt-4o-mini", "gpt-4o"]` 2개
- [ ] 정확도 우선: `["gpt-4o", "gpt-4o", "gpt-4o"]` 3개 이상
- [ ] 일관성 검증: `["gpt-4o"] * 5` 동일 모델 여러 번

### 개발 시
- [ ] 동적 구조 활용 (고정 코드 최소화)
- [ ] State는 불변성 유지
- [ ] Reducer 함수 이해
- [ ] 명확한 주석 포함

## 📝 변경 이력

### v2.0 (2024.11.13)
- 동적 LLM 모델 리스트 지원
- 범용 VideoAnalyzerAgent 구현
- 동적 노드 생성 워크플로우
- 동적 평균 계산 ReporterAgent
- 문서 업데이트

### v1.0 (2024.11.09)
- 초기 Multi-Agent 구조 구현
- 고정 2개 모델 병렬 실행
- LangGraph 워크플로우 구성

---

**마지막 업데이트**: 2024.11.13  
**버전**: 2.0  
**라이센스**: MIT

## 🎉 시작하기

준비되셨나요? [README.md](../README.md)로 이동하여 5분 만에 시작하세요!
