import os, re
from IPython.display import Image, display
import class_Media_Edit_250809 as ME
import class_MultimodalLLM_QA_250809 as mLLM
import class_PromptBank_250809 as PromptBank

api_key = os.getenv('OPENAI_API_KEY')
llm_name = "gpt-4o"  
mllm = mLLM.multimodalLLM(llm_name=llm_name, api_key=api_key)

def search_reference_time_check_action_step(system_prompt, user_prompt, play_time, start_time=0, segment_time=4, offset_time=2, show=True):
    """
    비디오에서 기준 시간을 찾고 행동 단계를 판단하는 함수
    Args:
        system_prompt (str): GPT 시스템 프롬프트
        user_prompt (str): GPT 사용자 프롬프트
        play_time (float): 비디오 재생 시간(초)
        start_time (float): 검색 시작 시간(초)
        segment_time (float): 분석할 구간 길이(초)
        offset_time (float): 검색 시 이동할 시간 간격(초)
        imageShow (bool): 이미지 표시 여부
    Returns:
        float: reference_time(초)
        dict: 행동 단계 판단 결과(키: action_step, 값: action, score: list, time: list)
    """
    #output_dir_temp = "output_video_MxN_image_for_reference_time"
    M, N = 1, int(segment_time * 2)  # 0.5초 간격으로 추출하여 판단
    gridSize = (int(1920/2)*N, int(1080/2)*M)

    while start_time <= play_time - segment_time:
        print(f'\n\n##### {start_time= }')
        end_time = start_time + segment_time
        
        output_image, image_W, image_H = videoEdit.extract_frames_to_MxN_image(
            option='time', 
            start=start_time,
            end=end_time,
            MxN=(M, N),
            video_path=origin_video_path,
            output_dir=None,  # image_array를 반환하고 파일을 생성하지 않음
            gridSize=gridSize,
            padSize=(0, 0)
        )
        
        # 이미지는 image_array 형태로 전달
        response = mllm.query_answer_chatGPT(system_prompt, user_prompt, image_array=output_image)
        if show:
            print(f"response={response}")

        # response 분석하여 필요한 정보 추출
        frame_detected = 0
        q_answers = {}
        
        try:
            # Sequence_Number 추출
            if "Sequence_Number:" in response:
                number_str = response.split("Sequence_Number:")[1].split("\n")[0].strip()
                frame_detected = int(number_str)
            else:
                print("No 'Sequence_Number:'")
                frame_detected = 0
                
            # Q1_Answer, Q2_Answer, Q3_Answer, ... 추출
            q_pattern = re.compile(r'Q(\d+)_Answer:\s*(YES|NO|yes|no|Yes|No)', re.IGNORECASE)
            q_matches = q_pattern.findall(response)
            
            for q_num, answer in q_matches:
                q_answers[f'Q{q_num}'] = answer.upper()
                
        except (ValueError, IndexError) as e:
            if show:
                print(f"응답 파싱 오류: {e}")
            frame_detected = 0
        
        if show:
            print(f'----->')
            print(f"start_time= {start_time}, frame_detected= {frame_detected}-th")
            print(f"Q_Answers= {q_answers}")
                
        if frame_detected != 0 and frame_detected != int(segment_time*2):  # frame_detected가 최초와 치후가 아니면 종료
            break
    
        start_time += offset_time

    if start_time <= play_time - segment_time:
        
        if show:
            # 이미지 표시를 위해 임시로 파일로 저장 (표시용)
            import tempfile
            import cv2
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                cv2.imwrite(tmp_file.name, output_image)
                displaySize = gridSize
                try:
                    display(Image(filename=tmp_file.name, width=displaySize[0], height=displaySize[1]))
                except ImportError:
                    print("IPython.display를 사용할 수 없어서, 이미지 표시를 건너뜁니다.")
                finally:
                    # 임시 파일 삭제
                    os.unlink(tmp_file.name)
    else:
        print("영상 거의 끝까지 탐색했습니다.")
        start_time = play_time  # 마지막 구간 처리
        frame_detected = 0  # 기본값 설정
        q_answers = {}  # 기본값 설정
        
    return start_time, frame_detected, q_answers


videoEdit = ME.MediaEdit()

video_path_selected = r"/home/ymatics/CodingSpace/2025_Care_Nurse/video_source/SMI/07_SMI_full.mov"

origin_video_path = video_path_selected
print(f"{origin_video_path=}")

# query video info
video_name, play_time, frame_count, video_width, video_height, file_size = videoEdit.query_videoInfo(origin_video_path)
print(f"{video_name=} Time: {play_time} sec, Length: {frame_count} frames, Resolution: {video_width}x{video_height} px, File: {file_size:,} Byte")

start_time, segment_time = 0, 4  # 초 단위로 입력
#offset_time = int(segment_time / 2) + (1 if segment_time % 2 != 0 else 0)  # segment 반절씩 이동하면서 분석
offset_time = segment_time - 1  # 오버랩을 1초씩 두고, segment_time씩 이동하면서 분석

system_prompt = "You are a helpful assistant that analyzes images and videos to determine if the user is performing a specific action."
user_prompt = f"""
[Task 1] - Individual Image Analysis
Analyze each image independently for the given image, without considering the context from other images in the sequence.
{PromptBank.search_reference_time['inhalerIN']['picture']}

* Judgment Criteria (apply all):
- Treat each image as a standalone frame without inferring information from previous or subsequent images
- If the person is holding an object in their hand and the shape is consistent with an inhaler, it may be considered an inhaler
- A part of the inhaler must be distinctly visible in the specific image
- This visibility must continue in the immediately following image

* Output Format:
- Sequence_Number: {{image sequence number if found, otherwise "0"}}
- Sequence_Reason: {{explain the decision brieflyin Korean}}

[Task 2] - Sequential Video Analysis
Analyze the provided images as consecutive video frames in temporal sequence. 
Evaluate the continuous action across all frames to determine:

Q1. {PromptBank.check_action_step_common['inhaler_in']['action']}

* Judgment Criteria (apply all):
- Consider all frames as parts of a continuous video
- Consider the continuity of motion and object presence across the sequence
- Use temporal context to identify objects that may be partially visible or obscured in individual frames

* Output Format:
Q1_Answer: [YES or NO]
Q1_Reason: {{explain the decision brieflyin Korean}}
"""

#print(f"user_prompt={user_prompt}")
start_time, frame_detected, q_answers = search_reference_time_check_action_step(system_prompt, user_prompt, play_time, start_time, segment_time, offset_time, show=True)
reference_time_inhalerIN = start_time + frame_detected * 0.5
print("reference_time=", reference_time_inhalerIN)
print("q_answers=", q_answers)