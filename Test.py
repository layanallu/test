# tabs/mission_summary.py
# WorldExpenditures.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go



# Load Data
df = pd.read_csv("space_missions_dataset.csv")

# 1. Basic Dataset Overview




def render(df):
    st.header("🛰️ Mission Summary Overview")

    # Create mission label: "Mission Type + Launch Vehicle"
    df["MissionLabel"] = df["Mission Type"] + " + " + df["Launch Vehicle"]
    label_counts = df["MissionLabel"].value_counts().reset_index()
    label_counts.columns = ["MissionLabel", "Count"]

    # Show mission label cards
    st.subheader("📌 Mission Types with Launch Vehicles")
    cols = st.columns(min(4, len(label_counts)))  # 4 per row
    for idx, row in label_counts.iterrows():
        cols[idx % 4].metric(label=row["MissionLabel"], value=f"{row['Count']} Missions")

    st.markdown("---")

    # Calculate success/failure rates
    success_rate = df["Mission Success (%)"].mean()
    failure_rate = 100 - success_rate

    # Donut Chart - Success Rate
    success_fig = go.Figure(go.Pie(
        labels=["Success", "Remaining"],
        values=[success_rate, 100 - success_rate],
        hole=0.5,
        marker_colors=["green", "lightgray"],
        textinfo='label+percent'
    ))
    success_fig.update_layout(title="✅ Success Rate")

    # Donut Chart - Failure Rate
    failure_fig = go.Figure(go.Pie(
        labels=["Failure", "Remaining"],
        values=[failure_rate, 100 - failure_rate],
        hole=0.5,
        marker_colors=["red", "lightgray"],
        textinfo='label+percent'
    ))
    failure_fig.update_layout(title="❌ Failure Rate")

    # Total cost
    total_cost = df["Mission Cost (billion USD)"].sum() * 1e9  # to USD

    def format_number(x):
        if x >= 1e9:
            return f"${x/1e9:.1f}B"
        elif x >= 1e6:
            return f"${x/1e6:.1f}M"
        elif x >= 1e3:
            return f"${x/1e3:.1f}K"
        return str(x)

    formatted_cost = format_number(total_cost)

    # Layout for donuts and total cost
    st.subheader("📊 Mission Performance Summary")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.plotly_chart(success_fig, use_container_width=True)
    with col2:
        st.plotly_chart(failure_fig, use_container_width=True)
    with col3:
        st.metric(label="💰 Total Mission Cost", value=formatted_cost)


render(df)

