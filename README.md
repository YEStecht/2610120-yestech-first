# 학생 성적 데이터 탐색

Streamlit 멀티페이지 앱입니다. 메인 `streamlit_app.py`에서 웹 기능 안내를 읽고 CSV를 드래그 앤 드롭하거나 파일 선택 버튼으로 업로드합니다. 업로드 직후 데이터 표가 표시되며, **데이터 분석에서 그래프 보기**를 누르면 별도 페이지에서 기술통계와 그래프를 확인할 수 있습니다. 업로드 데이터는 세션에 보관되어 페이지 간 공유됩니다. API 키는 필요하지 않습니다.

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

UTF-8(BOM 포함), CP949와 쉼표/탭 구분 파일을 지원합니다.

필수 열: `gender`, `race/ethnicity`, `parental level of education`, `lunch`, `test preparation course`, `math score`, `reading score`, `writing score`.

기술통계 표, 학생 수 막대그래프, 과목별 히스토그램, 그룹별 상자 그림을 Plotly로 제공합니다. 잘못된 점수 및 결측 점수는 해당 과목 분석에서 제외합니다.
