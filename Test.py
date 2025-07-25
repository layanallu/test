# tabs/mission_summary.py
# WorldExpenditures.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from babel.numbers import format_decimal



# Load Data
df = pd.read_csv("space_missions_dataset.csv")

# 1. Basic Dataset Overview



# tabs/mission_summary.py



def fancy_card(title: str, value: str, color: str = "#f9f9f9"):
    st.markdown(f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 16px; 
                    text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
            <h5 style="margin: 0; color: #444;">{title}</h5>
            <h2 style="margin: 0; color: #111;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# دالة العرض
def render(df: pd.DataFrame):
    st.header("🛰️ Mission Summary Overview")

    # الكروت الخاصة بـ Launch Vehicle
    st.subheader("🚀 Launch Vehicles Overview")
    launch_counts = df["Launch Vehicle"].value_counts().reset_index()
    launch_counts.columns = ["Launch Vehicle", "Count"]
    cols = st.columns(min(4, len(launch_counts)))
    for idx, row in launch_counts.iterrows():
        with cols[idx % 4]:
            fancy_card(row["Launch Vehicle"], f"{row['Count']} Missions")

    # الكروت الخاصة بـ Mission Type
    st.subheader("🎯 Mission Types Overview")
    mission_counts = df["Mission Type"].value_counts().reset_index()
    mission_counts.columns = ["Mission Type", "Count"]
    cols2 = st.columns(min(4, len(mission_counts)))
    for idx, row in mission_counts.iterrows():
        with cols2[idx % 4]:
            fancy_card(row["Mission Type"], f"{row['Count']} Missions")

    st.markdown("---")

    # ----------- Donut Charts -----------
    st.subheader("📊 Mission Success & Failure Rates")
    success_rate = df["Mission Success (%)"].mean()
    failure_rate = 100 - success_rate

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        fig_success = go.Figure(go.Indicator(
            mode="gauge+number",
            value=success_rate,
            number={"suffix": "%", "font": {"size": 36, "color": "green"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray"
            },
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "✅ Success Rate", "font": {"size": 18}}
        ))
        fig_success.update_layout(height=250, margin=dict(t=30, b=0))
        st.plotly_chart(fig_success, use_container_width=True)

    with col2:
        fig_failure = go.Figure(go.Indicator(
            mode="gauge+number",
            value=failure_rate,
            number={"suffix": "%", "font": {"size": 36, "color": "red"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "red"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray"
            },
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "❌ Failure Rate", "font": {"size": 18}}
        ))
        fig_failure.update_layout(height=250, margin=dict(t=30, b=0))
        st.plotly_chart(fig_failure, use_container_width=True)

    # ----------- Total Cost Card -----------
    total_cost = df["Mission Cost (billion USD)"].sum()
    formatted_cost = f"${format_decimal(total_cost, format='#,##0.00')} Billion"

    with col3:
        st.markdown(
            f"""
            <div style="background-color:#cbe58e; padding:25px; border-radius:10px; text-align:center;">
                <h5 style="margin-bottom:10px;">💰 Total Mission Cost</h5>
                <p style="font-size:24px; font-weight:bold; color:#333;">{formatted_cost}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


render(df)

