import streamlit as st
from app.analytics.patient_analytics import patient_analytics
from app.analytics.resource_analytics import resource_analytics

from app.doctors.doctor_schedule import doctor_schedule

from app.ehr.lab_reports import lab_reports
from app.ehr.prescriptions import prescriptions
from app.ehr.patient_history import patient_history

from app.notifications.appointment_notifications import appointment_notifications

from app.reports.patient_reports import patient_reports
from app.reports.excel_reports import excel_reports
from app.reports.pdf_reports import pdf_reports
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Healthcare System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DATABASE INIT
# ==========================================

from database.db import init_db

init_db()

# ==========================================
# IMPORT MODULES
# ==========================================

# Authentication
try:
    from app.auth.login import login_page
except:
    login_page = None

try:
    from app.auth.register import register_page
except:
    register_page = None

# Patient
try:
    from app.patients.patient_management import patient_management
except:
    patient_management = None

# Doctor
try:
    from app.doctors.doctor_management import doctor_management
except:
    doctor_management = None

# Appointment
try:
    from app.appointments.appointment_management import appointment_management
except:
    appointment_management = None

# EHR
try:
    from app.ehr.ehr_management import ehr_management
except:
    ehr_management = None

# Disease Prediction
try:
    from app.ai_models.disease_prediction import disease_prediction
except:
    disease_prediction = None

# Outcome Prediction
try:
    from app.ai_models.outcome_prediction import outcome_prediction
except:
    outcome_prediction = None

# Treatment
try:
    from app.treatment.treatment_recommendation import treatment_recommendation
except:
    treatment_recommendation = None

# Bed Management
try:
    from app.resources.bed_management import bed_management
except:
    bed_management = None

# Staff Management
try:
    from app.resources.staff_management import staff_management
except:
    staff_management = None

# Resource Allocation
try:
    from app.resources.resource_allocation import resource_allocation
except:
    resource_allocation = None

# Medical Report Analysis
try:
    from app.reports.medical_report_analysis import medical_report_analysis
except:
    medical_report_analysis = None

# Emergency Alert
try:
    from app.notifications.emergency_alert import emergency_alert_system
except:
    emergency_alert_system = None

# Chatbot
try:
    from app.chatbot.chatbot import chatbot_system
except:
    chatbot_system = None

# Analytics
try:
    from app.analytics.dashboard import analytics_dashboard
except:
    analytics_dashboard = None

# Notifications
try:
    from app.notifications.notification import notification_system
except:
    notification_system = None

# Reports
try:
    from app.reports.generate_reports import report_system
except:
    report_system = None

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color:#f5f7fa;
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#1565c0;
}

.subtitle {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

.metric-card {
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class='title'>
    🏥 AI Healthcare Prediction & Resource Management System
    </div>

    <div class='subtitle'>
    Smart Healthcare | AI Diagnostics | Hospital Management
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
    width=120
)
st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Dashboard",

        "🔐 Login",
        "📝 Register",

        "👨‍⚕️ Patient Management",
        "🩺 Doctor Management",
        "📅 Doctor Schedule",
        "📅 Appointment Management",

        "📋 EHR Management",
        "🧪 Lab Reports",
        "💊 Prescriptions",
        "📋 Patient History",

        "🤖 Disease Prediction",
        "📈 Outcome Prediction",

        "💊 Treatment Recommendation",

        "🛏 Bed Management",
        "👨‍⚕️ Staff Management",
        "📦 Resource Allocation",

        "📊 Patient Analytics",
        "📦 Resource Analytics",

        "🧾 Medical Report Analysis",

        "🚨 Emergency Alert System",

        "💬 AI Chatbot",

        "📊 Analytics Dashboard",

        "🔔 Notifications",
        "🔔 Appointment Notifications",

        "📑 Reports",
        "📑 Patient Reports",
        "📊 Excel Reports",
        "📄 PDF Reports"
    ],
    key="main_navigation"
)


        
# ==========================================
# HOME DASHBOARD
# ==========================================

