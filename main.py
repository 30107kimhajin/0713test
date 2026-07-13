import streamlit as st
import pandas as pd

# --------------------------------
# 기본 설정
# --------------------------------
st.set_page_config(page_title="도시 열섬현상과 전력수요 분석", layout="wide")

st.title("🌡️ 도시 열섬현상과 전력수요 분석")

# --------------------------------
# 데이터 불러오기
# --------------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yang = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜 형식 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yang["일시"] = pd.to_datetime(yang["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 열 이름 변경
seoul = seoul.rename(columns={"기온(°C)": "서울기온"})
yang = yang.rename(columns={"기온(°C)": "양평기온"})

# 필요한 열만 선택
seoul = seoul[["일시", "서울기온"]]
yang = yang[["일시", "양평기온"]]
power = power[["일시", "전력수요(MWh)"]]

# --------------------------------
# 탭 생성
# --------------------------------
tab1, tab2 = st.tabs(["🌡️ 열섬 분석", "⚡ 전력 연결"])

# ============================================================
# 탭1 : 열섬 분석
# ============================================================
with tab1:

    st.header("서울과 양평의 도시 열섬현상")

    # 데이터 합치기
    temp = pd.merge(seoul, yang, on="일시")

    temp["기온차"] = temp["서울기온"] - temp["양평기온"]
    temp["시"] = temp["일시"].dt.hour
    temp["월"] = temp["일시"].dt.month

    # ① 연간 기온 변화
    st.subheader("① 1년간 두 지역 기온 변화")

    line = temp.set_index("일시")[["서울기온", "양평기온"]]
    st.line_chart(line)

    # ② 시간별 평균 기온차
    st.subheader("② 시각(0~23시)별 평균 기온차 (서울-양평)")

    hour = temp.groupby("시")["기온차"].mean()
    st.bar_chart(hour)

    # ③ 월별 평균 기온차
    st.subheader("③ 월별 평균 기온차 (서울-양평)")

    month = temp.groupby("월")["기온차"].mean()
    st.bar_chart(month)

# ============================================================
# 탭2 : 전력 연결
# ============================================================
with tab2:

    st.header("서울 기온과 전력수요의 관계")

    # 데이터 합치기
    energy = pd.merge(seoul, power, on="일시")

    energy["월"] = energy["일시"].dt.month

    # 기온 구간 만들기 (5도 단위)
    bins = [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
    labels = [
        "-20~-15", "-15~-10", "-10~-5", "-5~0",
        "0~5", "5~10", "10~15", "15~20",
        "20~25", "25~30", "30~35", "35~40"
    ]

    energy["기온구간"] = pd.cut(
        energy["서울기온"],
        bins=bins,
        labels=labels
    )

    # ① 산점도
    st.subheader("① 기온과 전력수요의 산점도")

    scatter = energy.rename(columns={
        "서울기온": "x",
        "전력수요(MWh)": "y"
    })

    st.scatter_chart(scatter, x="x", y="y")

    # ② 기온구간별 평균 전력수요
    st.subheader("② 기온 구간별 평균 전력수요")

    temp_power = energy.groupby("기온구간")["전력수요(MWh)"].mean()
    st.bar_chart(temp_power)

    # ③ 월별 평균 전력수요
    st.subheader("③ 월별 평균 전력수요")

    month_power = energy.groupby("월")["전력수요(MWh)"].mean()
    st.bar_chart(month_power)

# --------------------------------
# 설명
# --------------------------------
st.markdown("""
---
### 📌 결과 해석

**열섬 분석**
- 서울 기온이 양평보다 높을수록 도시 열섬현상이 강하게 나타난다.
- 특히 야간이나 겨울철에 기온차가 커지는지 확인할 수 있다.

**전력 연결**
- 기온이 매우 높거나 매우 낮을수록 냉난방 사용 증가로 전력수요가 커지는 경향을 확인할 수 있다.
- 월별 평균 전력수요를 통해 계절에 따른 전력 소비 변화도 살펴볼 수 있다.
""")
