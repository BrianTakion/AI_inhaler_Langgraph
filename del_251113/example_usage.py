#!/usr/bin/env python
# coding: utf-8

"""
LangGraph Multi-Agent 사용 예제
다양한 비디오 파일을 분석하는 방법을 보여줍니다.
"""

import os
from dotenv import load_dotenv
import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow


def analyze_video(video_path: str, llm_name: str = "gpt-4o"):
    """
    비디오 파일을 분석하는 헬퍼 함수
    
    Args:
        video_path: 비디오 파일 경로
        llm_name: 사용할 LLM 모델 이름
        
    Returns:
        분석 결과 (final_state)
    """
    # 환경 변수 로드
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
    
    # LLM 초기화
    print(f"LLM 모델 초기화: {llm_name}")
    mllm = mLLM.multimodalLLM(llm_name=llm_name, api_key=api_key)
    
    # 초기 상태 생성
    initial_state = create_initial_state(
        video_path=video_path,
        llm_name=llm_name,
        api_key=api_key
    )
    
    # 워크플로우 생성 및 실행
    workflow = create_workflow(mllm)
    final_state = workflow.run(initial_state)
    
    return final_state


def example_1_single_video():
    """예제 1: 단일 비디오 분석"""
    print("\n" + "="*60)
    print("예제 1: 단일 비디오 분석")
    print("="*60)
    
    video_path = "/workspace/app/video_source/pMDI/10_Foster_full.mov"
    final_state = analyze_video(video_path)
    
    if final_state["status"] == "completed":
        print("\n✅ 분석 완료!")
        report = final_state["final_report"]
        print(f"감지된 행동: {report['summary']['total_actions_detected']}개")
    else:
        print("\n❌ 분석 실패")


def example_2_multiple_videos():
    """예제 2: 여러 비디오 분석"""
    print("\n" + "="*60)
    print("예제 2: 여러 비디오 분석")
    print("="*60)
    
    base_dir = "/workspace/app/video_source"
    video_list = [
        base_dir + "/pMDI/10_Foster_full.mov",
        base_dir + "/SMI/03_SMI_full.mov",
    ]
    
    results = []
    for video_path in video_list:
        print(f"\n분석 중: {os.path.basename(video_path)}")
        try:
            final_state = analyze_video(video_path)
            results.append({
                "video": os.path.basename(video_path),
                "status": final_state["status"],
                "report": final_state.get("final_report")
            })
        except Exception as e:
            print(f"오류 발생: {e}")
            results.append({
                "video": os.path.basename(video_path),
                "status": "error",
                "error": str(e)
            })
    
    # 결과 요약
    print("\n" + "="*60)
    print("분석 결과 요약")
    print("="*60)
    for result in results:
        status_icon = "✅" if result["status"] == "completed" else "❌"
        print(f"{status_icon} {result['video']}: {result['status']}")


def example_3_custom_workflow():
    """예제 3: 커스텀 워크플로우"""
    print("\n" + "="*60)
    print("예제 3: 커스텀 워크플로우 (Agent별 접근)")
    print("="*60)
    
    # 환경 변수 로드
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    # LLM 초기화
    mllm = mLLM.multimodalLLM(llm_name="gpt-4o", api_key=api_key)
    
    # 개별 Agent 사용 예제
    from agents.video_processor_agent import VideoProcessorAgent
    from agents.state import VideoAnalysisState
    
    video_path = "/workspace/app/video_source/pMDI/10_Foster_full.mov"
    
    # 초기 상태
    state = create_initial_state(video_path, "gpt-4o", api_key)
    
    # 1. VideoProcessor만 실행
    video_processor = VideoProcessorAgent()
    state = video_processor.process(state)
    
    print(f"\n비디오 정보:")
    print(f"  이름: {state['video_info']['video_name']}")
    print(f"  재생시간: {state['video_info']['play_time']}초")
    print(f"  프레임 수: {state['video_info']['frame_count']}")
    
    # 여기서 멈추거나, 필요한 Agent만 선택적으로 실행 가능


def example_4_error_handling():
    """예제 4: 오류 처리"""
    print("\n" + "="*60)
    print("예제 4: 오류 처리")
    print("="*60)
    
    # 존재하지 않는 비디오 파일
    invalid_video_path = "/workspace/app/video_source/non_existent.mp4"
    
    try:
        final_state = analyze_video(invalid_video_path)
        
        if final_state.get("errors"):
            print("\n발생한 오류:")
            for error in final_state["errors"]:
                print(f"  - {error}")
    except Exception as e:
        print(f"예외 발생: {e}")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("### LangGraph Multi-Agent 사용 예제 ###")
    print("#"*60)
    
    # 실행할 예제 선택
    examples = {
        "1": example_1_single_video,
        "2": example_2_multiple_videos,
        "3": example_3_custom_workflow,
        "4": example_4_error_handling
    }
    
    print("\n실행할 예제를 선택하세요:")
    print("1. 단일 비디오 분석")
    print("2. 여러 비디오 분석")
    print("3. 커스텀 워크플로우")
    print("4. 오류 처리")
    
    # 기본값: 예제 1 실행
    choice = input("\n선택 (기본값: 1): ").strip() or "1"
    
    if choice in examples:
        examples[choice]()
    else:
        print("잘못된 선택입니다. 예제 1을 실행합니다.")
        example_1_single_video()

