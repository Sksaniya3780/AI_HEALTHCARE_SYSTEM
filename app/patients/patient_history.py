import streamlit as st
import pandas as pd

def patient_history():

    st.title("📋 Patient History")

    try:
        df = pd.read_csv("data/patients.csv")

        patient = st.selectbox(
            "Select Patient",
            df["name"]
        )

        st.write(
            df[df["name"] == patient]
        )

    except Exception as e:
        st.error(str(e))