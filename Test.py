import pandas as pd
import plotly.graph_objects as go
import streamlit as st



# Load Data
df = pd.read_csv("space_missions_dataset.csv")
# Format large numbers clearly
def format_number(x):
    if x >= 1e9:
        return f"${x / 1e9:,.1f}B"
    elif x >= 1e6:
        return f"${x / 1e6:,.1f}M"
    elif x >= 1e3:
        return f"${x / 1e3:,.1f}K"
    return str(x)

# Display cards (launch vehicles or mission types)
def display_cards(title, data, col_num=2):
    st.subheader(title)
    columns = st.columns(col_num)
    for idx, row in data.iterrows():
        col = columns[idx % col_num]
        with col:
            st.markdown(f"<h4 style='margin-bottom:0; font-size:20px'>{row[0]}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:gray; font-size:16px'>{row[1]} Missions</p>", unsafe_allow_html=True)

# Main render function
def render(df):
    st.title("🚀 Space Mission Dashboard")

    # Launch Vehicle Cards
    lv_counts = df["Launch Vehicle"].value_counts().reset_index()
    lv_counts.columns = ["Launch Vehicle", "Count"]
    display_cards("🛩️ Launch Vehicles", lv_counts)

    st.markdown("---")

    # Mission Type Cards
    mt_counts = df["Mission Type"].value_counts().reset_index()
    mt_counts.columns = ["Mission Type", "Count"]
    display_cards("📡 Mission Types", mt_counts)

    st.markdown("---")

    # Success & Failure Donuts
    st.subheader("📊 Mission Outcome Distribution")
    success_rate = df["Mission Success (%)"].mean()
    failure_rate = 100 - success_rate

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Success Rate**")
        success_fig = go.Figure(go.Pie(
            labels=["Success", ""],
            values=[success_rate, 100 - success_rate],
            hole=0.6,
            marker_colors=["green", "#f0f0f0"],
            textinfo="none"
        ))
        success_fig.update_layout(
            height=350, width=350,
            annotations=[dict(
                text=f"{success_rate:.1f}%", x=0.5, y=0.5, font_size=24, showarrow=False
            )],
            showlegend=False
        )
        st.plotly_chart(success_fig, use_container_width=True)

    with col2:
        st.markdown("**Failure Rate**")
        failure_fig = go.Figure(go.Pie(
            labels=["Failure", ""],
            values=[failure_rate, 100 - failure_rate],
            hole=0.6,
            marker_colors=["red", "#f0f0f0"],
            textinfo="none"
        ))
        failure_fig.update_layout(
            height=350, width=350,
            annotations=[dict(
                text=f"{failure_rate:.1f}%", x=0.5, y=0.5, font_size=24, showarrow=False
            )],
            showlegend=False
        )
        st.plotly_chart(failure_fig, use_container_width=True)

    # Total Cost
    st.subheader("💰 Total Mission Cost")
    total_cost = df["Mission Cost (billion USD)"].sum() * 1e9
    formatted_cost = format_number(total_cost)
    st.metric(label="Total Cost", value=formatted_cost)

# Run the app
render(df)
