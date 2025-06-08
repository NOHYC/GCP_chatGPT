import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("📈 미국 & 한국 증시 지수 추이 (최근 1년)")

# 1년 전 날짜
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 미국 증시
us_indices = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI"
}

# 한국 증시
kr_indices = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11"
}

# 통합 딕셔너리
all_indices = {"미국 증시": us_indices, "한국 증시": kr_indices}

# 데이터 수집
def fetch_index_data(symbols: dict):
    data = {}
    for name, code in symbols.items():
        df = yf.download(code, start=start_date, end=end_date)
        if not df.empty:
            df = df[["Close"]].rename(columns={"Close": name})
            data[name] = df
        else:
            st.warning(f"{name} 데이터 없음")
    return pd.concat(data.values(), axis=1)

with st.spinner("📡 미국 증시 데이터를 불러오는 중..."):
    us_df = fetch_index_data(us_indices)

with st.spinner("📡 한국 증시 데이터를 불러오는 중..."):
    kr_df = fetch_index_data(kr_indices)

# 병합
full_df = pd.concat([us_df, kr_df], axis=1)
full_df.index.name = "날짜"

# 선택 UI
all_names = list(us_indices.keys()) + list(kr_indices.keys())
selected = st.multiselect("표시할 지수 선택", all_names, default=all_names)

if selected:
    st.subheader("📊 1년간 지수 종가 추이")
    st.line_chart(full_df[selected])
else:
    st.info("표시할 지수를 선택하세요.")

st.subheader("📋 최근 30일 지수 데이터")
st.dataframe(full_df[selected].tail(30), use_container_width=True)

# 다운로드
csv = full_df.to_csv().encode("utf-8")
st.download_button(
    "⬇️ 전체 데이터 다운로드 (CSV)",
    csv,
    "stock_indices_1year.csv",
    "text/csv"
)
