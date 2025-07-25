import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv("space_missions_dataset.csv")

# تنسيق الأرقام الكبيرة بشكل واضح
def format_number(x):
    if x >= 1e9:
        return f"${x / 1e9:,.1f}B"
    elif x >= 1e6:
        return f"${x / 1e6:,.1f}M"
    elif x >= 1e3:
        return f"${x / 1e3:,.1f}K"
    return str(x)

# دالة رئيسية
def render(df):
    st.header("🚀 Space Mission Summary")

    # --- Launch Vehicle Cards ---
    st.subheader("🛩️ Launch Vehicles")
    lv_counts = df["Launch Vehicle"].value_counts().reset_index()
    lv_counts.columns = ["Launch Vehicle", "Count"]
    for idx, row in lv_counts.iterrows():
        st.metric(label=row["Launch Vehicle"], value=f"{row['Count']} Missions")

    st.markdown("---")

    # --- Mission Type Cards ---
    st.subheader("📡 Mission Types")
    mt_counts = df["Mission Type"].value_counts().reset_index()
    mt_counts.columns = ["Mission Type", "Count"]
    for idx, row in mt_counts.iterrows():
        st.metric(label=row["Mission Type"], value=f"{row['Count']} Missions")

    st.markdown("---")

    # --- Success Rate Donut ---
    st.subheader("✅ Mission Success Rate")

    success_rate = df["Mission Success (%)"].mean()

    success_fig = go.Figure(go.Pie(
        labels=["Success"],
        values=[success_rate],
        hole=0.6,
        marker_colors=["green"],
        textinfo="none"
    ))

    success_fig.update_layout(
        showlegend=False,
        annotations=[dict(
            text=f"{success_rate:.1f}%",
            x=0.5, y=0.5, font_size=24, showarrow=False
        )]
    )

    st.plotly_chart(success_fig, use_container_width=True)

    # --- Total Cost ---
    st.subheader("💰 Total Mission Cost")
    total_cost = df["Mission Cost (billion USD)"].sum() * 1e9  # حولناها لـ دولار
    formatted_cost = format_number(total_cost)
    st.metric(label="Total Cost", value=formatted_cost)

# تشغيل الدالة
render(df)
