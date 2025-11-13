class PromptBank:
    def __init__(self):
        """
        PromptBank 클래스 초기화
        reference_time은 0, timeANDscore는 빈 리스트로 초기화
        """
        self.search_reference_time = {
            'inhalerIN': {
                'action': 'Is the inhaler visible at any point throughout the images?',
                'reference_time': 0
            },
            'faceONinhaler': {
                'action': 'Is the person holding an object to the mouth as if using an inhaler?',
                'reference_time': 0
            },
            'inhalerOUT': {
                'action': 'Is the inhaler invisible at any point throughout the images?',
                'reference_time': 0
            }
        }

        self.check_action_step_common = {
            'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'load_dose': {
                'action': 'Is the user loading the medication? (Consider the user loading the medication if they are manipulating, twisting, or opening the inhaler.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_cover': {
                'action': 'Has the user removed the mouthpiece cover? (Consider the user removing the cover if the mouthpiece is visible when the inhaler is positioned near the mouth.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'shake_inhaler': {
                'action': 'Is the user shaking the inhaler? (Consider the inhaler shaken whenever the hand holding the inhaler shows movement across successive frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_capsule': {
                'action': 'Is the user removing the capsule? (Consider the user removing the capsule if they are manipulating and focusing on the inhaler as if trying to remove it.)', 
                'timeANDscore': [],
                'confidence_score': []
            }
        }

        self.check_action_step_category1 = {
            'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_cover': {
                'action': 'Has the user removed the mouthpiece cover? (Consider the user removing the cover if the mouthpiece is visible when the inhaler is positioned near the mouth.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'shake_inhaler': {
                'action': 'Is the user shaking the inhaler? (Consider the inhaler shaken whenever the hand holding the inhaler shows movement across successive frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },          
        }

        self.check_action_step_category2 = {
            'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_cover': {
                'action': 'Has the user removed the mouthpiece cover? (Consider the user removing the cover if the mouthpiece is visible when the inhaler is positioned near the mouth.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
        }

        self.check_action_step_category3 = {
            'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'load_dose': {
                'action': 'Is the user loading the medication? (Consider the user loading the medication if they are manipulating, twisting, or opening the inhaler.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
        }
        
        self.check_action_step_category4 = {
             'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'load_dose': {
                'action': 'Is the user loading the medication? (Consider the user loading the medication if they are manipulating, twisting, or opening the inhaler.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_cover': {
                'action': 'Has the user removed the mouthpiece cover? (Consider the user removing the cover if the mouthpiece is visible when the inhaler is positioned near the mouth.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
        }
        
        self.check_action_step_category5 = {
            'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'load_dose': {
                'action': 'Is the user loading the medication? (Consider the user loading the medication if they are manipulating, twisting, or opening the inhaler.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_cover': {
                'action': 'Has the user removed the mouthpiece cover? (Consider the user removing the cover if the mouthpiece is visible when the inhaler is positioned near the mouth.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_capsule': {
                'action': 'Is the user removing the capsule? (Consider the user removing the capsule if they are manipulating and focusing on the inhaler as if trying to remove it.)', 
                'timeANDscore': [],
                'confidence_score': []
            }
        }

        self.check_action_step_category6 = {
            'sit_stand': {
                'action': 'Is the user sitting or standing upright? (Consider the user upright even if they are sitting with a slight forward lean.)',
                'timeANDscore': [],
                'confidence_score': []
            },
            'load_dose': {
                'action': 'Is the user loading the medication? (Consider the user loading the medication if they are manipulating, twisting, or opening the inhaler.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_cover': {
                'action': 'Has the user removed the mouthpiece cover? (Consider the user removing the cover if the mouthpiece is visible when the inhaler is positioned near the mouth.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inspect_mouthpiece': {
                'action': 'Is the user inspecting the mouthpiece? (Consider the user inspecting if they are gazing toward the mouthpiece.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_inhaler': {
                'action': 'Is the user holding the inhaler upright?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_before': {
                'action': 'Is the user exhaling away from the inhaler? (Consider exhaling if the mouth moves, the head lowers, or the eyes gaze downward.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'seal_lips': {
                'action': 'Is the user placing their mouth on the mouthpiece of the inhaler?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'inhale_deeply': {
                'action': 'Is the user inhaling from the inhaler? (Consider the user inhaling if the inhaler is in their mouth and they appear to be sucking on it.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'remove_inhaler': {
                'action': 'Is the user removing the inhaler from their mouth?', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'hold_breath': {
                'action': 'Is the user holding their breath? (Consider the user holding their breath if their mouth stays closed for a while.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
            'exhale_after': {
                'action': 'Is the user exhaling away from the inhaler? (Consider the user exhaling if lips are tighter than in the previous frames.)', 
                'timeANDscore': [],
                'confidence_score': []
            },
        }

    def save_to_promptbank(self, reference_key, reference_time, q_answers_accumulated, q_mapping):
        """
        누적된 Q&A 결과를 PromptBank에 저장하는 메서드
        
        Args:
            reference_key (str): search_reference_time의 키 (예: 'inhalerIN', 'faceONinhaler')
            reference_time (float): 기준 시간
            q_answers_accumulated (dict): 누적된 Q&A 결과 (time, answer, confidence)
            q_mapping (dict): Q번호와 액션 키의 매핑 (예: {'Q1': 'sit_stand'})
        """
        # 1. 기준 시간 저장
        self.search_reference_time[reference_key]['reference_time'] = reference_time
        
        # 2. Q&A 결과를 scoreANDtime 형태로 저장
        for q_key, action_key in q_mapping.items():
            if q_key in q_answers_accumulated:
                for answer_data in q_answers_accumulated[q_key]:
                    # answer_data는 (time, answer, confidence) 튜플
                    if len(answer_data) == 3:
                        time_val, answer_str, confidence = answer_data
                    else:
                        # 하위 호환성: confidence가 없는 경우
                        time_val, answer_str = answer_data
                        confidence = None
                    
                    # 시간값을 float로 변환하여 저장
                    time_val = float(time_val)
                    score = 1 if answer_str == 'YES' else 0
                    self.check_action_step_common[action_key]['timeANDscore'].append((time_val, score))
                    
                    # confidence score 저장
                    if confidence is not None:
                        self.check_action_step_common[action_key]['confidence_score'].append((time_val, confidence))