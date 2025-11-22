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
from datetime import datetime
from .state import VideoAnalysisState


class ReporterAgent:
    """
    리포팅 전담 Agent
    - 결과 취합
    - Plotly 그래프 생성
    - JSON/CSV 리포트 출력
    """
    
    # Reference 순서 정의 (밑에서 위로)
    REFERENCE_ORDER = ['inhalerIN', 'faceONinhaler', 'inhalerOUT']
    
    # 액션 순서 정의 (밑에서 위로)
    ACTION_ORDER = [
        'sit_stand', 'remove_cover', 'inspect_mouthpiece', 
        'hold_inhaler', 'load_dose',
        'exhale_before', 'seal_lips', 'inhale_deeply',
        'remove_inhaler', 'hold_breath', 'exhale_after',
        'replace_cover'
    ]
    
    def __init__(self):
        self.name = "ReporterAgent"
    
    def process(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """
        최종 리포트 생성 (여러 모델의 평균값 사용)
        
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
            
            # 모든 모델의 결과를 평균내기
            num_models = len(state.get("model_results", {}))
            print(f"\n[{self.name}] {num_models}개 모델 결과의 평균값 계산 중...")
            avg_data = self._compute_average(state)
            state["reference_times_avg"] = avg_data["reference_times_avg"]
            state["promptbank_data_avg"] = avg_data["promptbank_data_avg"]
            
            # 최종 리포트 생성
            final_report = self._create_final_report(state)
            state["final_report"] = final_report
            
            # 시각화 생성 (평균값 사용)
            visualization_fig = self._create_visualization(state)
            
            # 시각화 표시 및 HTML 파일로 저장
            if visualization_fig:
                # HTML 파일로 저장 (MMDD_HHMM 타임스탬프 포함)
                video_info = state["video_info"]
                timestamp_suffix = datetime.now().strftime("%m%d_%H%M")
                html_filename = f"visualization_{video_info['video_name']}_{timestamp_suffix}.html"
                html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), html_filename)
                visualization_fig.write_html(html_path)
                
                # 파일 경로 프린트
                print(f"\n[{self.name}] 시각화 HTML 파일 저장됨:")
                print(f"  파일 경로: {html_path}")
                print(f"  브라우저에서 열기: file://{html_path}")
                
                # 브라우저에서도 표시
                visualization_fig.show()
                
                state["visualization_path"] = html_path
            
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
        여러 Agent의 결과를 동적으로 평균내기
        
        Args:
            state: 현재 상태
            
        Returns:
            평균값 딕셔너리
        """
        model_results = state.get("model_results", {})
        
        if not model_results:
            raise ValueError("모델 결과가 없습니다.")
        
        num_models = len(model_results)
        print(f"[ReporterAgent] {num_models}개 모델의 결과를 평균 계산 중...")
        
        # Reference times 평균
        reference_times_avg = {}
        all_ref_time_keys = set()
        for model_id, result in model_results.items():
            ref_times = result.get("reference_times", {})
            all_ref_time_keys.update(ref_times.keys())
        
        for key in all_ref_time_keys:
            values = []
            for model_id, result in model_results.items():
                ref_times = result.get("reference_times", {})
                if key in ref_times:
                    values.append(ref_times[key])
            reference_times_avg[key] = round(sum(values) / len(values), 1) if values else 0
        
        # PromptBank 데이터 평균
        # search_reference_time 평균
        search_reference_time_avg = {}
        all_search_ref_keys = set()
        for model_id, result in model_results.items():
            promptbank = result.get("promptbank_data", {})
            search_ref = promptbank.get("search_reference_time", {})
            all_search_ref_keys.update(search_ref.keys())
        
        for key in all_search_ref_keys:
            ref_times = []
            action = None
            for model_id, result in model_results.items():
                promptbank = result.get("promptbank_data", {})
                search_ref = promptbank.get("search_reference_time", {})
                if key in search_ref:
                    ref_times.append(search_ref[key].get('reference_time', 0))
                    if action is None:
                        action = search_ref[key].get('action', '')
            
            avg_ref_time = round(sum(ref_times) / len(ref_times), 1) if ref_times else 0
            search_reference_time_avg[key] = {
                'action': action or '',
                'reference_time': avg_ref_time
            }
        
        # check_action_step_DPI_type3 평균
        check_action_step_DPI_type3_avg = {}
        all_action_keys = set()
        for model_id, result in model_results.items():
            promptbank = result.get("promptbank_data", {})
            check_action = promptbank.get("check_action_step_DPI_type3", {})
            all_action_keys.update(check_action.keys())
        
        for action_key in all_action_keys:
            # 모든 모델에서 해당 action_key의 데이터 수집
            all_times_scores = {}  # {time: [(score, confidence), ...]}
            action_description = None
            
            for model_id, result in model_results.items():
                promptbank = result.get("promptbank_data", {})
                check_action = promptbank.get("check_action_step_DPI_type3", {})
                if action_key in check_action:
                    action_data = check_action[action_key]
                    if action_description is None:
                        action_description = action_data.get('action', '')
                    
                    times = action_data.get('time', [])
                    scores = action_data.get('score', [])
                    confidences = dict(action_data.get('confidence_score', []))
                    
                    for i, t in enumerate(times):
                        if t not in all_times_scores:
                            all_times_scores[t] = []
                        score = scores[i] if i < len(scores) else 0
                        confidence = confidences.get(t, 0.5)
                        all_times_scores[t].append((score, confidence))
            
            # 각 시간에 대해 평균 계산
            time_avg = []
            score_avg = []
            confidence_avg = []
            
            for t in sorted(all_times_scores.keys()):
                score_conf_list = all_times_scores[t]
                scores = [sc[0] for sc in score_conf_list]
                confidences = [sc[1] for sc in score_conf_list]
                
                avg_score = sum(scores) / len(scores) if scores else 0
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
                
                time_avg.append(t)
                score_avg.append(1 if avg_score >= 0.5 else 0)
                confidence_avg.append((t, round(avg_confidence, 2)))
            
            check_action_step_DPI_type3_avg[action_key] = {
                'action': action_description or '',
                'time': time_avg,
                'score': score_avg,
                'confidence_score': confidence_avg
            }
        
        promptbank_data_avg = {
            "search_reference_time": search_reference_time_avg,
            "check_action_step_DPI_type3": check_action_step_DPI_type3_avg
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
            check_action_step_DPI_type3 = promptbank_data_avg.get("check_action_step_DPI_type3", {})
            for action_key, action_data in check_action_step_DPI_type3.items():
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
        """Plotly 시각화 생성 (여러 모델의 평균값 기반)"""
        try:
            promptbank_data_avg = state.get("promptbank_data_avg")
            if not promptbank_data_avg:
                print("평균 PromptBank 데이터가 없습니다.")
                return None
            
            video_info = state["video_info"]
            llm_name = state.get("llm_name", "Multiple Models (Average)")
            
            search_reference_time = promptbank_data_avg["search_reference_time"]
            check_action_step_DPI_type3 = promptbank_data_avg["check_action_step_DPI_type3"]
            
            # 모든 키와 y 위치 설정 (REFERENCE_ORDER, ACTION_ORDER 순서 적용, 밑에서 위로)
            reference_keys = list(search_reference_time.keys())
            action_keys = list(check_action_step_DPI_type3.keys())
            
            # REFERENCE_ORDER에 따라 reference_keys 정렬
            ordered_reference_keys = []
            for ref in self.REFERENCE_ORDER:
                if ref in reference_keys:
                    ordered_reference_keys.append(ref)
            
            # REFERENCE_ORDER에 없는 reference_keys도 추가
            for key in reference_keys:
                if key not in ordered_reference_keys:
                    ordered_reference_keys.append(key)
            
            # ACTION_ORDER에 따라 action_keys 정렬
            ordered_action_keys = []
            for action in self.ACTION_ORDER:
                if action in action_keys:
                    ordered_action_keys.append(action)
            
            # ACTION_ORDER에 없는 action_keys도 추가
            for key in action_keys:
                if key not in ordered_action_keys:
                    ordered_action_keys.append(key)
            
            # 전체 순서: reference_keys + action_keys (밑에서 위로)
            ordered_keys = ordered_reference_keys + ordered_action_keys
            
            # y 위치 할당 (밑에서 위로)
            y_positions = {key: i * 0.1 for i, key in enumerate(ordered_keys)}
            
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
            for key, value in check_action_step_DPI_type3.items():
                if value['confidence_score']:
                    confidence_dict[key] = {time: conf for time, conf in value['confidence_score']}
            
            for key, value in check_action_step_DPI_type3.items():
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

