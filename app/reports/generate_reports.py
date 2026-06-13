import streamlit as st
import pandas as pd
import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

DATABASE = "healthcare.db"


# =====================================
# DATABASE
# =====================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =====================================
# CREATE PDF
# =====================================

def create_pdf_report(title, content):

    filename = f"{title}.pdf"

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            title,
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            content,
            styles["BodyText"]
        )
    )

    doc.build(elements)

    return filename


# =====================================
# PATIENT REPORT
# =====================================

def patient_report():

    st.subheader(
        "👤 Patient Report"
    )

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM patients",
            conn
        )

        conn.close()

        st.dataframe(df)

        if st.button(
            "Generate Patient PDF"
        ):

            filename = create_pdf_report(
                "Patient_Report",
                df.to_html()
            )

            st.success(
                f"Generated: {filename}"
            )

    except:

        st.error(
            "Patient Data Not Found"
        )


# =====================================
# DOCTOR REPORT
# =====================================

def doctor_report():

    st.subheader(
        "👨‍⚕️ Doctor Report"
    )

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM doctors",
            conn
        )

        conn.close()

        st.dataframe(df)

        if st.button(
            "Generate Doctor PDF"
        ):

            filename = create_pdf_report(
                "Doctor_Report",
                df.to_html()
            )

            st.success(
                f"Generated: {filename}"
            )

    except:

        st.error(
            "Doctor Data Not Found"
        )


# =====================================
# APPOINTMENT REPORT
# =====================================

def appointment_report():

    st.subheader(
        "📅 Appointment Report"
    )

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM appointments",
            conn
        )

        conn.close()

        st.dataframe(df)

        if st.button(
            "Generate Appointment PDF"
        ):

            filename = create_pdf_report(
                "Appointment_Report",
                df.to_html()
            )

            st.success(
                f"Generated: {filename}"
            )

    except:

        st.error(
            "Appointment Data Not Found"
        )


# =====================================
# HOSPITAL SUMMARY REPORT
# =====================================

def hospital_report():

    st.subheader(
        "🏥 Hospital Summary"
    )

    try:

        conn = get_connection()

        patients = pd.read_sql_query(
            "SELECT COUNT(*) total FROM patients",
            conn
        )["total"][0]

        doctors = pd.read_sql_query(
            "SELECT COUNT(*) total FROM doctors",
            conn
        )["total"][0]

        appointments = pd.read_sql_query(
            "SELECT COUNT(*) total FROM appointments",
            conn
        )["total"][0]

        conn.close()

        content = f"""
        Total Patients: {patients}<br/>
        Total Doctors: {doctors}<br/>
        Total Appointments: {appointments}
        """

        st.write(content)

        if st.button(
            "Generate Hospital Report"
        ):

            filename = create_pdf_report(
                "Hospital_Report",
                content
            )

            st.success(
                f"Generated: {filename}"
            )

    except:

        st.error(
            "Unable To Generate Report"
        )


# =====================================
# MAIN
# =====================================

def report_system():

    st.title(
        "📑 Report Generation System"
    )

    menu = st.sidebar.selectbox(
        "Report Menu",
        [
            "Patient Report",
            "Doctor Report",
            "Appointment Report",
            "Hospital Report"
        ]
    )

    if menu == "Patient Report":
        patient_report()

    elif menu == "Doctor Report":
        doctor_report()

    elif menu == "Appointment Report":
        appointment_report()

    elif menu == "Hospital Report":
        hospital_report()