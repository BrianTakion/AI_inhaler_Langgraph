from pathlib import Path  # 표준 라이브러리
import base64             # 표준 라이브러리

import numpy as np
import pandas as pd
import cv2
import matplotlib
import plotly
import openai

def main():
    # 최소 동작 확인 메시지
    print("✅ DevContainer Python 환경 동작 확인")
    print(f"- Python pkg: numpy {np.__version__}, pandas {pd.__version__}, opencv {cv2.__version__}")
    print(f"- matplotlib {matplotlib.__version__}, plotly {plotly.__version__}")
    print(f"- openai {openai.__version__ if hasattr(openai, '__version__') else 'installed'}")

    # 경로·인코딩 간단 점검
    tmp = Path("/workspace/.check")
    tmp.write_text("hello devcontainer\n", encoding="utf-8")
    encoded = base64.b64encode(b"hello").decode("utf-8")
    print(f"- Path OK: {tmp} created")
    print(f"- base64 test: {encoded}")

if __name__ == "__main__":
    main()
