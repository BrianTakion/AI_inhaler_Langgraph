#!/usr/bin/env python
# coding: utf-8

"""
LangGraph State 정의
모든 Agent가 공유하는 상태를 정의합니다.
"""

from typing import TypedDict, List, Dict, Any, Optional
from typing_extensions import Annotated
import operator


def keep_first(left: Any, right: Any) -> Any:
    """병렬 실행 시 첫 번째 유효한 값 유지"""
    # right가 비어있거나 None이면 left 유지
    if right is None or (isinstance(right, str) and right == ""):
        return left
    # left가 비어있거나 None이면 right 사용
    if left is None or (isinstance(left, str) and left == ""):
        return right
    # 둘 다 유효하면 left 우선 (첫 번째 값 유지)
    return left


def keep_non_none(left: Any, right: Any) -> Any:
    """병렬 실행 시 None이 아닌 값 우선"""
    if right is not None:
        return right
    if left is not None:
        return left
    return None


class VideoAnalysisState(TypedDict):
    """
    비디오 분석을 위한 공유 상태
    
    Attributes:
        video_path: 분석할 비디오 파일 경로
        video_info: 비디오 메타데이터 (이름, 재생시간, 프레임수, 해상도 등)
        
        # Reference Time 관련 (병렬 agent용)
        reference_times_4o: 기준 시간들 - gpt-4o
        reference_times_4o_mini: 기준 시간들 - gpt-4o-mini
        reference_detection_results: 각 기준 시간 탐지 결과
        
        # Action Analysis 관련 (병렬 agent용)
        action_analysis_results_4o: 행동 단계 분석 결과 - gpt-4o
        action_analysis_results_4o_mini: 행동 단계 분석 결과 - gpt-4o-mini
        q_answers_accumulated_4o: 누적된 Q&A 결과 - gpt-4o
        q_answers_accumulated_4o_mini: 누적된 Q&A 결과 - gpt-4o-mini
        
        # PromptBank (병렬 agent용)
        promptbank_data_4o: PromptBank 데이터 - gpt-4o
        promptbank_data_4o_mini: PromptBank 데이터 - gpt-4o-mini
        
        # 평균 결과
        reference_times_avg: 평균 기준 시간들
        promptbank_data_avg: 평균 PromptBank 데이터
        
        # 최종 결과
        final_report: 최종 분석 리포트
        visualization_path: 시각화 결과 경로
        
        # 메타데이터
        errors: 발생한 오류들
        status: 현재 처리 상태
        agent_logs: 각 Agent의 로그
    """
    # 입력 (병렬 실행 시 첫 번째 값 유지)
    video_path: Annotated[str, keep_first]
    llm_name: Annotated[Optional[str], keep_first]
    api_key: Annotated[Optional[str], keep_first]
    
    # 비디오 정보 (병렬 실행 시 첫 번째 값 유지)
    video_info: Annotated[Optional[Dict[str, Any]], keep_first]
    
    # Reference Time (병렬)
    reference_times_4o: Annotated[Dict[str, float], operator.or_]
    reference_times_4o_mini: Annotated[Dict[str, float], operator.or_]
    reference_detection_results: Annotated[Dict[str, Dict], operator.or_]
    
    # Action Analysis (병렬)
    action_analysis_results_4o: Annotated[Dict[str, Any], operator.or_]
    action_analysis_results_4o_mini: Annotated[Dict[str, Any], operator.or_]
    q_answers_accumulated_4o: Annotated[Dict[str, Dict], operator.or_]
    q_answers_accumulated_4o_mini: Annotated[Dict[str, Dict], operator.or_]
    
    # PromptBank (병렬 실행 시 None이 아닌 값 우선)
    promptbank_data_4o: Annotated[Optional[Dict[str, Any]], keep_non_none]
    promptbank_data_4o_mini: Annotated[Optional[Dict[str, Any]], keep_non_none]
    
    # 평균 결과 (병렬 실행 시 None이 아닌 값 우선)
    reference_times_avg: Annotated[Optional[Dict[str, float]], keep_non_none]
    promptbank_data_avg: Annotated[Optional[Dict[str, Any]], keep_non_none]
    
    # 최종 결과 (병렬 실행 시 None이 아닌 값 우선)
    final_report: Annotated[Optional[Dict[str, Any]], keep_non_none]
    visualization_path: Annotated[Optional[str], keep_non_none]
    
    # 메타데이터
    errors: Annotated[List[str], operator.add]
    status: Annotated[str, keep_non_none]
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
        reference_times_4o={},
        reference_times_4o_mini={},
        reference_detection_results={},
        action_analysis_results_4o={},
        action_analysis_results_4o_mini={},
        q_answers_accumulated_4o={},
        q_answers_accumulated_4o_mini={},
        promptbank_data_4o=None,
        promptbank_data_4o_mini=None,
        reference_times_avg=None,
        promptbank_data_avg=None,
        final_report=None,
        visualization_path=None,
        errors=[],
        status="initialized",
        agent_logs=[]
    )

