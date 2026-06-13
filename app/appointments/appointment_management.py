import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

DATABASE = "healthcare.db"


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =====================================
# CREATE TABLE
# =====================================

def create_appointment_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor_name TEXT,
        appointment_date TEXT,
        appointment_time TEXT,
        reason TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# GET PATIENTS
# =====================================

def get_patients():

    conn = get_connection()

    try:
        df = pd.read_sql_query(
            "SELECT name FROM patients",
            conn
        )

        conn.close()

        return df["name"].tolist()

    except:
        conn.close()
        return []


# =====================================
# GET DOCTORS
# =====================================

def get_doctors():

    conn = get_connection()

    try:
        df = pd.read_sql_query(
            "SELECT name FROM doctors",
            conn
        )

        conn.close()

        return df["name"].tolist()

    except:
        conn.close()
        return []


# =====================================
# BOOK APPOINTMENT
# =====================================

def book_appointment():

    st.subheader("📅 Book Appointment")

    patients = get_patients()
    doctors = get_doctors()

    if len(patients) == 0:
        st.warning("Add Patients First")
        return

    if len(doctors) == 0:
        st.warning("Add Doctors First")
        return

    with st.form("appointment_form"):

        patient_name = st.selectbox(
            "Select Patient",
            patients
        )

        doctor_name = st.selectbox(
            "Select Doctor",
            doctors
        )

        appointment_date = st.date_input(
            "Appointment Date",
            min_value=date.today()
        )

        appointment_time = st.selectbox(
            "Appointment Time",
            [
                "09:00 AM",
                "10:00 AM",
                "11:00 AM",
                "12:00 PM",
                "02:00 PM",
                "03:00 PM",
                "04:00 PM"
            ]
        )

        reason = st.text_area(
            "Reason for Visit"
        )

        submit = st.form_submit_button(
            "Book Appointment"
        )

        if submit:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO appointments
            (
                patient_name,
                doctor_name,
                appointment_date,
                appointment_time,
                reason,
                status
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                patient_name,
                doctor_name,
                str(appointment_date),
                appointment_time,
                reason,
                "Pending"
            ))

            conn.commit()
            conn.close()

            st.success(
                "Appointment Booked Successfully"
            )


# =====================================
# VIEW APPOINTMENTS
# =====================================

def view_appointments():

    st.subheader("📋 Appointment Records")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM appointments",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Appointments Found")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================
# SEARCH APPOINTMENT
# =====================================

def search_appointment():

    st.subheader("🔍 Search Appointment")

    patient_name = st.text_input(
        "Patient Name"
    )

    if st.button("Search"):

        conn = get_connection()

        df = pd.read_sql_query(
            """
            SELECT *
            FROM appointments
            WHERE patient_name LIKE ?
            """,
            conn,
            params=(f"%{patient_name}%",)
        )

        conn.close()

        if df.empty:
            st.error("No Appointment Found")
        else:
            st.dataframe(
                df,
                use_container_width=True
            )


# =====================================
# UPDATE STATUS
# =====================================

def update_status():

    st.subheader("✅ Update Appointment Status")

    appointment_id = st.number_input(
        "Appointment ID",
        min_value=1,
        step=1
    )

    status = st.selectbox(
        "Status",
        [
            "Pending",
            "Approved",
            "Completed",
            "Cancelled"
        ]
    )

    if st.button("Update Status"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE appointments
        SET status=?
        WHERE appointment_id=?
        """,
        (
            status,
            appointment_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Status Updated"
        )


# =====================================
# RESCHEDULE
# =====================================

def reschedule_appointment():

    st.subheader("🔄 Reschedule Appointment")

    appointment_id = st.number_input(
        "Appointment ID",
        min_value=1,
        step=1,
        key="reschedule"
    )

    new_date = st.date_input(
        "New Appointment Date"
    )

    if st.button("Reschedule"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE appointments
        SET appointment_date=?
        WHERE appointment_id=?
        """,
        (
            str(new_date),
            appointment_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Appointment Rescheduled"
        )


# =====================================
# CANCEL APPOINTMENT
# =====================================

def cancel_appointment():

    st.subheader("❌ Cancel Appointment")

    appointment_id = st.number_input(
        "Appointment ID",
        min_value=1,
        step=1,
        key="cancel"
    )

    if st.button("Cancel Appointment"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE appointments
        SET status='Cancelled'
        WHERE appointment_id=?
        """,
        (appointment_id,)
        )

        conn.commit()
        conn.close()

        st.success(
            "Appointment Cancelled"
        )


# =====================================
# ANALYTICS
# =====================================

def appointment_analytics():

    st.subheader("📊 Appointment Analytics")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM appointments",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Data Available")
        return

    st.metric(
        "Total Appointments",
        len(df)
    )

    st.bar_chart(
        df["status"].value_counts()
    )


# =====================================
# MAIN FUNCTION
# =====================================

def appointment_management():

    create_appointment_table()

    st.title("📅 Appointment Scheduling System")

    menu = st.sidebar.selectbox(
        "Appointment Menu",
        [
            "Book Appointment",
            "View Appointments",
            "Search Appointment",
            "Update Status",
            "Reschedule Appointment",
            "Cancel Appointment",
            "Appointment Analytics"
        ]
    )

    if menu == "Book Appointment":
        book_appointment()

    elif menu == "View Appointments":
        view_appointments()

    elif menu == "Search Appointment":
        search_appointment()

    elif menu == "Update Status":
        update_status()

    elif menu == "Reschedule Appointment":
        reschedule_appointment()

    elif menu == "Cancel Appointment":
        cancel_appointment()

    elif menu == "Appointment Analytics":
        appointment_analytics()