import streamlit as st
import pandas as pd
import os

def excel_reports():

    st.title("📊 Excel Reports")

    try:
        if not os.path.exists("data/patients.csv"):
            st.error("patients.csv not found")
            return

        df = pd.read_csv("data/patients.csv")

        st.dataframe(df)

        excel_file = "data/patient_report.xlsx"

        df.to_excel(
            excel_file,
            index=False
        )

        with open(excel_file, "rb") as file:
            st.download_button(
                label="Download Excel Report",
                data=file,
                file_name="patient_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error: {e}")