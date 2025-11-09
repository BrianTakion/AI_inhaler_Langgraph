#!/usr/bin/env python
# coding: utf-8

"""
LangGraph 기반 Multi-Agent 흡입기 비디오 분석기
"""

import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다. .env 파일에 'OPENAI_API_KEY=your-key' 형식으로 추가하세요.")

# 모듈 임포트
import class_MultimodalLLM_QA_251107 as mLLM
from agents.state import create_initial_state
from graph_workflow import create_workflow


def main():
    """메인 실행 함수"""
    
    # LLM 초기화
    llm_name = "gpt-4o"
    print(f"LLM 모델 초기화: {llm_name}")
    mllm = mLLM.multimodalLLM(llm_name=llm_name, api_key=api_key)
    
    # 비디오 파일 경로 설정
    base_dir = r"/workspace/app/video_source"
    
    # 비디오 선택 (여러 옵션 중 선택)
    video_options = {
        "pMDI_10": base_dir + r"/pMDI/10_Foster_full.mov",
        "SMI_03": base_dir + r"/SMI/03_SMI_full.mov",
        "DPI_01": base_dir + r"/DPI/01_Ellipta_full.mov",
    }
    
    # 사용할 비디오 선택
    video_path = video_options["pMDI_10"]
    
    print(f"\n분석할 비디오: {video_path}")
    
    # 초기 상태 생성
    initial_state = create_initial_state(
        video_path=video_path,
        llm_name=llm_name,
        api_key=api_key
    )
    
    # 워크플로우 생성
    workflow = create_workflow(mllm)
    
    # 워크플로우 실행
    final_state = workflow.run(initial_state)
    
    # 결과 확인
    if final_state["status"] == "completed":
        print("\n✅ 분석이 성공적으로 완료되었습니다!")
        
        # 최종 리포트 정보
        if final_state.get("final_report"):
            report = final_state["final_report"]
            print(f"\n총 {report['summary']['total_actions_detected']}개의 행동이 감지되었습니다.")
        
        # Agent 로그 요약
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

