import streamlit as st
import pandas as pd

def patient_reports():

    st.title("📑 Patient Reports")

    try:

        df = pd.read_csv(
            "data/patients.csv"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Patient Report",
            data=csv,
            file_name="patient_report.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")