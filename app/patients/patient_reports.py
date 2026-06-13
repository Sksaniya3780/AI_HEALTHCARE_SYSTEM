import streamlit as st
import pandas as pd

def patient_reports():

    st.title("📑 Patient Reports")

    try:
        df = pd.read_csv("data/patients.csv")

        st.dataframe(df)

        st.download_button(
            "Download Report",
            df.to_csv(index=False),
            file_name="patient_report.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(str(e))