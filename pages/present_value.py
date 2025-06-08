import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 주요 원자재 가격 추이 (최근 1년)")

# 원자재 목록 (야후 심볼)
commodity_symbols = {
    "금(Gold)": "GC=F",
    "은(Silver)": "SI=F",
    "구리(Copper)": "HG=F",
    "WTI 유가(Crude Oil)": "CL=F",
    "천연가스(Natural Gas)": "NG=F",
    "옥수수(Corn)": "ZC=F",
    "대두(Soybeans)": "ZS=F",
    "밀(Wheat)": "ZW=F",
    "가솔린(Gasoline)": "RB=F",
    "백금(Platinum)": "PL=F",
}

# 날짜 범위 설정: 최근 1년
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 가져오기
with st.spinner("📡 원자재 가격 데이터를 수집 중입니다..."):
    data = {}
    for name, symbol in commodity_symbols.items():
        df = yf.download(symbol, start=start_date, end=end_date)
        if not df.empty:
            df = df[["Close"]].rename(columns={"Close": name})
            data[name] = df
        else:
            st.warning(f"⚠️ {name} 데이터 없음.")

# 모든 데이터 병합
merged = pd.concat(data.values(), axis=1)
merged.index.name = "날짜"

# 시각화
st.subheader("📈 가격 추이 그래프")
selected_commodities = st.multiselect("표시할 원자재 선택", list(commodity_symbols.keys()), default=list(commodity_symbols.keys()))

if selected_commodities:
    st.line_chart(merged[selected_commodities])
else:
    st.info("표시할 원자재를 선택하세요.")

# 표 출력
st.subheader("📋 가격 데이터 테이블")
st.dataframe(merged.tail(30), use_container_width=True)

# 다운로드 버튼
csv = merged.to_csv().encode("utf-8")
st.download_button(
    "⬇️ 전체 데이터 다운로드 (CSV)",
    csv,
    "commodities_1year.csv",
    "text/csv",
    key="download-csv"
)
