import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load the dataset
df = pd.read_csv("space_missions_dataset.csv")


st.subheader("Launch Vehicle Stats")

# نجيب أكثر 6 مركبات استخدامًا
top_vehicles = df['Launch Vehicle'].value_counts().head(6)

col1, col2 = st.columns(2)

# أول 3 في العمود الأول
with col1:
    for name, count in top_vehicles.items():
        st.markdown(f"### {name}")
        st.markdown(f"{count} missions")
        if top_vehicles.index.get_loc(name) == 2:
            break

# آخر 3 في العمود الثاني
with col2:
    for name, count in list(top_vehicles.items())[3:]:
        st.markdown(f"### {name}")
        st.markdown(f"{count} missions")

# ----------------------------

st.subheader("Mission Type Stats")

top_types = df['Mission Type'].value_counts().head(6)

col3, col4 = st.columns(2)

with col3:
    for name, count in top_types.items():
        st.markdown(f"### {name}")
        st.markdown(f"{count} missions")
        if top_types.index.get_loc(name) == 2:
            break

with col4:
    for name, count in list(top_types.items())[3:]:
        st.markdown(f"### {name}")
        st.markdown(f"{count} missions")

