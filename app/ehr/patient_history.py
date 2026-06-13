import streamlit as st
import pandas as pd

def patient_history():

    st.title("📋 Patient History")

    try:

        df = pd.read_csv(
            "data/patients.csv"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        patient = st.selectbox(
            "Select Patient",
            df["name"]
        )

        patient_data = df[
            df["name"] == patient
        ]

        st.subheader(
            "Patient Details"
        )

        st.dataframe(
            patient_data,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error: {e}")