import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="911 Emergency Calls Dashboard", layout="wide")

st.title("🚨 911 Emergency Calls Analytics Dashboard")

# Apelare API Backend
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

@st.cache_data
def load_data():
    try:
        cat_res = requests.get(f"{API_BASE_URL}/calls/by-category")
        cat_res.raise_for_status()
        
        trend_res = requests.get(f"{API_BASE_URL}/calls/monthly-trends")
        trend_res.raise_for_status()
        
        metrics_res = requests.get(f"{API_BASE_URL}/metrics/summary")
        metrics_res.raise_for_status()

        return pd.DataFrame(cat_res.json()), pd.DataFrame(trend_res.json()), metrics_res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Eroare la conectarea cu API-ul backend: {e}")
        st.stop()

df_cat, df_trend, metrics = load_data()

# Metrici KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Apeluri Urgență", f"{metrics['total_calls']:,}")
col2.metric("Total Orașe (Townships)", metrics['total_townships'])
col3.metric("Coduri Poștale", metrics['total_zipcodes'])

st.markdown("---")

# Grafice Interactive (Plotly)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribuția Apelurilor pe Categorii")
    fig_pie = px.pie(
        df_cat, 
        values='count', 
        names='category', 
        color='category',
        color_discrete_map={'EMS': '#EF553B', 'Traffic': '#636EFA', 'Fire': '#00CC96'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Evoluția Lunară a Apelurilor")
    fig_line = px.line(df_trend, x='month', y='count', color='category', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# Secțiune de descărcare date
st.subheader("📥 Descărcare Date Automatizată prin API")
selected_cat = st.selectbox("Filtrează după categorie:", ["Toate", "EMS", "Traffic", "Fire"])

if st.button("Generare și Descărcare CSV"):
    url = (
        f"{API_BASE_URL}/calls/download" 
        if selected_cat == "Toate" 
        else f"{API_BASE_URL}/calls/download?category={selected_cat}"
    )
    res = requests.get(url)
    if res.status_code == 200:
        df_download = pd.DataFrame(res.json())
        csv = df_download.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descarcă fișierul CSV", 
            data=csv, 
            file_name="filtered_911_calls.csv", 
            mime="text/csv"
        )
    else:
        st.error(f"Eroare la preluarea datelor pentru descărcare: Status {res.status_code}")