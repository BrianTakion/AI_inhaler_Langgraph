#!/usr/bin/env python
# coding: utf-8

"""
LangGraph Workflow 정의
Multi-Agent 워크플로우를 구성합니다.
"""

from langgraph.graph import StateGraph, END
from agents.state import VideoAnalysisState
from agents.video_processor_agent import VideoProcessorAgent
from agents.video_analyzer_agent import VideoAnalyzerAgent
from agents.reporter_agent import ReporterAgent


class InhalerAnalysisWorkflow:
    """
    흡입기 비디오 분석 워크플로우
    
    워크플로우:
    1. VideoProcessor: 비디오 메타데이터 추출
    2. VideoAnalyzer: 기준 시점 탐지 및 행동 단계 분석 (통합)
    3. Reporter: 결과 취합 및 시각화
    """
    
    def __init__(self, mllm):
        """
        워크플로우 초기화
        
        Args:
            mllm: Multimodal LLM 인스턴스
        """
        self.mllm = mllm
        
        # Agent 초기화
        self.video_processor = VideoProcessorAgent()
        self.video_analyzer = VideoAnalyzerAgent(mllm, self.video_processor)
        self.reporter = ReporterAgent()
        
        # 워크플로우 그래프 생성
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile()
    
    def _create_workflow(self):
        """LangGraph 워크플로우 생성"""
        
        # StateGraph 생성
        workflow = StateGraph(VideoAnalysisState)
        
        # 노드 추가
        workflow.add_node("video_processor", self._video_processor_node)
        workflow.add_node("video_analyzer", self._video_analyzer_node)
        workflow.add_node("reporter", self._reporter_node)
        
        # 엣지 추가 (워크플로우 순서)
        workflow.set_entry_point("video_processor")
        workflow.add_edge("video_processor", "video_analyzer")
        workflow.add_edge("video_analyzer", "reporter")
        workflow.add_edge("reporter", END)
        
        return workflow
    
    def _video_processor_node(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """비디오 처리 노드"""
        print("\n" + "="*50)
        print("=== 1. Video Processor Agent 실행 ===")
        print("="*50)
        return self.video_processor.process(state)
    
    def _video_analyzer_node(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """비디오 분석 노드 (기준 시점 탐지 + 행동 분석 통합)"""
        print("\n" + "="*50)
        print("=== 2. Video Analyzer Agent 실행 ===")
        print("="*50)
        return self.video_analyzer.process(state)
    
    def _reporter_node(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """리포트 생성 노드"""
        print("\n" + "="*50)
        print("=== 3. Reporter Agent 실행 ===")
        print("="*50)
        return self.reporter.process(state)
    
    def run(self, initial_state: VideoAnalysisState) -> VideoAnalysisState:
        """
        워크플로우 실행
        
        Args:
            initial_state: 초기 상태
            
        Returns:
            최종 상태
        """
        print("\n" + "#"*50)
        print("### LangGraph Multi-Agent 워크플로우 시작 ###")
        print("#"*50)
        
        # 워크플로우 실행
        final_state = self.app.invoke(initial_state)
        
        print("\n" + "#"*50)
        print("### LangGraph Multi-Agent 워크플로우 완료 ###")
        print("#"*50)
        
        # 에러 확인
        if final_state.get("errors"):
            print("\n[경고] 다음 오류가 발생했습니다:")
            for error in final_state["errors"]:
                print(f"  - {error}")
        
        return final_state
    
    def visualize_workflow(self, output_path: str = "workflow_diagram.png"):
        """
        워크플로우 다이어그램 생성 (선택적)
        
        Args:
            output_path: 출력 파일 경로
        """
        try:
            from IPython.display import Image, display
            
            # 워크플로우 시각화
            display(Image(self.app.get_graph().draw_mermaid_png()))
            print(f"워크플로우 다이어그램이 생성되었습니다.")
        except Exception as e:
            print(f"워크플로우 시각화 실패: {e}")


def create_workflow(mllm) -> InhalerAnalysisWorkflow:
    """
    워크플로우 생성 헬퍼 함수
    
    Args:
        mllm: Multimodal LLM 인스턴스
        
    Returns:
        InhalerAnalysisWorkflow 인스턴스
    """
    return InhalerAnalysisWorkflow(mllm)

