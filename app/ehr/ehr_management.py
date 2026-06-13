import streamlit as st
import sqlite3
import pandas as pd
import os

DATABASE = "healthcare.db"


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =====================================
# CREATE EHR TABLE
# =====================================

def create_ehr_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ehr(
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor_name TEXT,
        diagnosis TEXT,
        prescription TEXT,
        treatment_plan TEXT,
        vaccination_record TEXT,
        doctor_notes TEXT,
        visit_date TEXT
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
# ADD EHR RECORD
# =====================================

def add_ehr_record():

    st.subheader("➕ Add EHR Record")

    patients = get_patients()
    doctors = get_doctors()

    if len(patients) == 0:
        st.warning("Please add patients first")
        return

    if len(doctors) == 0:
        st.warning("Please add doctors first")
        return

    with st.form("ehr_form"):

        patient_name = st.selectbox(
            "Patient",
            patients
        )

        doctor_name = st.selectbox(
            "Doctor",
            doctors
        )

        diagnosis = st.text_area(
            "Diagnosis"
        )

        prescription = st.text_area(
            "Prescription"
        )

        treatment_plan = st.text_area(
            "Treatment Plan"
        )

        vaccination_record = st.text_area(
            "Vaccination Record"
        )

        doctor_notes = st.text_area(
            "Doctor Notes"
        )

        visit_date = st.date_input(
            "Visit Date"
        )

        submit = st.form_submit_button(
            "Save Record"
        )

        if submit:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO ehr
            (
                patient_name,
                doctor_name,
                diagnosis,
                prescription,
                treatment_plan,
                vaccination_record,
                doctor_notes,
                visit_date
            )
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                patient_name,
                doctor_name,
                diagnosis,
                prescription,
                treatment_plan,
                vaccination_record,
                doctor_notes,
                str(visit_date)
            ))

            conn.commit()
            conn.close()

            st.success(
                "EHR Record Added Successfully"
            )


# =====================================
# VIEW EHR
# =====================================

def view_ehr():

    st.subheader("📋 EHR Records")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM ehr",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Records Found")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================
# SEARCH EHR
# =====================================

def search_ehr():

    st.subheader("🔍 Search Patient EHR")

    patient_name = st.text_input(
        "Patient Name"
    )

    if st.button("Search EHR"):

        conn = get_connection()

        df = pd.read_sql_query(
            """
            SELECT *
            FROM ehr
            WHERE patient_name LIKE ?
            """,
            conn,
            params=(f"%{patient_name}%",)
        )

        conn.close()

        if df.empty:
            st.error("No EHR Found")
        else:
            st.dataframe(
                df,
                use_container_width=True
            )


# =====================================
# UPDATE EHR
# =====================================

def update_ehr():

    st.subheader("✏️ Update EHR")

    record_id = st.number_input(
        "Record ID",
        min_value=1,
        step=1
    )

    diagnosis = st.text_area(
        "New Diagnosis"
    )

    if st.button("Update EHR"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE ehr
        SET diagnosis=?
        WHERE record_id=?
        """,
        (
            diagnosis,
            record_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Record Updated"
        )


# =====================================
# DELETE EHR
# =====================================

def delete_ehr():

    st.subheader("❌ Delete EHR")

    record_id = st.number_input(
        "Record ID",
        min_value=1,
        step=1,
        key="delete_record"
    )

    if st.button("Delete Record"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM ehr
        WHERE record_id=?
        """,
        (record_id,)
        )

        conn.commit()
        conn.close()

        st.success(
            "Record Deleted"
        )


# =====================================
# UPLOAD LAB REPORT
# =====================================

def upload_lab_report():

    st.subheader("📄 Upload Lab Report")

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    uploaded_file = st.file_uploader(
        "Choose File",
        type=[
            "pdf",
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_file:

        filepath = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(filepath, "wb") as f:
            f.write(
                uploaded_file.getbuffer()
            )

        st.success(
            "Report Uploaded Successfully"
        )


# =====================================
# EHR ANALYTICS
# =====================================

def ehr_analytics():

    st.subheader("📊 EHR Analytics")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM ehr",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Data Available")
        return

    st.metric(
        "Total Records",
        len(df)
    )

    disease_counts = (
        df["diagnosis"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(
        disease_counts
    )


# =====================================
# MAIN FUNCTION
# =====================================

def ehr_management():

    create_ehr_table()

    st.title(
        "🩺 Electronic Health Records (EHR)"
    )

    menu = st.sidebar.selectbox(
        "EHR Menu",
        [
            "Add Record",
            "View Records",
            "Search EHR",
            "Update Record",
            "Delete Record",
            "Upload Lab Report",
            "EHR Analytics"
        ]
    )

    if menu == "Add Record":
        add_ehr_record()

    elif menu == "View Records":
        view_ehr()

    elif menu == "Search EHR":
        search_ehr()

    elif menu == "Update Record":
        update_ehr()

    elif menu == "Delete Record":
        delete_ehr()

    elif menu == "Upload Lab Report":
        upload_lab_report()

    elif menu == "EHR Analytics":
        ehr_analytics()