#!/usr/bin/env python
# coding: utf-8

"""
LangGraph 기반 Multi-Agent 흡입기 비디오 분석기
동적 LLM 모델 리스트 지원 - 병렬 실행 및 평균 시각화
"""

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다. .env 파일에 'OPENAI_API_KEY=your-key' 형식으로 추가하세요.")

import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow


def main():
    """
    메인 실행 함수
    
    주요 기능:
    1. 리스트로 여러 LLM 모델 지정 (같은 모델 중복 가능)
    2. 모든 모델이 병렬로 비디오 분석 수행
    3. 결과를 자동으로 평균 계산 및 시각화
    """
    
    # ========================================
    # LLM 모델 설정
    # ========================================
    # 리스트에 원하는 모델을 자유롭게 지정 (개수 제한 없음, 중복 가능)
    # 예시:
    #   llm_models = ["gpt-4o"]                              # 1개 모델
    #   llm_models = ["gpt-4o", "gpt-4o-mini"]               # 2개 모델
    #   llm_models = ["gpt-4o-mini", "gpt-4o-mini", "gpt-4o"] # 3개 모델 (중복 가능)
    #   llm_models = ["gpt-4o"] * 5                          # 5개 동일 모델
    
    llm_models = ["gpt-4o-mini", "gpt-5-mini", "gpt-4o-mini"]
    
    print(f"LLM 모델 초기화 ({len(llm_models)}개):")
    for idx, model_name in enumerate(llm_models):
        print(f"  {idx+1}. {model_name}")
    
    mllm_instances = [
        mLLM.multimodalLLM(llm_name=model_name, api_key=api_key)
        for model_name in llm_models
    ]
    
    # ========================================
    # 비디오 파일 설정
    # ========================================
    base_dir = r"/workspace/app/video_source"
    video_options = {
        "pMDI_10": base_dir + r"/pMDI/10_Foster_full.mov",
        "SMI_03": base_dir + r"/SMI/03_SMI_full.mov",
        "DPI_01": base_dir + r"/DPI/01_Ellipta_full.mov",
    }
    
    video_path = video_options["pMDI_10"]
    
    print(f"\n분석할 비디오: {video_path}")
    
    # ========================================
    # 워크플로우 실행
    # ========================================
    initial_state = create_initial_state(
        video_path=video_path,
        llm_models=llm_models,
        api_key=api_key
    )
    
    workflow = create_workflow(mllm_instances, llm_models)
    final_state = workflow.run(initial_state)
    
    # ========================================
    # 결과 출력
    # ========================================
    if final_state["status"] == "completed":
        print("\n✅ 분석이 성공적으로 완료되었습니다!")
        
        if final_state.get("final_report"):
            report = final_state["final_report"]
            print(f"\n총 {report['summary']['total_actions_detected']}개의 행동이 감지되었습니다.")
        
        print(f"\n총 {len(final_state['agent_logs'])}개의 Agent 로그가 기록되었습니다.")
        
    else:
        print("\n❌ 분석 중 오류가 발생했습니다.")
        if final_state.get("errors"):
            print("오류 목록:")
            for error in final_state["errors"]:
                print(f"  - {error}")
    
    print("\n분석 완료!")
    return final_state


if __name__ == "__main__":
    final_state = main()

