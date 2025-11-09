#!/usr/bin/env python
# coding: utf-8

"""
Action Analyzer Agent
개별 행동 단계를 분석합니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .state import VideoAnalysisState


class ActionAnalyzerAgent:
    """
    행동 단계 분석 전담 Agent
    - 개별 행동 인식
    - 신뢰도 평가
    - 시간대별 행동 매핑
    """
    
    def __init__(self):
        self.name = "ActionAnalyzerAgent"
    
    def process(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """
        행동 단계를 분석하고 결과를 상태에 저장
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        try:
            state["agent_logs"].append({
                "agent": self.name,
                "action": "start_analysis",
                "message": "행동 단계 분석 시작"
            })
            
            # PromptBank 데이터에서 행동 단계 정보 추출
            promptbank_data = state["promptbank_data"]
            
            if promptbank_data:
                # 행동 분석 결과 생성
                action_summary = self._create_action_summary(promptbank_data)
                
                state["action_analysis_results"] = action_summary
                state["status"] = "action_analyzed"
                
                state["agent_logs"].append({
                    "agent": self.name,
                    "action": "analysis_complete",
                    "message": f"행동 단계 분석 완료: {len(action_summary)}개 행동 인식"
                })
                
                print(f"[{self.name}] 행동 단계 분석 완료: {len(action_summary)}개 행동")
            else:
                raise ValueError("PromptBank 데이터가 없습니다")
            
        except Exception as e:
            error_msg = f"[{self.name}] 행동 단계 분석 중 오류: {str(e)}"
            state["errors"].append(error_msg)
            state["status"] = "error"
            print(error_msg)
        
        return state
    
    def _create_action_summary(self, promptbank_data: dict) -> dict:
        """
        PromptBank 데이터로부터 행동 요약 생성
        
        Args:
            promptbank_data: PromptBank 데이터
            
        Returns:
            행동 요약 딕셔너리
        """
        action_summary = {}
        check_action_step_common = promptbank_data.get("check_action_step_common", {})
        
        for action_key, action_data in check_action_step_common.items():
            if action_data['time']:  # 데이터가 있는 경우만
                # YES(score=1)인 시간들 추출
                yes_times = [
                    time_val for time_val, score_val in zip(action_data['time'], action_data['score'])
                    if score_val == 1
                ]
                
                # NO(score=0)인 시간들 추출
                no_times = [
                    time_val for time_val, score_val in zip(action_data['time'], action_data['score'])
                    if score_val == 0
                ]
                
                # Confidence 정보
                confidence_info = {}
                if action_data.get('confidence_score'):
                    confidence_info = {
                        time: conf for time, conf in action_data['confidence_score']
                    }
                
                action_summary[action_key] = {
                    'action_description': action_data['action'],
                    'detected_times': yes_times,
                    'not_detected_times': no_times,
                    'confidence': confidence_info,
                    'total_detections': len(yes_times)
                }
        
        return action_summary

