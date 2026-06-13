import streamlit as st
import pandas as pd

def patient_analytics():

    st.title("📊 Patient Analytics")

    try:
        df = pd.read_csv("data/patients.csv")

        st.dataframe(df, use_container_width=True)

        st.metric("Total Patients", len(df))

        if "gender" in df.columns:
            st.subheader("Gender Distribution")
            st.bar_chart(df["gender"].value_counts())

        if "age" in df.columns:
            st.subheader("Age Distribution")
            st.bar_chart(df["age"])

    except Exception as e:
        st.error(f"Error: {e}")