# LangGraph Multi-Agent 빠른 시작 가이드

## 5분 만에 시작하기

### 1단계: 환경 설정 (1분)

```bash
# 1. 패키지 설치
pip install langgraph langchain langchain-openai openai opencv-python plotly python-dotenv

# 또는 requirements 파일 사용
pip install -r requirements_langgraph.txt

# 2. API 키 설정
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 2단계: 비디오 파일 준비 (1분)

비디오 파일을 `video_source/` 폴더에 배치하거나, 원하는 경로를 지정하세요.

```
video_source/
├── pMDI/
│   └── 10_Foster_full.mov
├── SMI/
│   └── 03_SMI_full.mov
└── DPI/
    └── 01_Ellipta_full.mov
```

### 3단계: 병렬 실행 (3분)

```bash
# 메인 스크립트 실행 (GPT-4o + GPT-4o-mini 병렬 분석)
python main_langgraph_251109.py
```

**실행 특징**:
- GPT-4o와 GPT-4o-mini가 동시에 비디오를 분석
- 두 모델의 결과를 평균하여 더 정확한 분석 결과 제공
- 분석 완료 후 Plotly 그래프가 자동으로 표시됨

## 결과 확인

실행 후 다음과 같은 출력을 볼 수 있습니다:

```
##################################################
### LangGraph Multi-Agent 워크플로우 시작 ###
##################################################

==================================================
=== 1. Video Processor Agent 실행 ===
==================================================
[VideoProcessorAgent] 비디오 정보: 10_Foster_full, 45.2초, 1356프레임

==================================================
=== 2. Reference Detector Agent 실행 ===
==================================================
[ReferenceDetectorAgent] inhalerIN 탐지 시작...
  검색 중... start_time=0.0초
  검색 중... start_time=3.0초
[ReferenceDetectorAgent] inhalerIN 탐지 완료: 3.0초

[ReferenceDetectorAgent] faceONinhaler 탐지 시작...
  검색 중... start_time=3.0초
  검색 중... start_time=5.0초
[ReferenceDetectorAgent] faceONinhaler 탐지 완료: 7.0초

[ReferenceDetectorAgent] inhalerOUT 탐지 시작...
  검색 중... start_time=7.0초
  검색 중... start_time=10.0초
[ReferenceDetectorAgent] inhalerOUT 탐지 완료: 13.0초

==================================================
=== 3. Action Analyzer Agent 실행 ===
==================================================
[ActionAnalyzerAgent] 행동 단계 분석 완료: 13개 행동

==================================================
=== 4. Reporter Agent 실행 ===
==================================================

==================================================
=== 비디오 분석 결과 요약 ===
==================================================

[비디오 정보]
  파일명: 10_Foster_full
  재생시간: 45.2초
  총 프레임: 1356
  해상도: 1920x1080px

[기준 시간]
  inhalerIN: 3.0초
  faceONinhaler: 7.0초
  inhalerOUT: 13.0초

[행동 분석]
  총 감지된 행동: 8개

==================================================

✅ 분석이 성공적으로 완료되었습니다!
총 8개의 행동이 감지되었습니다.

[시각화 그래프 표시]
```

## 고급 사용법

### 커스텀 비디오 분석

```python
from dotenv import load_dotenv
import os
import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow

# 환경 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# LLM 초기화
mllm = mLLM.multimodalLLM(llm_name="gpt-4o", api_key=api_key)

# 비디오 경로
video_path = "/path/to/your/video.mp4"

# 초기 상태 생성
initial_state = create_initial_state(
    video_path=video_path,
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

### 여러 비디오 일괄 분석

```python
video_list = [
    "/path/to/video1.mp4",
    "/path/to/video2.mp4",
    "/path/to/video3.mp4"
]

for video_path in video_list:
    print(f"\n분석 중: {video_path}")
    initial_state = create_initial_state(video_path, "gpt-4o", api_key)
    workflow = create_workflow(mllm)
    final_state = workflow.run(initial_state)
    
    # 결과 저장
    # ...
```

### Agent별 개별 실행

```python
from agents.video_processor_agent import VideoProcessorAgent
from agents.reference_detector_agent import ReferenceDetectorAgent

# VideoProcessor만 실행
video_processor = VideoProcessorAgent()
state = create_initial_state(video_path, "gpt-4o", api_key)
state = video_processor.process(state)

print(f"비디오 정보: {state['video_info']}")

# ReferenceDetector 실행
reference_detector = ReferenceDetectorAgent(mllm, video_processor)
state = reference_detector.process(state)

print(f"기준 시간: {state['reference_times']}")
```

## 문제 해결

### 문제: API 키 오류
```
ValueError: OPENAI_API_KEY 환경변수가 설정되지 않았습니다.
```

**해결:**
```bash
echo "OPENAI_API_KEY=your-actual-api-key" > .env
```

### 문제: 비디오 파일을 열 수 없음
```
[VideoProcessorAgent] 비디오 처리 중 오류: 비디오 파일을 열 수 없습니다
```

**해결:**
1. 비디오 파일 경로 확인
2. 파일 형식 확인 (mp4, mov, avi 등)
3. 파일 접근 권한 확인

### 문제: LangGraph 모듈을 찾을 수 없음
```
ModuleNotFoundError: No module named 'langgraph'
```

**해결:**
```bash
pip install langgraph langchain langchain-openai
```

## 다음 단계

1. **예제 실행**: `python example_usage.py`
2. **문서 읽기**: `README_LANGGRAPH.md`
3. **비교 분석**: `COMPARISON.md`
4. **커스터마이징**: 각 Agent 클래스 수정

## 지원

문제가 있거나 질문이 있으면:
1. `COMPARISON.md`에서 원본과의 차이점 확인
2. `README_LANGGRAPH.md`에서 자세한 설명 확인
3. `example_usage.py`에서 다양한 사용 예제 확인

---

**팁:** 처음 실행 시 OpenAI API 비용이 발생할 수 있습니다. 짧은 비디오로 먼저 테스트해보세요.

