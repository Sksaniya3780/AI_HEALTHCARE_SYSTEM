import streamlit as st
import sqlite3
import pandas as pd

DATABASE = "healthcare.db"


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =====================================
# CREATE DOCTOR TABLE
# =====================================

def create_doctor_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        qualification TEXT,
        experience INTEGER,
        phone TEXT,
        email TEXT,
        available_slots TEXT
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# ADD DOCTOR
# =====================================

def add_doctor():

    st.subheader("➕ Add Doctor")

    with st.form("doctor_form"):

        name = st.text_input("Doctor Name")

        specialization = st.selectbox(
            "Specialization",
            [
                "Cardiology",
                "Neurology",
                "Orthopedics",
                "Dermatology",
                "Pediatrics",
                "General Medicine",
                "Gynecology",
                "Oncology"
            ]
        )

        department = st.text_input("Department")

        qualification = st.text_input("Qualification")

        experience = st.number_input(
            "Experience (Years)",
            min_value=0,
            max_value=50
        )

        phone = st.text_input("Phone Number")

        email = st.text_input("Email")

        available_slots = st.text_input(
            "Available Slots (Example: 10AM-12PM)"
        )

        submit = st.form_submit_button(
            "Save Doctor"
        )

        if submit:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO doctors
            (
                name,
                specialization,
                department,
                qualification,
                experience,
                phone,
                email,
                available_slots
            )
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                name,
                specialization,
                department,
                qualification,
                experience,
                phone,
                email,
                available_slots
            ))

            conn.commit()
            conn.close()

            st.success(
                "Doctor Added Successfully"
            )


# =====================================
# VIEW DOCTORS
# =====================================

def view_doctors():

    st.subheader("👨‍⚕️ Doctor Records")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM doctors",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Doctors Found")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================
# SEARCH DOCTOR
# =====================================

def search_doctor():

    st.subheader("🔍 Search Doctor")

    search_name = st.text_input(
        "Enter Doctor Name"
    )

    if st.button("Search Doctor"):

        conn = get_connection()

        query = """
        SELECT *
        FROM doctors
        WHERE name LIKE ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(f"%{search_name}%",)
        )

        conn.close()

        if df.empty:
            st.error("Doctor Not Found")
        else:
            st.dataframe(
                df,
                use_container_width=True
            )


# =====================================
# UPDATE DOCTOR
# =====================================

def update_doctor():

    st.subheader("✏️ Update Doctor")

    doctor_id = st.number_input(
        "Doctor ID",
        min_value=1,
        step=1
    )

    conn = get_connection()

    doctor = pd.read_sql_query(
        """
        SELECT *
        FROM doctors
        WHERE doctor_id=?
        """,
        conn,
        params=(doctor_id,)
    )

    conn.close()

    if not doctor.empty:

        st.success("Doctor Found")

        specialization = st.text_input(
            "Specialization",
            value=doctor.iloc[0]["specialization"]
        )

        available_slots = st.text_input(
            "Available Slots",
            value=doctor.iloc[0]["available_slots"]
        )

        if st.button("Update Doctor"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            UPDATE doctors
            SET specialization=?,
                available_slots=?
            WHERE doctor_id=?
            """,
            (
                specialization,
                available_slots,
                doctor_id
            ))

            conn.commit()
            conn.close()

            st.success(
                "Doctor Updated Successfully"
            )


# =====================================
# DELETE DOCTOR
# =====================================

def delete_doctor():

    st.subheader("❌ Delete Doctor")

    doctor_id = st.number_input(
        "Doctor ID",
        min_value=1,
        step=1,
        key="delete_doctor"
    )

    if st.button("Delete Doctor"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM doctors
        WHERE doctor_id=?
        """,
        (doctor_id,)
        )

        conn.commit()
        conn.close()

        st.success(
            "Doctor Deleted Successfully"
        )


# =====================================
# DOCTOR ANALYTICS
# =====================================

def doctor_analytics():

    st.subheader("📊 Doctor Analytics")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM doctors",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Data Available")
        return

    st.metric(
        "Total Doctors",
        len(df)
    )

    st.bar_chart(
        df["specialization"].value_counts()
    )


# =====================================
# MAIN MODULE
# =====================================

def doctor_management():

    create_doctor_table()

    st.title("👨‍⚕️ Doctor Management System")

    menu = st.sidebar.selectbox(
        "Doctor Menu",
        [
            "Add Doctor",
            "View Doctors",
            "Search Doctor",
            "Update Doctor",
            "Delete Doctor",
            "Doctor Analytics"
        ]
    )

    if menu == "Add Doctor":
        add_doctor()

    elif menu == "View Doctors":
        view_doctors()

    elif menu == "Search Doctor":
        search_doctor()

    elif menu == "Update Doctor":
        update_doctor()

    elif menu == "Delete Doctor":
        delete_doctor()

    elif menu == "Doctor Analytics":
        doctor_analytics()