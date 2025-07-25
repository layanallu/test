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

# دالة عرض كروت بشكل منسق
def display_cards(title, data, col_num=2):
    st.subheader(title)
    columns = st.columns(col_num)
    for idx, row in data.iterrows():
        col = columns[idx % col_num]
        with col:
            st.markdown(f"<h4 style='margin-bottom:0'>{row[0]}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:gray'>{row[1]} Missions</p>", unsafe_allow_html=True)

# دالة رئيسية
def render(df):
    st.header("🚀 Space Mission Summary")

    # --- Launch Vehicle Cards ---
    lv_counts = df["Launch Vehicle"].value_counts().reset_index()
    lv_counts.columns = ["Launch Vehicle", "Count"]
    display_cards("🛩️ Launch Vehicles", lv_counts)

    st.markdown("---")

    # --- Mission Type Cards ---
    mt_counts = df["Mission Type"].value_counts().reset_index()
    mt_counts.columns = ["Mission Type", "Count"]
    display_cards("📡 Mission Types", mt_counts)

    st.markdown("---")

    # --- Success & Failure Rate Donut ---
    st.subheader("📊 Mission Success Rate")

    success_rate = df["Mission Success (%)"].mean()
    failure_rate = 100 - success_rate

    donut_fig = go.Figure(go.Pie(
        labels=["Success", "Failure"],
        values=[success_rate, failure_rate],
        hole=0.6,
        marker_colors=["green", "red"],
        textinfo="label+percent"
    ))

    donut_fig.update_layout(
        showlegend=True,
        annotations=[dict(
            text=f"{success_rate:.1f}%",
            x=0.5, y=0.5, font_size=24, showarrow=False
        )]
    )

    st.plotly_chart(donut_fig, use_container_width=True)

    # --- Total Cost ---
    st.subheader("💰 Total Mission Cost")
    total_cost = df["Mission Cost (billion USD)"].sum() * 1e9  # حولناها لـ دولار
    formatted_cost = format_number(total_cost)
    st.metric(label="Total Cost", value=formatted_cost)

# تشغيل الدالة
render(df)
