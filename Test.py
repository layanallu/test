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


def render(df):
    st.header("🚀 Mission Summary Overview")

    # ----------- Card Section: Launch Vehicle -----------
    st.subheader("🧩 Launch Vehicles")
    vehicle_counts = df["Launch Vehicle"].value_counts().reset_index()
    vehicle_counts.columns = ["Launch Vehicle", "Count"]
    v_cols = st.columns(min(4, len(vehicle_counts)))
    for idx, row in vehicle_counts.iterrows():
        with v_cols[idx % 4]:
            st.markdown(
                f"""
                <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; text-align:center;">
                    <h5 style="margin:0;">{row['Launch Vehicle']}</h5>
                    <p style="font-size:20px; font-weight:bold; color:#4a4a4a;">{row['Count']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ----------- Card Section: Mission Type -----------
    st.subheader("🎯 Mission Types")
    type_counts = df["Mission Type"].value_counts().reset_index()
    type_counts.columns = ["Mission Type", "Count"]
    t_cols = st.columns(min(4, len(type_counts)))
    for idx, row in type_counts.iterrows():
        with t_cols[idx % 4]:
            st.markdown(
                f"""
                <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; text-align:center;">
                    <h5 style="margin:0;">{row['Mission Type']}</h5>
                    <p style="font-size:20px; font-weight:bold; color:#4a4a4a;">{row['Count']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

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
            <div style="background-color:#f9f9f9; padding:25px; border-radius:10px; text-align:center;">
                <h5 style="margin-bottom:10px;">💰 Total Mission Cost</h5>
                <p style="font-size:24px; font-weight:bold; color:#333;">{formatted_cost}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


render(df)

