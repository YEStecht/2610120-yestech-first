import pandas as pd
import plotly.express as px
import streamlit as st

st.title("학생 성적 기술통계")
st.write("메인 화면에서 업로드한 데이터의 학생 구성과 성적 분포를 확인하세요.")
CATEGORIES = {"gender": "성별", "race/ethnicity": "인종/민족", "parental level of education": "부모 학력", "lunch": "급식 유형", "test preparation course": "시험 준비 과정"}
SCORES = {"math score": "수학", "reading score": "읽기", "writing score": "쓰기"}
stored_data = st.session_state.get("students_data")
if stored_data is None:
    st.info("메인 화면에서 CSV 파일을 먼저 업로드해 주세요.")
    st.page_link(st.session_state["home_page"], label="메인 화면에서 CSV 업로드", icon="📂")
    st.stop()
data = stored_data.copy()
st.page_link(st.session_state["home_page"], label="업로드한 데이터 변경", icon="📂")

invalid = 0
for column in SCORES:
    numeric = pd.to_numeric(data[column], errors="coerce")
    valid = numeric.between(0, 100)
    invalid += int((data[column].notna() & ~valid).sum())
    data[column] = numeric.where(valid)
for column in CATEGORIES:
    data[column] = data[column].astype("string").str.strip().replace("", pd.NA).fillna("미입력")
if invalid:
    st.warning(f"숫자가 아니거나 0~100 범위를 벗어난 점수 {invalid:,}개는 결측값으로 처리했습니다.")
st.caption("점수 결측값은 해당 과목 분석에서 제외됩니다. 범주 결측값은 ‘미입력’으로 표시합니다.")
metrics = st.columns(4)
metrics[0].metric("학생 수", f"{len(data):,}명")
for container, (column, label) in zip(metrics[1:], SCORES.items()):
    mean = data[column].mean()
    container.metric(f"{label} 평균", "자료 없음" if pd.isna(mean) else f"{mean:.1f}점")
st.subheader("과목별 기술통계")
summary = data[list(SCORES)].describe().T.rename(index=SCORES, columns={"count": "유효 학생 수", "mean": "평균", "std": "표준편차", "min": "최솟값", "25%": "1사분위수", "50%": "중앙값", "75%": "3사분위수", "max": "최댓값"})
st.dataframe(summary.round(2), use_container_width=True)
left, right = st.columns(2)
with left:
    st.subheader("범주별 학생 수")
    category = st.selectbox("배경 변수", list(CATEGORIES), format_func=CATEGORIES.get)
    counts = data[category].value_counts().rename_axis("구분").reset_index(name="학생 수")
    st.plotly_chart(px.bar(counts, x="구분", y="학생 수", text_auto=True, title=f"{CATEGORIES[category]}별 학생 수"), use_container_width=True)
with right:
    st.subheader("점수 분포")
    score = st.selectbox("과목", list(SCORES), format_func=SCORES.get)
    st.plotly_chart(px.histogram(data.dropna(subset=[score]), x=score, nbins=20, labels={score: f"{SCORES[score]} 점수"}, title=f"{SCORES[score]} 점수 분포"), use_container_width=True)
st.subheader("그룹별 성적 비교")
st.plotly_chart(px.box(data.dropna(subset=[score]), x=category, y=score, color=category, labels={category: CATEGORIES[category], score: f"{SCORES[score]} 점수"}, title=f"{CATEGORIES[category]}별 {SCORES[score]} 점수", points="outliers"), use_container_width=True)
st.caption("상자 그림은 중앙값과 사분위 범위를 보여 줍니다. 그룹 간 차이는 인과관계를 의미하지 않습니다.")
