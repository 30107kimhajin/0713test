import streamlit as st
import pandas as pd

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="도시 열섬현상과 전력수요", layout="wide")

st.title("🌡️ 도시 열섬현상과 전력수요 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yang = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜형 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yang["일시"] = pd.to_datetime(yang["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 필요한 열만 사용
seoul = seoul[["일시", "기온(°C)"]]
yang = yang[["일시", "기온(°C)"]]

# 이름 변경
seoul.columns = ["일시", "서울"]
yang.columns = ["일시", "양평"]

# -----------------------------
# 탭 만들기
# -----------------------------
tab1, tab2 = st.tabs(["🌡️ 열섬 분석", "⚡ 전력 연결"])

# ====================================================
# 탭1 : 열섬 분석
# ====================================================
with tab1:

    st.header("서울과 양평의 기온 비교")

    temp = pd.merge(seoul, yang, on="일시")

    temp["기온차"] = temp["서울"] - temp["양평"]
    temp["시"] = temp["일시"].dt.hour
    temp["월"] = temp["일시"].dt.month

    st.subheader("① 1년간 두 지역 기온 변화")
    st.line_chart(temp.set_index("일시")[["서울", "양평"]])

    st.subheader("② 시각별 평균 기온차")
    hour = temp.groupby("시")["기온차"].mean()
    st.bar_chart(hour)

    st.subheader("③ 월별 평균 기온차")
    month = temp.groupby("월")["기온차"].mean()
    st.bar_chart(month)

# ====================================================
# 탭2 : 전력 연결
# ====================================================
with tab2:

    st.header("서울 기온과 전력수요")

    energy = pd.merge(seoul, power, on="일시")

    energy["월"] = energy["일시"].dt.month

    st.subheader("① 기온과 전력수요의 산점도")

    scatter = energy.rename(columns={
        "서울": "기온",
        "전력수요(MWh)": "전력수요"
    })

    st.scatter_chart(
        data=scatter,
        x="기온",
        y="전력수요"
    )

    # 기온 구간 생성(5도 간격)
    energy["기온구간"] = (energy["서울"] // 5) * 5

    st.subheader("② 기온 구간별 평균 전력수요")

    temp_power = energy.groupby("기온구간")["전력수요(MWh)"].mean()
    st.bar_chart(temp_power)

    st.subheader("③ 월별 평균 전력수요")

    month_power = energy.groupby("월")["전력수요(MWh)"].mean()
    st.bar_chart(month_power)

st.divider()

st.markdown("""
### 📌 결과 해석
- 서울과 양평의 기온 차이를 통해 도시 열섬현상을 확인할 수 있습니다.
- 서울의 기온과 전력수요를 비교하여 기온 변화가 전력 사용량에 어떤 영향을 주는지 확인할 수 있습니다.
""")
