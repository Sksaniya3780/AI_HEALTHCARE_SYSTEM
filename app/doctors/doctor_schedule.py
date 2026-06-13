import streamlit as st
import pandas as pd

def doctor_schedule():

    st.title("👨‍⚕️ Doctor Schedule")

    try:
        df = pd.read_csv("data/doctors.csv")

        st.dataframe(df)

        doctor = st.selectbox(
            "Select Doctor",
            df["name"]
        )

        selected = df[df["name"] == doctor]

        st.write(selected)

    except Exception as e:
        st.error(str(e))