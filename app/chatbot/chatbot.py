import streamlit as st
import pandas as pd
from datetime import datetime


# =====================================
# INITIALIZE CHAT
# =====================================

def initialize_chat():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


# =====================================
# CHATBOT LOGIC
# =====================================

def chatbot_response(user_input):

    text = user_input.lower()

    # Symptoms

    if "fever" in text:
        return """
Possible causes:
• Viral Infection
• Flu
• COVID-like Symptoms

Recommendation:
Drink fluids and consult a doctor if fever persists.
"""

    elif "diabetes" in text:
        return """
Diabetes Guidance:

• Monitor blood sugar regularly
• Follow a low sugar diet
• Exercise daily
• Schedule endocrinologist consultation
"""

    elif "heart" in text:
        return """
Heart Health Advice:

• Reduce salt intake
• Monitor blood pressure
• Exercise regularly
• Consult a cardiologist
"""

    elif "appointment" in text:
        return """
Appointment Help:

1. Open Appointment Module
2. Select Doctor
3. Choose Time Slot
4. Confirm Booking
"""

    elif "medicine" in text:
        return """
Medication Reminder:

• Take medicines on time
• Never skip doses
• Maintain prescription records
"""

    elif "hospital" in text:
        return """
Hospital Services:

• Patient Management
• Doctor Consultation
• Emergency Services
• Resource Management
• AI Disease Prediction
"""

    elif "help" in text:

        return """
Available Commands:

• fever
• diabetes
• heart
• appointment
• medicine
• hospital
"""

    else:

        return """
I am Healthcare AI Assistant.

Try asking:

• fever symptoms
• diabetes advice
• heart disease
• appointment booking
• medicine reminder
"""


# =====================================
# CHAT INTERFACE
# =====================================

def chatbot_interface():

    initialize_chat()

    st.subheader(
        "💬 Healthcare AI Chatbot"
    )

    user_input = st.text_input(
        "Ask Your Question"
    )

    if st.button("Send"):

        if user_input:

            response = chatbot_response(
                user_input
            )

            st.session_state.chat_history.append(
                (
                    datetime.now().strftime(
                        "%H:%M:%S"
                    ),
                    user_input,
                    response
                )
            )

    st.subheader("Chat History")

    for chat in reversed(
        st.session_state.chat_history
    ):

        time, question, answer = chat

        st.markdown(
            f"""
**🕒 {time}**

**👤 User:**
{question}

**🤖 Assistant:**
{answer}
---
"""
        )


# =====================================
# SYMPTOM CHECKER
# =====================================

def symptom_checker():

    st.subheader(
        "🩺 Symptom Checker"
    )

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    fatigue = st.checkbox("Fatigue")
    chest_pain = st.checkbox("Chest Pain")

    if st.button("Analyze Symptoms"):

        if fever and cough:

            st.warning(
                "Possible Flu or Viral Infection"
            )

        if chest_pain:

            st.error(
                "Consult Cardiologist Immediately"
            )

        if fatigue:

            st.info(
                "Recommend Blood Test"
            )


# =====================================
# MEDICATION REMINDER
# =====================================

def medication_reminder():

    st.subheader(
        "💊 Medication Reminder"
    )

    medicine = st.text_input(
        "Medicine Name"
    )

    reminder_time = st.time_input(
        "Reminder Time"
    )

    if st.button("Set Reminder"):

        st.success(
            f"Reminder Set For {medicine}"
        )

        st.info(
            f"Time: {reminder_time}"
        )


# =====================================
# FAQ
# =====================================

def faq_module():

    st.subheader(
        "❓ Hospital FAQ"
    )

    faq = st.selectbox(
        "Select Question",
        [
            "Hospital Timing",
            "Appointment Booking",
            "Emergency Services",
            "Doctor Availability"
        ]
    )

    if faq == "Hospital Timing":

        st.info(
            "Hospital Open 24x7"
        )

    elif faq == "Appointment Booking":

        st.info(
            "Use Appointment Module"
        )

    elif faq == "Emergency Services":

        st.info(
            "Emergency Available 24x7"
        )

    elif faq == "Doctor Availability":

        st.info(
            "Check Doctor Module"
        )


# =====================================
# MAIN FUNCTION
# =====================================

def chatbot_system():

    st.title(
        "🤖 AI Healthcare Chatbot"
    )

    menu = st.sidebar.selectbox(
        "Chatbot Menu",
        [
            "AI Chat",
            "Symptom Checker",
            "Medication Reminder",
            "FAQ"
        ]
    )

    if menu == "AI Chat":
        chatbot_interface()

    elif menu == "Symptom Checker":
        symptom_checker()

    elif menu == "Medication Reminder":
        medication_reminder()

    elif menu == "FAQ":
        faq_module()