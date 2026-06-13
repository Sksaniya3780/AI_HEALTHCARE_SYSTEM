import streamlit as st
import pandas as pd

def resource_analytics():

    st.title("📦 Resource Analytics")

    try:
        df = pd.read_csv("data/resources.csv")

        st.dataframe(df)

        st.metric("Total Resources", len(df))

        if "available" in df.columns:
            st.subheader("Available Resources")
            st.bar_chart(df.set_index("resource_name")["available"])

    except Exception as e:
        st.error(str(e))