import csv
from io import StringIO

import pandas as pd
import streamlit as st

st.set_page_config(page_title="학생 성적 데이터 탐색", page_icon="📚", layout="wide")
def save_upload():
    uploaded = st.session_state.get("students_csv_upload")
    if uploaded is None:
        st.session_state.pop("students_csv_bytes", None)
        st.session_state.pop("students_data", None)
    else:
        st.session_state["students_csv_bytes"] = uploaded.getvalue()


def render_home():
    st.markdown("""
    # 학생 성적 데이터 탐색

    이 웹은 사용자가 업로드한 학생 성적 CSV 파일을 표와 그래프로 살펴보는 도구입니다.
    파일을 드래그 앤 드롭하거나 파일 선택 버튼으로 업로드하면 데이터를 바로 확인할 수 있습니다.

    **데이터 분석** 페이지에서는 평균·중앙값·표준편차 등의 기술통계와
    Plotly 그래프를 통해 학생 구성, 과목별 점수 분포, 그룹별 성적 차이를 살펴볼 수 있습니다.
    분석할 배경 변수와 과목을 선택하면 그래프가 바뀝니다.

    다른 파일을 분석하려면 이 화면에서 업로드한 파일을 교체하세요.
    통계와 그래프는 업로드한 파일을 기준으로 계산됩니다.
    """)

    CATEGORIES = {"gender": "성별", "race/ethnicity": "인종/민족", "parental level of education": "부모 학력", "lunch": "급식 유형", "test preparation course": "시험 준비 과정"}
    SCORES = {"math score": "수학", "reading score": "읽기", "writing score": "쓰기"}
    with st.container(border=True):
        st.subheader("📂 데이터 업로드")
        st.write("아래 영역에 CSV 파일을 드래그 앤 드롭하거나 **Browse files(파일 선택)** 버튼을 눌러 업로드하세요.")
        uploaded = st.file_uploader(
            "CSV 파일 업로드",
            type=["csv"],
            key="students_csv_upload",
            on_change=save_upload,
            help="파일을 끌어다 놓거나 파일 선택 버튼을 누르면 데이터가 표시됩니다. 그래프는 데이터 분석 페이지에서 확인하세요.",
        )
    if uploaded is not None:
        st.session_state["students_csv_bytes"] = uploaded.getvalue()
    raw = st.session_state.get("students_csv_bytes")
    if raw is None:
        st.info("CSV 파일을 업로드해 주세요. 쉼표 또는 탭 구분 파일을 지원합니다.")
        st.stop()
    st.session_state.pop("students_data", None)
    try:
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("cp949")
        data = pd.read_csv(StringIO(text), sep=None, engine="python")
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError, csv.Error, ValueError):
        st.error("파일을 읽을 수 없습니다. UTF-8 또는 CP949로 저장한 CSV인지 확인해 주세요.")
        st.stop()
    data.columns = data.columns.str.strip()
    required = [*CATEGORIES, *SCORES]
    missing = [column for column in required if column not in data.columns]
    if missing or data.columns.duplicated().any():
        st.error("필수 열이 없거나 열 이름이 중복되어 있습니다.")
        st.write("필수 열: " + ", ".join(required))
        if missing:
            st.write("누락된 열: " + ", ".join(missing))
        st.stop()
    if data.empty:
        st.warning("데이터 행이 없습니다.")
        st.stop()
    st.session_state["students_data"] = data
    st.success(f"업로드 완료 · 학생 {len(data):,}명 · 변수 {len(data.columns)}개")
    st.subheader("업로드한 데이터")
    st.dataframe(data, use_container_width=True)
    st.page_link(analysis_page, label="데이터 분석에서 그래프 보기", icon="📊")


home_page = st.Page(render_home, title="이용 안내 및 업로드", icon="📂", default=True)
analysis_page = st.Page("pages/1_데이터_분석.py", title="데이터 분석", icon="📊", url_path="analysis")
st.session_state["home_page"] = home_page
selected_page = st.navigation([home_page, analysis_page])
selected_page.run()
