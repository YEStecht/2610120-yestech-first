import pandas as pd
import streamlit as st

st.set_page_config(page_title="학생 성적 데이터 탐색", page_icon="📊")

st.title("학생 성적 데이터 탐색")
st.write("StudentsPerformance.csv 파일을 업로드하면 학생 배경 정보를 그래프로 확인할 수 있습니다.")

uploaded_file = st.file_uploader("CSV 파일 선택 또는 여기로 끌어다 놓기", type="csv")

if uploaded_file is not None:
    try:
        students = pd.read_csv(uploaded_file)
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError):
        st.error("CSV 파일을 읽을 수 없습니다. 올바른 CSV 파일인지 확인해 주세요.")
        st.stop()

    students.columns = students.columns.str.strip()
    chart_columns = {
        "race/ethnicity": "인종/민족별 학생 수",
        "parental level of education": "부모 학력별 학생 수",
    }
    missing_columns = [column for column in chart_columns if column not in students.columns]

    if missing_columns:
        missing_names = ", ".join(missing_columns)
        st.error(f"필수 열을 찾을 수 없습니다: {missing_names}")
        st.caption("CSV에 'race/ethnicity'와 'parental level of education' 열이 있는지 확인해 주세요.")
        st.stop()

    st.subheader("인종/민족별 학생 수")
    race_counts = (
        students["race/ethnicity"]
        .fillna("미입력")
        .replace("", "미입력")
        .value_counts()
        .rename_axis("인종/민족")
        .reset_index(name="학생 수")
    )
    st.bar_chart(race_counts, x="인종/민족", y="학생 수")

    st.subheader("부모 학력별 학생 수")
    education_counts = (
        students["parental level of education"]
        .fillna("미입력")
        .replace("", "미입력")
        .value_counts()
        .rename_axis("부모 학력")
        .reset_index(name="학생 수")
    )
    st.bar_chart(education_counts, x="부모 학력", y="학생 수")

    with st.expander("업로드한 데이터 미리보기"):
        st.dataframe(students, use_container_width=True)
else:
    st.info("분석을 시작하려면 StudentsPerormance.csv 파일을 업로드해 주세요.")
