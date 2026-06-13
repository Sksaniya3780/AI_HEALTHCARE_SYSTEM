import streamlit as st
import pandas as pd

def prescriptions():

    st.title("💊 Prescriptions")

    patient = st.text_input("Patient Name")

    medicine = st.text_area("Medicines")

    if st.button("Save Prescription"):

        data = pd.DataFrame({
            "Patient":[patient],
            "Prescription":[medicine]
        })

        data.to_csv(
            "data/prescriptions.csv",
            mode="a",
            header=False,
            index=False
        )

        st.success("Prescription Saved")