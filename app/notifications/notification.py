import streamlit as st
from datetime import datetime


# =====================================
# EMAIL NOTIFICATION
# =====================================

def send_email():

    st.subheader("📧 Email Notification")

    recipient = st.text_input(
        "Recipient Email"
    )

    subject = st.text_input(
        "Subject"
    )

    message = st.text_area(
        "Message"
    )

    if st.button("Send Email"):

        st.success(
            f"Email Sent To {recipient}"
        )

        st.info(
            f"Subject: {subject}"
        )


# =====================================
# SMS NOTIFICATION
# =====================================

def send_sms():

    st.subheader("📱 SMS Notification")

    phone = st.text_input(
        "Phone Number"
    )

    message = st.text_area(
        "SMS Message"
    )

    if st.button("Send SMS"):

        st.success(
            f"SMS Sent To {phone}"
        )


# =====================================
# APPOINTMENT REMINDER
# =====================================

def appointment_reminder():

    st.subheader(
        "📅 Appointment Reminder"
    )

    patient = st.text_input(
        "Patient Name"
    )

    date = st.date_input(
        "Appointment Date"
    )

    if st.button(
        "Send Reminder"
    ):

        st.success(
            f"Reminder Sent To {patient}"
        )

        st.info(
            f"Appointment Date: {date}"
        )


# =====================================
# MEDICINE REMINDER
# =====================================

def medicine_reminder():

    st.subheader(
        "💊 Medicine Reminder"
    )

    patient = st.text_input(
        "Patient Name"
    )

    medicine = st.text_input(
        "Medicine"
    )

    if st.button(
        "Send Medicine Reminder"
    ):

        st.success(
            f"Reminder Sent For {medicine}"
        )


# =====================================
# EMERGENCY ALERT
# =====================================

def emergency_notification():

    st.subheader(
        "🚨 Emergency Notification"
    )

    patient = st.text_input(
        "Patient Name"
    )

    emergency = st.text_area(
        "Emergency Message"
    )

    if st.button(
        "Send Emergency Alert"
    ):

        st.error(
            f"Emergency Alert Sent For {patient}"
        )


# =====================================
# MAIN
# =====================================

def notification_system():

    st.title(
        "🔔 Notification System"
    )

    menu = st.sidebar.selectbox(
        "Notification Menu",
        [
            "Email",
            "SMS",
            "Appointment Reminder",
            "Medicine Reminder",
            "Emergency Alert"
        ]
    )

    if menu == "Email":
        send_email()

    elif menu == "SMS":
        send_sms()

    elif menu == "Appointment Reminder":
        appointment_reminder()

    elif menu == "Medicine Reminder":
        medicine_reminder()

    elif menu == "Emergency Alert":
        emergency_notification()