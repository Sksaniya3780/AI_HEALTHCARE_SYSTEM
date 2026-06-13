import streamlit as st
import sqlite3
import pandas as pd
import os

DATABASE = "healthcare.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ==========================
# ADD PATIENT
# ==========================
def add_patient():

    st.title("🏥 Patient Management System")
    st.subheader("➕ Add New Patient")

    with st.form("patient_form"):

        name = st.text_input("Patient Name")

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=0
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        blood_group = st.selectbox(
            "Blood Group",
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )

        phone = st.text_input("Phone Number")

        address = st.text_area("Address")

        disease = st.text_input("Disease")

        allergies = st.text_input("Allergies")

        insurance = st.text_input("Insurance")

        submit = st.form_submit_button("Save Patient")

        if submit:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO patients
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                address,
                disease,
                allergies,
                insurance
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                address,
                disease,
                allergies,
                insurance
            ))

            conn.commit()
            conn.close()

            st.success("✅ Patient Added Successfully")


# ==========================
# VIEW PATIENTS
# ==========================
def view_patients():

    st.subheader("📋 Patient Records")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Patients Found")
    else:
        st.dataframe(df, use_container_width=True)


# ==========================
# SEARCH PATIENT
# ==========================
def search_patient():

    st.subheader("🔍 Search Patient")

    search_name = st.text_input("Enter Patient Name")

    if st.button("Search"):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM patients WHERE name LIKE ?",
            conn,
            params=(f"%{search_name}%",)
        )

        conn.close()

        if df.empty:
            st.error("Patient Not Found")
        else:
            st.dataframe(df, use_container_width=True)


# ==========================
# DELETE PATIENT
# ==========================
def delete_patient():

    st.subheader("❌ Delete Patient")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Patient"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM patients WHERE id=?",
            (patient_id,)
        )

        conn.commit()
        conn.close()

        st.success("Patient Deleted Successfully")


# ==========================
# UPLOAD REPORT
# ==========================
def upload_report():

    st.subheader("📄 Upload Medical Report")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    uploaded_file = st.file_uploader(
        "Choose File",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file:

        filepath = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File Uploaded Successfully")


# ==========================
# MAIN FUNCTION
# ==========================
def patient_management():

    menu = st.sidebar.selectbox(
        "Patient Menu",
        [
            "Add Patient",
            "View Patients",
            "Search Patient",
            "Delete Patient",
            "Upload Report"
        ]
    )

    if menu == "Add Patient":
        add_patient()

    elif menu == "View Patients":
        view_patients()

    elif menu == "Search Patient":
        search_patient()

    elif menu == "Delete Patient":
        delete_patient()

    elif menu == "Upload Report":
        upload_report()


if __name__ == "__main__":
    patient_management()