# LangGraph Multi-Agent 흡입기 비디오 분석기 - 인덱스

## 📖 문서 가이드

프로젝트를 처음 접하시나요? 다음 순서로 문서를 읽어보세요:

### 🚀 시작하기 (5-10분)

1. **[QUICKSTART.md](QUICKSTART.md)** ⭐⭐⭐⭐⭐
   - 5분 만에 시작하는 가이드
   - 설치 및 기본 실행 방법
   - 간단한 예제

### 📚 이해하기 (20-30분)

2. **[SUMMARY_MULTIAGENT.md](SUMMARY_MULTIAGENT.md)** ⭐⭐⭐⭐⭐
   - 프로젝트 전체 개요
   - Multi-Agent 아키텍처 설명
   - 주요 개선사항 요약

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** ⭐⭐⭐⭐
   - 시스템 아키텍처 상세 설명
   - Agent별 구조 및 역할
   - 데이터 흐름 다이어그램
   - Mermaid 시각화

4. **[COMPARISON.md](COMPARISON.md)** ⭐⭐⭐⭐
   - 원본 코드와의 비교
   - 장단점 분석
   - 실제 사용 시나리오

### 🔧 사용하기 (30분-1시간)

5. **[README_LANGGRAPH.md](README_LANGGRAPH.md)** ⭐⭐⭐⭐
   - 자세한 사용 설명서
   - Agent별 상세 설명
   - 베스트 프랙티스
   - FAQ

6. **[example_usage.py](example_usage.py)** ⭐⭐⭐⭐
   - 다양한 사용 예제
   - 커스텀 워크플로우
   - 오류 처리 예제

## 📁 파일 구조

### 핵심 파일

```
app/
├── 📖 문서 (당신이 지금 보는 파일들)
│   ├── INDEX.md                    # 📍 이 파일
│   ├── QUICKSTART.md               # ⚡ 빠른 시작
│   ├── SUMMARY_MULTIAGENT.md       # 📋 프로젝트 요약
│   ├── ARCHITECTURE.md             # 🏗️ 아키텍처 설명
│   ├── COMPARISON.md               # 📊 원본과 비교
│   └── README_LANGGRAPH.md         # 📖 상세 문서
│
├── 🤖 Agent 모듈 (핵심 로직)
│   └── agents/
│       ├── state.py                     # 상태 정의
│       ├── video_processor_agent.py     # 비디오 처리
│       ├── reference_detector_agent.py  # 기준 시점 탐지
│       ├── action_analyzer_agent.py     # 행동 분석
│       └── reporter_agent.py            # 리포팅
│
├── 🔄 워크플로우
│   └── graph_workflow.py           # LangGraph 워크플로우
│
├── 🚀 실행 파일
│   ├── main_langgraph_251109.py    # 메인 실행
│   └── example_usage.py            # 사용 예제
│
├── 🛠️ 유틸리티 (기존 코드)
│   ├── class_MultimodalLLM_QA_251107.py
│   ├── class_Media_Edit_251107.py
│   └── class_PromptBank_251107.py
│
└── 📦 설정
    └── requirements_langgraph.txt  # 패키지 요구사항
```

### 참고용 파일

```
app/
├── 251107 inhaler_video_analyzer.py  # 원본 코드 (비교용)
└── video_source/                      # 비디오 파일들
```

## 🎯 사용 시나리오별 가이드

### 시나리오 1: 처음 사용하는 경우

```
1. QUICKSTART.md 읽기 (5분)
2. 환경 설정 및 패키지 설치
3. main_langgraph_251109.py 실행
4. 결과 확인
```

### 시나리오 2: 코드 이해가 필요한 경우

```
1. SUMMARY_MULTIAGENT.md 읽기 (10분)
2. ARCHITECTURE.md 읽기 (15분)
3. 각 Agent 파일 읽기 (30분)
4. example_usage.py 실행해보기
```

### 시나리오 3: 커스터마이징이 필요한 경우

```
1. README_LANGGRAPH.md의 커스터마이징 섹션
2. example_usage.py의 예제 3번 참고
3. 해당 Agent 파일 수정
4. 테스트 및 검증
```

### 시나리오 4: 원본과 비교하고 싶은 경우

```
1. COMPARISON.md 읽기 (20분)
2. 251107 inhaler_video_analyzer.py 확인
3. agents/ 폴더의 파일들 비교
4. 성능 및 코드 품질 평가
```

### 시나리오 5: 프로덕션 배포

```
1. README_LANGGRAPH.md의 베스트 프랙티스
2. ARCHITECTURE.md의 오류 처리 섹션
3. 테스트 전략 수립
4. 모니터링 설정
5. 배포
```

## 🔍 주요 개념 찾기

