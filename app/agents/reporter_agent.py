#!/usr/bin/env python
# coding: utf-8

"""
Reporter Agent
분석 결과를 취합하고 시각화합니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
from .state import VideoAnalysisState


class ReporterAgent:
    """
    리포팅 전담 Agent
    - 결과 취합
    - Plotly 그래프 생성
    - JSON/CSV 리포트 출력
    """
    
    def __init__(self):
        self.name = "ReporterAgent"
    
    def process(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """
        최종 리포트 생성
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        try:
            state["agent_logs"].append({
                "agent": self.name,
                "action": "start_reporting",
                "message": "리포트 생성 시작"
            })
            
            # 최종 리포트 생성
            final_report = self._create_final_report(state)
            state["final_report"] = final_report
            
            # 시각화 생성
            visualization_fig = self._create_visualization(state)
            
            # 시각화 표시
            if visualization_fig:
                visualization_fig.show()
                state["visualization_path"] = "visualization_generated"
            
            state["status"] = "completed"
            
            state["agent_logs"].append({
                "agent": self.name,
                "action": "reporting_complete",
                "message": "리포트 생성 완료"
            })
            
            print(f"\n[{self.name}] 최종 리포트 생성 완료")
            self._print_summary(final_report)
            
        except Exception as e:
            error_msg = f"[{self.name}] 리포트 생성 중 오류: {str(e)}"
            state["errors"].append(error_msg)
            state["status"] = "error"
            print(error_msg)
            import traceback
            traceback.print_exc()
        
        return state
    
    def _create_final_report(self, state: VideoAnalysisState) -> dict:
        """최종 리포트 생성"""
        video_info = state["video_info"]
        reference_times = state["reference_times"]
        action_analysis = state["action_analysis_results"]
        
        return {
            "video_info": video_info,
            "reference_times": reference_times,
            "action_analysis": action_analysis,
            "summary": {
                "total_actions_detected": sum(
                    1 for action in action_analysis.values() 
                    if action['total_detections'] > 0
                ),
                "analysis_duration": video_info["play_time"]
            }
        }
    
    def _create_visualization(self, state: VideoAnalysisState):
        """Plotly 시각화 생성"""
        try:
            promptbank_data = state["promptbank_data"]
            video_info = state["video_info"]
            llm_name = state.get("llm_name", "gpt-4o")
            
            search_reference_time = promptbank_data["search_reference_time"]
            check_action_step_common = promptbank_data["check_action_step_common"]
            
            # 모든 키와 y 위치 설정
            reference_keys = list(search_reference_time.keys())
            action_keys = list(check_action_step_common.keys())
            all_keys = reference_keys + action_keys
            y_positions = {key: i * 0.1 for i, key in enumerate(all_keys)}
            
            play_time = video_info["play_time"]
            min_time, max_time = -1.0, play_time
            
            # Figure 생성
            fig = go.Figure()
            
            # 스트라이프 그리기
            for key, y_pos in y_positions.items():
                if key in reference_keys:
                    color = "blue"
                    opacity = 0.3
                else:
                    color = "gray"
                    opacity = 0.3
                
                fig.add_shape(
                    type="line",
                    x0=0, y0=y_pos, x1=1, y1=y_pos,
                    xref="paper", yref="y",
                    line=dict(color=color, width=10),
                    opacity=opacity
                )
            
            # Reference time 수직선 및 점 추가
            reference_times = []
            reference_y_pos = []
            reference_texts = []
            
            for key, value in search_reference_time.items():
                if value['reference_time'] >= 0:
                    y_pos = y_positions[key]
                    
                    # 수직선
                    fig.add_shape(
                        type="line",
                        x0=value['reference_time'], y0=min(y_positions.values()) - 0.05,
                        x1=value['reference_time'], y1=max(y_positions.values()) + 0.05,
                        line=dict(color="blue", width=1.5),
                        opacity=0.7
                    )
                    
                    reference_times.append(value['reference_time'])
                    reference_y_pos.append(y_pos)
                    reference_texts.append(f"{value['reference_time']:.1f}s")
            
            # Reference time 점들
            if reference_times:
                fig.add_trace(go.Scatter(
                    x=reference_times,
                    y=reference_y_pos,
                    mode='markers+text',
                    marker=dict(size=12, color='blue'),
                    text=reference_texts,
                    textposition="top center",
                    textfont=dict(size=9, color='blue'),
                    name='Reference Time',
                    showlegend=False,
                    hovertemplate='Reference Time: %{x:.1f}s<extra></extra>'
                ))
            
            # Action step 점들 추가
            action_times_filled = []
            action_y_pos_filled = []
            action_keys_filled = []
            action_confidence_filled = []
            action_times_empty = []
            action_y_pos_empty = []
            action_keys_empty = []
            action_confidence_empty = []
            
            # Confidence 딕셔너리 생성
            confidence_dict = {}
            for key, value in check_action_step_common.items():
                if value['confidence_score']:
                    confidence_dict[key] = {time: conf for time, conf in value['confidence_score']}
            
            for key, value in check_action_step_common.items():
                if value['time']:
                    y_pos = y_positions[key]
                    for time_val, score_val in zip(value['time'], value['score']):
                        time_val = float(time_val)
                        confidence_val = confidence_dict.get(key, {}).get(time_val, 0.5)
                        
                        if score_val == 1:
                            action_times_filled.append(time_val)
                            action_y_pos_filled.append(y_pos)
                            action_keys_filled.append(key)
                            action_confidence_filled.append(confidence_val)
                        elif score_val == 0:
                            action_times_empty.append(time_val)
                            action_y_pos_empty.append(y_pos)
                            action_keys_empty.append(key)
                            action_confidence_empty.append(confidence_val)
            
            # Score=1인 점들
            if action_times_filled:
                fig.add_trace(go.Scatter(
                    x=action_times_filled,
                    y=action_y_pos_filled,
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=action_confidence_filled,
                        colorscale='Greens',
                        cmin=0.0,
                        cmax=1.0,
                        symbol='circle',
                        colorbar=dict(
                            title="Confidence<br>(Score=1)",
                            x=1.02,
                            y=0.75,
                            len=0.4,
                            thickness=15
                        ),
                        line=dict(width=1, color='darkgreen')
                    ),
                    name='Action Steps (Score=1)',
                    showlegend=False,
                    hovertemplate='%{text}<br>Time: %{x:.1f}s<br>Score: 1<br>Confidence: %{marker.color:.2f}<extra></extra>',
                    text=action_keys_filled
                ))
            
            # Score=0인 점들
            if action_times_empty:
                fig.add_trace(go.Scatter(
                    x=action_times_empty,
                    y=action_y_pos_empty,
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=action_confidence_empty,
                        colorscale='Reds',
                        cmin=0.0,
                        cmax=1.0,
                        symbol='circle-open',
                        colorbar=dict(
                            title="Confidence<br>(Score=0)",
                            x=1.02,
                            y=0.25,
                            len=0.4,
                            thickness=15
                        ),
                        line=dict(width=2)
                    ),
                    name='Action Steps (Score=0)',
                    showlegend=False,
                    hovertemplate='%{text}<br>Time: %{x:.1f}s<br>Score: 0<br>Confidence: %{marker.color:.2f}<extra></extra>',
                    text=action_keys_empty
                ))
            
            # 레이아웃 설정
            fig.update_layout(
                title={
                    'text': f'[Multi-Agent] Visualization: Reference Time and Action Steps, {llm_name}',
                    'x': 0.5,
                    'font': {'size': 14, 'family': 'Arial'}
                },
                xaxis=dict(
                    title='time (sec)',
                    gridcolor='rgba(0,0,0,0.3)',
                    gridwidth=1,
                    range=[min_time, max_time],
                    showgrid=True
                ),
                yaxis=dict(
                    title='event',
                    tickmode='array',
                    tickvals=list(y_positions.values()),
                    ticktext=list(y_positions.keys()),
                    gridcolor='rgba(0,0,0,0.1)',
                    gridwidth=1
                ),
                plot_bgcolor='white',
                width=1000,
                height=600,
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            print(f"시각화 생성 중 오류: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _print_summary(self, report: dict):
        """요약 정보 출력"""
        print("\n" + "="*50)
        print("=== 비디오 분석 결과 요약 ===")
        print("="*50)
        
        # 비디오 정보
        video_info = report["video_info"]
        print(f"\n[비디오 정보]")
        print(f"  파일명: {video_info['video_name']}")
        print(f"  재생시간: {video_info['play_time']}초")
        print(f"  총 프레임: {video_info['frame_count']}")
        print(f"  해상도: {video_info['video_width']}x{video_info['video_height']}px")
        
        # 기준 시간
        reference_times = report["reference_times"]
        print(f"\n[기준 시간]")
        for key, value in reference_times.items():
            print(f"  {key}: {value}초")
        
        # 행동 분석
        print(f"\n[행동 분석]")
        print(f"  총 감지된 행동: {report['summary']['total_actions_detected']}개")
        
        print("\n" + "="*50)

