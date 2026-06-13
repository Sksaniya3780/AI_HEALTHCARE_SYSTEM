import streamlit as st
import pandas as pd

def lab_reports():

    st.title("🧪 Lab Reports")

    uploaded = st.file_uploader(
        "Upload Lab Report",
        type=["csv"]
    )

    if uploaded:

        df = pd.read_csv(uploaded)

        st.dataframe(df)

        st.success("Report Uploaded Successfully")