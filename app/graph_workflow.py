#!/usr/bin/env python
# coding: utf-8

"""
LangGraph Workflow 정의
Multi-Agent 워크플로우를 구성합니다.
"""

from langgraph.graph import StateGraph, END
from agents.state import VideoAnalysisState
from agents.video_processor_agent import VideoProcessorAgent
from agents.video_analyzer_agent_4o import VideoAnalyzerAgent4o
from agents.video_analyzer_agent_4o_mini import VideoAnalyzerAgent4oMini
from agents.reporter_agent import ReporterAgent


class InhalerAnalysisWorkflow:
    """
    흡입기 비디오 분석 워크플로우
    
    워크플로우:
    1. VideoProcessor: 비디오 메타데이터 추출
    2. VideoAnalyzer (병렬):
       - VideoAnalyzer4o: GPT-4o를 사용한 분석
       - VideoAnalyzer4oMini: GPT-4o-mini를 사용한 분석
    3. Reporter: 결과 취합 및 평균값 시각화
    """
    
    def __init__(self, mllm_4o, mllm_4o_mini):
        """
        워크플로우 초기화
        
        Args:
            mllm_4o: GPT-4o Multimodal LLM 인스턴스
            mllm_4o_mini: GPT-4o-mini Multimodal LLM 인스턴스
        """
        self.mllm_4o = mllm_4o
        self.mllm_4o_mini = mllm_4o_mini
        
        # Agent 초기화
        self.video_processor = VideoProcessorAgent()
        self.video_analyzer_4o = VideoAnalyzerAgent4o(mllm_4o, self.video_processor)
        self.video_analyzer_4o_mini = VideoAnalyzerAgent4oMini(mllm_4o_mini, self.video_processor)
        self.reporter = ReporterAgent()
        
        # 워크플로우 그래프 생성
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile()
    
    def _create_workflow(self):
        """LangGraph 워크플로우 생성 (병렬 처리)"""
        
        # StateGraph 생성
        workflow = StateGraph(VideoAnalysisState)
        
        # 노드 추가
        workflow.add_node("video_processor", self._video_processor_node)
        workflow.add_node("video_analyzer_4o", self._video_analyzer_4o_node)
        workflow.add_node("video_analyzer_4o_mini", self._video_analyzer_4o_mini_node)
        workflow.add_node("reporter", self._reporter_node)
        
        # 엣지 추가 (워크플로우 순서)
        workflow.set_entry_point("video_processor")
        # 병렬 실행: video_processor -> 두 analyzer가 병렬로 실행
        workflow.add_edge("video_processor", "video_analyzer_4o")
        workflow.add_edge("video_processor", "video_analyzer_4o_mini")
        # 두 analyzer 결과를 reporter로 전달
        workflow.add_edge("video_analyzer_4o", "reporter")
        workflow.add_edge("video_analyzer_4o_mini", "reporter")
        workflow.add_edge("reporter", END)
        
        return workflow
    
    def _video_processor_node(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """비디오 처리 노드"""
        print("\n" + "="*50)
        print("=== 1. Video Processor Agent 실행 ===")
        print("="*50)
        return self.video_processor.process(state)
    
    def _video_analyzer_4o_node(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """비디오 분석 노드 - GPT-4o"""
        print("\n" + "="*50)
        print("=== 2-1. Video Analyzer Agent (GPT-4o) 실행 ===")
        print("="*50)
        return self.video_analyzer_4o.process(state)
    
    def _video_analyzer_4o_mini_node(self, state: VideoAnalysisState) -> VideoAnalysisState:
        """비디오 분석 노드 - GPT-4o-mini"""
        print("\n" + "="*50)
        print("=== 2-2. Video Analyzer Agent (GPT-4o-mini) 실행 ===")
        print("="*50)
        return self.video_analyzer_4o_mini.process(state)
    
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


def create_workflow(mllm_4o, mllm_4o_mini) -> InhalerAnalysisWorkflow:
    """
    워크플로우 생성 헬퍼 함수
    
    Args:
        mllm_4o: GPT-4o Multimodal LLM 인스턴스
        mllm_4o_mini: GPT-4o-mini Multimodal LLM 인스턴스
        
    Returns:
        InhalerAnalysisWorkflow 인스턴스
    """
    return InhalerAnalysisWorkflow(mllm_4o, mllm_4o_mini)

