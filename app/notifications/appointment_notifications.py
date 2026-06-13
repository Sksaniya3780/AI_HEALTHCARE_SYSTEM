import streamlit as st
import pandas as pd

def appointment_notifications():

    st.title("🔔 Appointment Notifications")

    try:
        df = pd.read_csv("data/appointments.csv")

        pending = df[df["status"] == "Pending"]

        st.subheader("Pending Appointments")

        st.dataframe(
            pending,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error: {e}")