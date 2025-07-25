# Re-import necessary libraries after kernel reset
import pandas as pd

# Reload the uploaded dataset
df = pd.read_csv("/mnt/data/space_missions_dataset.csv")

# Redefine the cleaned summary render function without card styling
def clean_summary_render(df: pd.DataFrame):
    import streamlit as st
    import plotly.graph_objects as go
    from babel.numbers import format_decimal

    st.header("🛰️ Mission Summary Overview")

    # Launch Vehicle Cards
    st.subheader("🚀 Launch Vehicles Overview")
    launch_counts = df["Launch Vehicle"].value_counts().reset_index()
    launch_counts.columns = ["Launch Vehicle", "Count"]
    cols = st.columns(min(4, len(launch_counts)))
    for idx, row in launch_counts.iterrows():
        with cols[idx % 4]:
            st.metric(label=row["Launch Vehicle"], value=f"{row['Count']} Missions")

    # Mission Type Cards
    st.subheader("🎯 Mission Types Overview")
    mission_counts = df["Mission Type"].value_counts().reset_index()
    mission_counts.columns = ["Mission Type", "Count"]
    cols2 = st.columns(min(4, len(mission_counts)))
    for idx, row in mission_counts.iterrows():
        with cols2[idx % 4]:
            st.metric(label=row["Mission Type"], value=f"{row['Count']} Missions")

    st.markdown("---")

    # Donut Charts for Mission Success & Failure Rates
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

    # Total Cost Card
    total_cost = df["Mission Cost (billion USD)"].sum()
    formatted_cost = f"${format_decimal(total_cost, format='#,##0.00')} Billion"

    with col3:
        st.metric(label="💰 Total Mission Cost", value=formatted_cost)

# Function ready to use in Streamlit app
clean_summary_render_code = clean_summary_render.__code__.co_code  # placeholder for deployment note


