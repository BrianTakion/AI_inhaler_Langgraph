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
        최종 리포트 생성 (두 agent의 평균값 사용)
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        try:
            state["agent_logs"].append({
                "agent": self.name,
                "action": "start_reporting",
                "message": "리포트 생성 시작 (평균값 계산)"
            })
            
            # 두 agent의 결과를 평균내기
            print(f"\n[{self.name}] 두 Agent 결과의 평균값 계산 중...")
            avg_data = self._compute_average(state)
            state["reference_times_avg"] = avg_data["reference_times_avg"]
            state["promptbank_data_avg"] = avg_data["promptbank_data_avg"]
            
            # 최종 리포트 생성
            final_report = self._create_final_report(state)
            state["final_report"] = final_report
            
            # 시각화 생성 (평균값 사용)
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
            
            print(f"\n[{self.name}] 최종 리포트 생성 완료 (평균값 기반)")
            self._print_summary(final_report)
            
        except Exception as e:
            error_msg = f"[{self.name}] 리포트 생성 중 오류: {str(e)}"
            state["errors"].append(error_msg)
            state["status"] = "error"
            print(error_msg)
            import traceback
            traceback.print_exc()
        
        return state
    
    def _compute_average(self, state: VideoAnalysisState) -> dict:
        """
        두 Agent의 결과를 평균내기
        
        Args:
            state: 현재 상태
            
        Returns:
            평균값 딕셔너리
        """
        # Reference times 평균
        ref_times_4o = state.get("reference_times_4o", {})
        ref_times_4o_mini = state.get("reference_times_4o_mini", {})
        
        reference_times_avg = {}
        for key in set(list(ref_times_4o.keys()) + list(ref_times_4o_mini.keys())):
            val_4o = ref_times_4o.get(key, 0)
            val_4o_mini = ref_times_4o_mini.get(key, 0)
            reference_times_avg[key] = round((val_4o + val_4o_mini) / 2.0, 1)
        
        # PromptBank 데이터 평균
        promptbank_4o = state.get("promptbank_data_4o", {})
        promptbank_4o_mini = state.get("promptbank_data_4o_mini", {})
        
        # search_reference_time 평균
        search_ref_4o = promptbank_4o.get("search_reference_time", {})
        search_ref_4o_mini = promptbank_4o_mini.get("search_reference_time", {})
        
        search_reference_time_avg = {}
        for key in set(list(search_ref_4o.keys()) + list(search_ref_4o_mini.keys())):
            ref_4o = search_ref_4o.get(key, {})
            ref_4o_mini = search_ref_4o_mini.get(key, {})
            
            avg_ref_time = round(
                (ref_4o.get('reference_time', 0) + ref_4o_mini.get('reference_time', 0)) / 2.0, 
                1
            )
            
            search_reference_time_avg[key] = {
                'action': ref_4o.get('action', ref_4o_mini.get('action', '')),
                'reference_time': avg_ref_time
            }
        
        # check_action_step_common 평균
        check_4o = promptbank_4o.get("check_action_step_common", {})
        check_4o_mini = promptbank_4o_mini.get("check_action_step_common", {})
        
        check_action_step_common_avg = {}
        for action_key in set(list(check_4o.keys()) + list(check_4o_mini.keys())):
            action_4o = check_4o.get(action_key, {})
            action_4o_mini = check_4o_mini.get(action_key, {})
            
            # time과 score를 합치고 평균 계산
            time_4o = action_4o.get('time', [])
            score_4o = action_4o.get('score', [])
            conf_4o = dict(action_4o.get('confidence_score', []))
            
            time_4o_mini = action_4o_mini.get('time', [])
            score_4o_mini = action_4o_mini.get('score', [])
            conf_4o_mini = dict(action_4o_mini.get('confidence_score', []))
            
            # 모든 시간값 수집
            all_times = set(time_4o + time_4o_mini)
            
            time_avg = []
            score_avg = []
            confidence_avg = []
            
            for t in sorted(all_times):
                # 각 시간에 대한 score와 confidence 찾기
                scores = []
                confidences = []
                
                if t in time_4o:
                    idx = time_4o.index(t)
                    scores.append(score_4o[idx])
                    confidences.append(conf_4o.get(t, 0.5))
                
                if t in time_4o_mini:
                    idx = time_4o_mini.index(t)
                    scores.append(score_4o_mini[idx])
                    confidences.append(conf_4o_mini.get(t, 0.5))
                
                # 평균 계산
                avg_score = sum(scores) / len(scores) if scores else 0
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
                
                # 반올림하여 0 또는 1로 변환
                time_avg.append(t)
                score_avg.append(1 if avg_score >= 0.5 else 0)
                confidence_avg.append((t, round(avg_confidence, 2)))
            
            check_action_step_common_avg[action_key] = {
                'action': action_4o.get('action', action_4o_mini.get('action', '')),
                'time': time_avg,
                'score': score_avg,
                'confidence_score': confidence_avg
            }
        
        promptbank_data_avg = {
            "search_reference_time": search_reference_time_avg,
            "check_action_step_common": check_action_step_common_avg
        }
        
        return {
            "reference_times_avg": reference_times_avg,
            "promptbank_data_avg": promptbank_data_avg
        }
    
    def _create_final_report(self, state: VideoAnalysisState) -> dict:
        """최종 리포트 생성 (평균값 기반)"""
        video_info = state["video_info"]
        reference_times_avg = state.get("reference_times_avg", {})
        promptbank_data_avg = state.get("promptbank_data_avg", {})
        
        # 평균 데이터로부터 action_analysis 생성
        action_analysis = {}
        if promptbank_data_avg:
            check_action_step_common = promptbank_data_avg.get("check_action_step_common", {})
            for action_key, action_data in check_action_step_common.items():
                if action_data.get('time'):
                    yes_times = [
                        time_val for time_val, score_val in zip(action_data['time'], action_data['score'])
                        if score_val == 1
                    ]
                    no_times = [
                        time_val for time_val, score_val in zip(action_data['time'], action_data['score'])
                        if score_val == 0
                    ]
                    confidence_info = {
                        time: conf for time, conf in action_data.get('confidence_score', [])
                    }
                    action_analysis[action_key] = {
                        'action_description': action_data['action'],
                        'detected_times': yes_times,
                        'not_detected_times': no_times,
                        'confidence': confidence_info,
                        'total_detections': len(yes_times)
                    }
        
        return {
            "video_info": video_info,
            "reference_times": reference_times_avg,
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
        """Plotly 시각화 생성 (평균값 기반)"""
        try:
            promptbank_data_avg = state.get("promptbank_data_avg")
            if not promptbank_data_avg:
                print("평균 PromptBank 데이터가 없습니다.")
                return None
            
            video_info = state["video_info"]
            llm_name = "gpt-4o & gpt-4o-mini (Average)"
            
            search_reference_time = promptbank_data_avg["search_reference_time"]
            check_action_step_common = promptbank_data_avg["check_action_step_common"]
            
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
                        color=action_confidence_filled,  # Confidence 값으로 내부 색상 설정
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
                        line=dict(
                            width=1,
                            color=action_confidence_filled,  # 테두리도 Confidence로 설정
                            colorscale='Greens',
                            cmin=0.0,
                            cmax=1.0
                        )
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
                        color=action_confidence_empty,  # Confidence 값으로 내부 색상 설정
                        colorscale='Reds',
                        cmin=0.0,
                        cmax=1.0,
                        symbol='circle',  # 채워진 원으로 변경 (내부 색상 보이도록)
                        colorbar=dict(
                            title="Confidence<br>(Score=0)",
                            x=1.02,
                            y=0.25,
                            len=0.4,
                            thickness=15
                        ),
                        line=dict(
                            width=1,  # 테두리 두께를 Score=1과 동일하게 조정
                            color=action_confidence_empty,  # 테두리도 Confidence로 설정
                            colorscale='Reds',
                            cmin=0.0,
                            cmax=1.0
                        )
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