if menu == "🏠 Dashboard":

    st.success(
        "Welcome to AI-Powered Healthcare Prediction & Resource Management System"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Patients", "120")
    c2.metric("Doctors", "35")
    c3.metric("Beds", "250")
    c4.metric("Resources", "500")

    st.markdown("---")

    st.subheader("Available Modules")

    st.write("""
    ✔ Authentication

    ✔ Patient Management

    ✔ Doctor Management

    ✔ Appointment Scheduling

    ✔ Electronic Health Records

    ✔ Disease Prediction

    ✔ Outcome Prediction

    ✔ Treatment Recommendation

    ✔ Bed Management

    ✔ Staff Management

    ✔ Resource Allocation

    ✔ Medical Report Analysis

    ✔ Emergency Alert System

    ✔ AI Chatbot

    ✔ Analytics Dashboard

    ✔ Notifications

    ✔ Report Generation
    """)

# ==========================================
# AUTH MODULES
# ==========================================

elif menu == "🔐 Login":
    if login_page:
        login_page()
    else:
        st.error("login.py not configured")

elif menu == "📝 Register":
    if register_page:
        register_page()
    else:
        st.error("register.py not configured")

# ==========================================
# MANAGEMENT MODULES
# ==========================================

elif menu == "👨‍⚕️ Patient Management":
    if patient_management:
        patient_management()

elif menu == "🩺 Doctor Management":
    if doctor_management:
        doctor_management()

elif menu == "📅 Appointment Management":
    if appointment_management:
        appointment_management()

elif menu == "📋 EHR Management":
    if ehr_management:
        ehr_management()

# ==========================================
# AI MODULES
# ==========================================

elif menu == "🤖 Disease Prediction":
    if disease_prediction:
        disease_prediction()

elif menu == "📈 Outcome Prediction":
    if outcome_prediction:
        outcome_prediction()

elif menu == "💊 Treatment Recommendation":
    if treatment_recommendation:
        treatment_recommendation()

# ==========================================
# RESOURCE MODULES
# ==========================================

elif menu == "🛏 Bed Management":
    if bed_management:
        bed_management()

elif menu == "👨‍⚕️ Staff Management":
    if staff_management:
        staff_management()

elif menu == "📦 Resource Allocation":
    if resource_allocation:
        resource_allocation()

# ==========================================
# REPORT ANALYSIS
# ==========================================

elif menu == "🧾 Medical Report Analysis":
    if medical_report_analysis:
        medical_report_analysis()

# ==========================================
# EMERGENCY MODULE
# ==========================================

elif menu == "🚨 Emergency Alert System":
    if emergency_alert_system:
        emergency_alert_system()

# ==========================================
# CHATBOT
# ==========================================

elif menu == "💬 AI Chatbot":
    if chatbot_system:
        chatbot_system()

# ==========================================
# ANALYTICS
# ==========================================

elif menu == "📊 Analytics Dashboard":
    if analytics_dashboard:
        analytics_dashboard()

# ==========================================
# NOTIFICATIONS
# ==========================================

elif menu == "🔔 Notifications":
    if notification_system:
        notification_system()

# ==========================================
# REPORTS
# ==========================================

elif menu == "📑 Reports":
    if report_system:
        report_system()
elif menu == "📅 Doctor Schedule":
    doctor_schedule()

elif menu == "🧪 Lab Reports":
    lab_reports()

elif menu == "💊 Prescriptions":
    prescriptions()

elif menu == "📋 Patient History":
    patient_history()

elif menu == "📊 Patient Analytics":
    patient_analytics()

elif menu == "📦 Resource Analytics":
    resource_analytics()

elif menu == "🔔 Appointment Notifications":
    appointment_notifications()

elif menu == "📑 Patient Reports":
    patient_reports()

elif menu == "📊 Excel Reports":
    excel_reports()

elif menu == "📄 PDF Reports":
    pdf_reports()
# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <center>
    <b>AI Healthcare Prediction & Resource Management System</b><br>
    Powered by Streamlit • Machine Learning • Healthcare Analytics
    </center>
    """,
    unsafe_allow_html=True
)
