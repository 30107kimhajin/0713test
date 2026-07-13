import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상 분석", layout="wide")

st.title("🌡️ 서울과 양평의 도시 열섬현상 분석")

# -------------------------------
# 데이터 불러오기
# -------------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")

# 날짜형으로 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])

# 열 이름 변경
seoul = seoul.rename(columns={"기온(°C)": "서울"})
yangpyeong = yangpyeong.rename(columns={"기온(°C)": "양평"})

# 필요한 열만 선택
seoul = seoul[["일시", "서울"]]
yangpyeong = yangpyeong[["일시", "양평"]]

# 데이터 합치기
df = pd.merge(seoul, yangpyeong, on="일시")

# 기온차 계산
df["기온차"] = df["서울"] - df["양평"]

# 시간, 월 추출
df["시"] = df["일시"].dt.hour
df["월"] = df["일시"].dt.month

# -------------------------------
# ① 1년간 기온 변화
# -------------------------------
st.header("① 1년간 서울과 양평의 기온 변화")

line_df = df.set_index("일시")[["서울", "양평"]]
st.line_chart(line_df)

# -------------------------------
# ② 시간별 평균 기온차
# -------------------------------
st.header("② 시각(0~23시)별 평균 기온차 (서울 - 양평)")

hour_df = df.groupby("시")["기온차"].mean()

st.bar_chart(hour_df)

# -------------------------------
# ③ 월별 평균 기온차
# -------------------------------
st.header("③ 월(1~12월)별 평균 기온차 (서울 - 양평)")

month_df = df.groupby("월")["기온차"].mean()

st.bar_chart(month_df)

# -------------------------------
# 데이터 보기
# -------------------------------
with st.expander("데이터 확인"):
    st.dataframe(df)

st.markdown("""
### 🔍 결과 해석
- **기온차 = 서울 기온 - 양평 기온**
- 기온차가 **양수(+)**이면 서울이 더 따뜻합니다.
- 서울이 양평보다 지속적으로 높은 기온을 보인다면 **도시 열섬현상**이 나타난 것으로 볼 수 있습니다.
- 특히 **야간**이나 **겨울철**에 기온차가 크게 나타나는지 확인해 보세요.
""")
