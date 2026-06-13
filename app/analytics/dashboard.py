import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DATABASE = "healthcare.db"


# ======================================
# DATABASE CONNECTION
# ======================================

def get_connection():
    return sqlite3.connect(DATABASE)


# ======================================
# SAFE COUNT FUNCTION
# ======================================

def get_count(table_name):

    try:
        conn = get_connection()

        count = pd.read_sql_query(
            f"SELECT COUNT(*) AS total FROM {table_name}",
            conn
        )

        conn.close()

        return int(count["total"][0])

    except:
        return 0


# ======================================
# ADMIN DASHBOARD
# ======================================

def admin_dashboard():

    st.subheader("🏥 Hospital Overview")

    patients = get_count("patients")
    doctors = get_count("doctors")
    appointments = get_count("appointments")
    beds = get_count("beds")
    staff = get_count("staff")
    resources = get_count("resources")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Patients",
        patients
    )

    col2.metric(
        "Doctors",
        doctors
    )

    col3.metric(
        "Appointments",
        appointments
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Beds",
        beds
    )

    col5.metric(
        "Staff",
        staff
    )

    col6.metric(
        "Resources",
        resources
    )

    st.divider()

    chart_data = pd.DataFrame({
        "Module": [
            "Patients",
            "Doctors",
            "Appointments",
            "Beds",
            "Staff",
            "Resources"
        ],
        "Count": [
            patients,
            doctors,
            appointments,
            beds,
            staff,
            resources
        ]
    })

    fig = px.bar(
        chart_data,
        x="Module",
        y="Count",
        title="Hospital Statistics"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ======================================
# PATIENT ANALYTICS
# ======================================

def patient_dashboard():

    st.subheader("👨‍⚕️ Patient Dashboard")

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM patients",
            conn
        )

        conn.close()

        st.dataframe(
            df,
            use_container_width=True
        )

        if "gender" in df.columns:

            fig = px.pie(
                df,
                names="gender",
                title="Gender Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    except:

        st.warning(
            "Patient Data Not Available"
        )


# ======================================
# DOCTOR DASHBOARD
# ======================================

def doctor_dashboard():

    st.subheader("👨‍⚕️ Doctor Dashboard")

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM doctors",
            conn
        )

        conn.close()

        st.dataframe(
            df,
            use_container_width=True
        )

        if "specialization" in df.columns:

            fig = px.histogram(
                df,
                x="specialization",
                title="Doctor Specializations"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    except:

        st.warning(
            "Doctor Data Not Available"
        )


# ======================================
# BED ANALYTICS
# ======================================

def bed_dashboard():

    st.subheader("🛏 Bed Analytics")

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM beds",
            conn
        )

        conn.close()

        fig = px.pie(
            df,
            names="status",
            title="Bed Occupancy"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except:

        st.warning(
            "Bed Data Not Available"
        )


# ======================================
# RESOURCE ANALYTICS
# ======================================

def resource_dashboard():

    st.subheader("📦 Resource Analytics")

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM resources",
            conn
        )

        conn.close()

        fig = px.bar(
            df,
            x="resource_name",
            y="available",
            title="Available Resources"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except:

        st.warning(
            "Resource Data Not Available"
        )


# ======================================
# EMERGENCY ANALYTICS
# ======================================

def emergency_dashboard():

    st.subheader("🚨 Emergency Analytics")

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM emergency_alerts",
            conn
        )

        conn.close()

        fig = px.histogram(
            df,
            x="severity",
            title="Emergency Alerts"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except:

        st.warning(
            "Emergency Data Not Available"
        )


# ======================================
# MAIN DASHBOARD
# ======================================

def analytics_dashboard():

    st.title(
        "📊 AI Healthcare Analytics Dashboard"
    )

    menu = st.sidebar.selectbox(
        "Dashboard Menu",
        [
            "Hospital Overview",
            "Patient Dashboard",
            "Doctor Dashboard",
            "Bed Analytics",
            "Resource Analytics",
            "Emergency Analytics"
        ]
    )

    if menu == "Hospital Overview":
        admin_dashboard()

    elif menu == "Patient Dashboard":
        patient_dashboard()

    elif menu == "Doctor Dashboard":
        doctor_dashboard()

    elif menu == "Bed Analytics":
        bed_dashboard()

    elif menu == "Resource Analytics":
        resource_dashboard()

    elif menu == "Emergency Analytics":
        emergency_dashboard()