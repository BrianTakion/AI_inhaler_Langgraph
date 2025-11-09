#!/usr/bin/env python
# coding: utf-8

"""
LangGraph State 정의
모든 Agent가 공유하는 상태를 정의합니다.
"""

from typing import TypedDict, List, Dict, Any, Optional
from typing_extensions import Annotated
import operator


class VideoAnalysisState(TypedDict):
    """
    비디오 분석을 위한 공유 상태
    
    Attributes:
        video_path: 분석할 비디오 파일 경로
        video_info: 비디오 메타데이터 (이름, 재생시간, 프레임수, 해상도 등)
        
        # Reference Time 관련
        reference_times: 기준 시간들 (inhalerIN, faceONinhaler, inhalerOUT)
        reference_detection_results: 각 기준 시간 탐지 결과
        
        # Action Analysis 관련
        action_analysis_results: 행동 단계 분석 결과
        q_answers_accumulated: 누적된 Q&A 결과
        
        # PromptBank
        promptbank_data: PromptBank 데이터
        
        # 최종 결과
        final_report: 최종 분석 리포트
        visualization_path: 시각화 결과 경로
        
        # 메타데이터
        errors: 발생한 오류들
        status: 현재 처리 상태
        agent_logs: 각 Agent의 로그
    """
    # 입력
    video_path: str
    llm_name: Optional[str]
    api_key: Optional[str]
    
    # 비디오 정보
    video_info: Optional[Dict[str, Any]]
    
    # Reference Time
    reference_times: Annotated[Dict[str, float], operator.or_]
    reference_detection_results: Annotated[Dict[str, Dict], operator.or_]
    
    # Action Analysis
    action_analysis_results: Annotated[Dict[str, Any], operator.or_]
    q_answers_accumulated: Annotated[Dict[str, Dict], operator.or_]
    
    # PromptBank
    promptbank_data: Optional[Dict[str, Any]]
    
    # 최종 결과
    final_report: Optional[Dict[str, Any]]
    visualization_path: Optional[str]
    
    # 메타데이터
    errors: Annotated[List[str], operator.add]
    status: str
    agent_logs: Annotated[List[Dict[str, str]], operator.add]


def create_initial_state(video_path: str, llm_name: str = "gpt-4o", api_key: str = None) -> VideoAnalysisState:
    """
    초기 상태 생성
    
    Args:
        video_path: 비디오 파일 경로
        llm_name: 사용할 LLM 모델 이름
        api_key: OpenAI API 키
        
    Returns:
        초기화된 VideoAnalysisState
    """
    return VideoAnalysisState(
        video_path=video_path,
        llm_name=llm_name,
        api_key=api_key,
        video_info=None,
        reference_times={},
        reference_detection_results={},
        action_analysis_results={},
        q_answers_accumulated={},
        promptbank_data=None,
        final_report=None,
        visualization_path=None,
        errors=[],
        status="initialized",
        agent_logs=[]
    )

