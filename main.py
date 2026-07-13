import streamlit as st
import pandas as pd

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="도시 열섬현상과 전력수요", layout="wide")
st.title("🌡️ 도시 열섬현상과 전력수요 분석")

# -------------------------------
# 데이터 읽기
# -------------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yang = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yang["일시"] = pd.to_datetime(yang["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 필요한 열만 선택하고 이름 변경
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울"})
yang = yang[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평"})

# -------------------------------
# 탭 만들기
# -------------------------------
tab1, tab2 = st.tabs(["🌡️ 열섬 분석", "⚡ 전력 연결"])

# ======================================================
# 탭1
# ======================================================
with tab1:

    st.header("서울과 양평의 기온 비교")

    df = pd.merge(seoul, yang, on="일시")

    df["기온차"] = df["서울"] - df["양평"]
    df["시"] = df["일시"].dt.hour
    df["월"] = df["일시"].dt.month

    st.subheader("① 1년간 기온 변화")

    line = df.set_index("일시")[["서울", "양평"]]
    st.line_chart(line)

    st.subheader("② 시각별 평균 기온차")

    hour = df.groupby("시", as_index=True)["기온차"].mean()
    st.bar_chart(hour)

    st.subheader("③ 월별 평균 기온차")

    month = df.groupby("월", as_index=True)["기온차"].mean()
    st.bar_chart(month)

# ======================================================
# 탭2
# ======================================================
with tab2:

    st.header("서울 기온과 전력수요")

    energy = pd.merge(seoul, power, on="일시")

    energy["월"] = energy["일시"].dt.month

    # 기온 구간
    bins = [-20,-15,-10,-5,0,5,10,15,20,25,30,35,40]

    energy["기온구간"] = pd.cut(
        energy["서울"],
        bins=bins
    )

    st.subheader("① 기온과 전력수요 산점도")

    st.scatter_chart(
        energy,
        x="서울",
        y="전력수요(MWh)"
    )

    st.subheader("② 기온 구간별 평균 전력수요")

    temp = energy.groupby("기온구간", observed=False)["전력수요(MWh)"].mean()
    st.bar_chart(temp)

    st.subheader("③ 월별 평균 전력수요")

    month_power = energy.groupby("월")["전력수요(MWh)"].mean()
    st.bar_chart(month_power)

st.divider()

st.write("### 결과 해석")
st.write("- 서울 기온이 양평보다 높을수록 도시 열섬현상이 강하게 나타납니다.")
st.write("- 기온이 높거나 낮을수록 냉·난방 사용으로 전력수요가 증가하는 경향을 확인할 수 있습니다.")
