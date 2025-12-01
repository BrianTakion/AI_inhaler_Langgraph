# ReporterAgent 평가 로직 개선 요구사항 분석 및 수정 방향

## 1. 개요
본 문서는 `app_DPI_type3/agents/reporter_agent.py` 내 `ReporterAgent`의 결과 리포팅 로직을 개선하기 위한 요구사항을 분석하고 기술적인 수정 방향을 정의합니다. 
기존의 단순 평균값 시각화 방식에서 벗어나, **Reference Time(기준 시점)**을 바탕으로 각 행동(Action)의 성공 여부를 **최종 판단(Decision)**하는 로직을 추가하고 이를 시각화에 반영하는 것을 목표로 합니다.

---

## 2. 현행 로직 분석 (AS-IS)

현재 `ReporterAgent`는 다음 순서로 동작합니다.

1.  **Reference Time 평균 산출**: 여러 모델이 예측한 `search_reference_time`의 평균을 계산.
2.  **Action Step 평균 산출**: 여러 모델이 예측한 `check_action_step_DPI_type3`의 점수(Score) 및 신뢰도(Confidence) 평균을 계산.
3.  **단순 시각화**: 계산된 평균 데이터를 Plotly 타임라인 차트로 단순 나열 및 저장.
    *   별도의 성공/실패 판정 로직(Decision)이 존재하지 않음.
    *   점수가 0.5 이상이면 시각화 상에서 점으로 표시되는 수준임.

---

## 3. 변경 요구사항 상세 (TO-BE)

### 3.1. 데이터 처리 (기존 유지)
*   (1), (2) 항목은 기존과 동일하게 유지합니다.
    *   `search_reference_time` 평균값 계산.
    *   `check_action_step_DPI_type3` 평균값 계산.

### 3.2. 최종 판단 로직 추가 (신규)
평균치로 산출된 데이터를 기반으로, **특정 시간 구간(Reference Time 기준)** 내에서 Action의 발생 여부를 체크하여 `TRUE(1)` 또는 `FALSE(0)`를 확정합니다.

**기본 규칙:**
*   모든 `action_step_decision`의 초기값은 **FALSE**로 설정합니다.
*   각 Action 별로 아래의 조건을 만족할 경우 **TRUE**로 변경합니다.

#### 기준 시간 변수 정의
*   `T_in`: **inhalerIN** (흡입기가 화면에 들어온 시점)
*   `T_face`: **faceONinhaler** (흡입기를 입에 문 시점)
*   `T_out`: **inhalerOUT** (흡입기가 화면에서 나간 시점)

#### Action 별 판단 조건표

| Action Key | 판단 구간 / 시점 | 판단 조건 (Logic) |
| :--- | :--- | :--- |
| **sit_stand** | `T_face` 시점 및 그 직전 시점 | 두 시점 모두 `TRUE`여야 함 (AND 조건) |
| **remove_cover** | `T_face` 시점 및 그 직전 시점 | 하나라도 `TRUE`이면 성공 (OR 조건) |
| **inspect_mouthpiece** | `T_face` 시점 및 그 직전 시점 | 하나라도 `TRUE`이면 성공 (OR 조건) |
| **hold_inhaler** | `T_face` 시점 및 그 직전 시점 | 하나라도 `TRUE`이면 성공 (OR 조건) |
| **load_dose** | `T_in` ~ `T_face` 사이 | 구간 내 하나라도 `TRUE`이면 성공 |
| **exhale_before** | `T_face` 시점 및 그 직전 시점 | 하나라도 `TRUE`이면 성공 (OR 조건) |
| **seal_lips** | `T_face` 시점 및 그 직후 시점 | 하나라도 `TRUE`이면 성공 (OR 조건) |
| **inhale_deeply** | `T_face` 시점 및 그 직후 시점 | (`seal_lips` **AND** `inhale_deeply`)가 하나라도 `TRUE`이면 성공 |
| **remove_inhaler** | `T_face` ~ `T_out` 사이 | 구간 내 하나라도 `TRUE`이면 성공 |
| **hold_breath** | `T_face` ~ `T_out` 사이 | 구간 내 **2초 이상 연속**으로 `TRUE` 유지 시 성공 |
| **exhale_after** | `T_face` ~ `T_out` 사이 | 구간 내 하나라도 `TRUE`이면 성공 |
| **clean_inhaler** | `T_face` ~ `T_out` 사이 | 구간 내 하나라도 `TRUE`이면 성공 |

### 3.3. 시각화 업데이트
*   산출된 Decision 결과(1 또는 0)를 Y축 라벨에 포함하여 표시합니다.
*   **형식 예시:** `sit_stand(1)`, `remove_cover(0)`

---

## 4. 수정 방향 (Technical Implementation Plan)

### 4.1. `_evaluate_decisions` 메서드 신규 구현
`_compute_average` 이후, 시각화 생성 전에 실행될 별도의 판단 메서드를 구현합니다.

**입력:**
*   `reference_times_avg`: 평균 기준 시간 데이터
*   `promptbank_data_avg`: 평균 Action 데이터 (시간별 Score 포함)

**처리 프로세스:**
1.  **기준 시간 추출:** `inhalerIN`, `faceONinhaler`, `inhalerOUT` 값을 추출합니다. (값이 없을 경우 예외 처리 또는 전체 구간 간주)
2.  **데이터 구조화:** 각 Action 별로 `(time, score)` 리스트를 확보합니다. (Score >= 0.5를 TRUE로 간주)
3.  **조건 루프 실행:** 위 3.2의 조건표에 따라 각 Action을 순회하며 True/False를 판별합니다.
    *   *Time Window Filtering:* 각 조건에 맞는 시간 범위의 데이터만 필터링합니다.
    *   *Logic Check:* `any()`, `all()`, 또는 시간 차이 계산(`hold_breath`용)을 수행합니다.

**출력:**
*   `decisions`: `{ "sit_stand": 1, "remove_cover": 0, ... }` 형태의 딕셔너리.

### 4.2. `_create_final_report` 수정
*   `_evaluate_decisions`를 호출하여 판단 결과를 얻습니다.
*   결과 리포트 딕셔너리에 `action_decisions` 키를 추가하여 저장합니다.

### 4.3. `_create_visualization` 수정
*   Y축 라벨 생성 로직을 변경합니다.
*   기존: `action_key` (예: "sit_stand")
*   변경: `f"{action_key}({decision_value})"` (예: "sit_stand(1)")
*   `decision_value`는 4.2에서 생성한 결과에서 조회합니다.

### 4.4. 고려사항 및 예외처리
*   **기준 시간 누락:** `faceONinhaler` 등의 기준 시간이 감지되지 않았을 경우, 해당 구간에 의존하는 판단 로직은 모두 `FALSE` 처리하거나, 안전하게 전체 구간에서 탐색하도록 예외 처리가 필요합니다. (기본적으로는 FALSE 처리가 안전함)
*   **연속 시간 계산:** `hold_breath`의 1초 판단을 위해 타임스탬프 간의 차이(`delta`)를 누적하거나, 연속된 프레임의 시간 차를 계산하는 로직이 필요합니다.

---

## 5. 예상되는 파일 변경
*   **Target File:** `app_DPI_type3/agents/reporter_agent.py`
*   **Modified Methods:**
    *   `_create_final_report`: 결정 로직 호출 및 결과 저장 추가.
    *   `_create_visualization`: Y축 라벨 포맷팅 변경.
*   **New Method:**
    *   `_evaluate_decisions(self, reference_times, action_data)`: 핵심 판단 로직 구현.