### Agent 관련
- **Agent란?** → [SUMMARY_MULTIAGENT.md](SUMMARY_MULTIAGENT.md#agent-상세-구조)
- **Agent 추가** → [README_LANGGRAPH.md](README_LANGGRAPH.md#새로운-agent-추가)
- **Agent 구조** → [ARCHITECTURE.md](ARCHITECTURE.md#agent-상세-구조)

### 워크플로우 관련
- **워크플로우란?** → [ARCHITECTURE.md](ARCHITECTURE.md#전체-시스템-아키텍처)
- **워크플로우 수정** → [README_LANGGRAPH.md](README_LANGGRAPH.md#워크플로우-수정)
- **실행 흐름** → [ARCHITECTURE.md](ARCHITECTURE.md#워크플로우-실행-흐름)

### 상태 관리
- **State란?** → [agents/state.py](agents/state.py)
- **상태 필드** → [ARCHITECTURE.md](ARCHITECTURE.md#상태state-관리)
- **상태 업데이트** → [README_LANGGRAPH.md](README_LANGGRAPH.md#상태-관리)

### 비교 및 평가
- **원본과 차이점** → [COMPARISON.md](COMPARISON.md#주요-차이점)
- **성능 비교** → [COMPARISON.md](COMPARISON.md#성능-비교)
- **사용 사례** → [COMPARISON.md](COMPARISON.md#실제-사용-시나리오)

## 💡 빠른 참조

### 코드 스니펫

#### 기본 실행
```python
# main_langgraph_251109.py 참조
from graph_workflow import create_workflow
workflow = create_workflow(mllm)
final_state = workflow.run(initial_state)
```

#### Agent 개발
```python
# agents/video_processor_agent.py 참조
class MyAgent:
    def process(self, state):
        # 처리 로직
        return state
```

#### 워크플로우 정의
```python
# graph_workflow.py 참조
workflow.add_node("my_agent", self._my_agent_node)
workflow.add_edge("previous_agent", "my_agent")
```

### 주요 명령어

```bash
# 설치
pip install -r requirements_langgraph.txt

# 실행
python main_langgraph_251109.py

# 예제 실행
python example_usage.py

# 테스트 (예정)
pytest tests/
```

## 📞 도움말

### 문제 해결

| 문제 | 참조 문서 | 섹션 |
|------|-----------|------|
| API 키 오류 | QUICKSTART.md | 문제 해결 |
| 비디오 파일 오류 | README_LANGGRAPH.md | 트러블슈팅 |
| LangGraph 설치 오류 | QUICKSTART.md | 환경 설정 |
| Agent 수정 방법 | README_LANGGRAPH.md | 커스터마이징 |
| 성능 최적화 | ARCHITECTURE.md | 성능 최적화 |

### 추가 학습 자료

1. **LangGraph 공식 문서**
   - https://langchain-ai.github.io/langgraph/

2. **LangChain 공식 문서**
   - https://python.langchain.com/

3. **OpenAI API 문서**
   - https://platform.openai.com/docs

4. **Multi-Agent Systems**
   - [관련 논문 및 자료 링크]

## 🎓 학습 경로

### 초급 (1-2일)
1. ✅ QUICKSTART.md 읽고 실행
2. ✅ SUMMARY_MULTIAGENT.md로 개념 이해
3. ✅ example_usage.py 실행해보기
4. ✅ 간단한 비디오로 테스트

### 중급 (3-5일)
1. ✅ ARCHITECTURE.md로 구조 이해
2. ✅ 각 Agent 파일 코드 읽기
3. ✅ 워크플로우 수정해보기
4. ✅ 새로운 행동 단계 추가

### 고급 (1-2주)
1. ✅ 새로운 Agent 개발
2. ✅ 병렬 처리 구현
3. ✅ 성능 최적화
4. ✅ 프로덕션 배포

## 🗺️ 프로젝트 로드맵

### 완료 ✅
- [x] Multi-Agent 아키텍처 구현
- [x] LangGraph 워크플로우 구성
- [x] 4개 Agent 개발
- [x] 포괄적인 문서 작성

### 계획 중 📋
- [ ] Quality Validator Agent 추가
- [ ] 병렬 처리 구현
- [ ] 단위 테스트 작성
- [ ] 성능 벤치마크
- [ ] 웹 인터페이스 개발

### 향후 고려사항 💭
- [ ] 다른 의료 기기 지원
- [ ] 실시간 분석 기능
- [ ] 클라우드 배포
- [ ] API 서버 구축

## 📊 통계

- **총 코드 라인 수**: ~1,170 줄
- **Agent 수**: 4개
- **문서 파일 수**: 6개
- **예제 수**: 4개
- **지원 비디오 형식**: mp4, mov, avi, mkv 등

## 🏆 베스트 프랙티스 체크리스트

### 개발 시
- [ ] Agent는 단일 책임 원칙 준수
- [ ] 상태는 불변성 유지
- [ ] 오류는 적절히 처리 및 로깅
- [ ] 코드는 명확한 주석 포함
- [ ] 함수는 명확한 docstring 포함

### 배포 시
- [ ] 환경 변수로 API 키 관리
- [ ] 적절한 로깅 설정
- [ ] 오류 모니터링 구현
- [ ] 성능 메트릭 수집
- [ ] 백업 및 복구 계획

## 📝 변경 이력

### v1.0 (2024.11.09)
- 초기 Multi-Agent 구조 구현
- 4개 핵심 Agent 개발
- LangGraph 워크플로우 구성
- 포괄적인 문서 작성

---

**마지막 업데이트**: 2024.11.09  
**버전**: 1.0  
**라이센스**: MIT

## 🎉 시작하기

준비되셨나요? [QUICKSTART.md](QUICKSTART.md)로 이동하여 5분 만에 시작하세요!

