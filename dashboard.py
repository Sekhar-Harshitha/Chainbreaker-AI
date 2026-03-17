import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="ChainBreaker AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 ChainBreaker AI — Misinformation Dashboard")

# Function to load data
def load_data():
    log_file = Path("data.json")
    if not log_file.exists():
        return pd.DataFrame()
    
    data = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    df = pd.DataFrame(data)
    # Ensure all required columns exist even if data is empty or missing fields
    required_cols = ['timestamp', 'text', 'verdict', 'virality_score', 'cached']
    for col in required_cols:
        if col not in df.columns:
            df[col] = None
    return df

# Sidebar for auto-refresh
st.sidebar.title("Settings")
if st.sidebar.button("Refresh Now"):
    st.rerun()

# Optional: Simple auto-refresh using JavaScript if needed, 
# but for now we rely on the manual refresh button or future st_autorefresh.

# Load data
df = load_data()

if not df.empty:
    # Metrics
    total_messages = len(df)
    false_claims = len(df[df['verdict'] == 'FALSE'])
    
    # Safely calculate mean, handling non-numeric or empty
    try:
        avg_virality = pd.to_numeric(df['virality_score'], errors='coerce').mean()
    except:
        avg_virality = 0
        
    cache_hits = len(df[df['cached'] == True])

    # Display Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Messages", total_messages)
    col2.metric("False Claims", false_claims)
    col3.metric("Avg Virality Score", f"{avg_virality:.1f}/10" if not pd.isna(avg_virality) else "0.0/10")
    col4.metric("Cache Hits", cache_hits)

    st.divider()

    # Visualizations
    st.subheader("🔍 Analysis")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("**Virality Score Distribution**")
        if not df['virality_score'].dropna().empty:
            fig_virality = px.histogram(
                df, x="virality_score", 
                title="Virality Score Distribution",
                nbins=10,
                color_discrete_sequence=['#FF4B4B']
            )
            fig_virality.update_layout(bargap=0.1)
            st.plotly_chart(fig_virality, use_container_width=True)
        else:
            st.info("No virality data to display.")

    with chart_col2:
        st.write("**Verdict Distribution**")
        if not df['verdict'].dropna().empty:
            verdict_counts = df['verdict'].value_counts().reset_index()
            verdict_counts.columns = ['verdict', 'count']
            
            fig_verdict = px.pie(
                verdict_counts,
                names='verdict',
                values='count',
                hole=0.4,
                color='verdict',
                color_discrete_map={
                    'FALSE': '#FF4B4B',
                    'UNCERTAIN': '#FFA500',
                    'TRUE': '#00CC96'
                }
            )
            st.plotly_chart(fig_verdict, use_container_width=True)
        else:
            st.info("No verdict data to display.")

    st.divider()

    # Recent Messages Table
    st.subheader("📋 Recent Messages")
    # Display last 10
    recent_df = df.sort_values(by='timestamp', ascending=False).head(10)
    # Filter to show only available requested columns
    display_cols = [c for c in ['text', 'verdict', 'virality_score', 'cached'] if c in recent_df.columns]
    st.table(recent_df[display_cols])

else:
    st.info("No data available yet. Processing new messages will update this dashboard.")

# Auto-refresh using a simple timer
# NOTE: Streamlit doesn't have a native auto-refresh without custom components, 
# but we can use st_autorefresh or a simple workaround if needed.
# For now, manual refresh or simple rerun if the user stays on page.
# (But streamlit run handles most live updates if the file changes or with rerun)
# streamlit-autorefresh is a third party lib. I'll stick to a simple Rerun button for now.
