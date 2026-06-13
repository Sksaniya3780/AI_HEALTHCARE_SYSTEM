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
# CREATE TABLE
# =====================================

def create_bed_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beds(
        bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ward_type TEXT,
        status TEXT,
        patient_name TEXT
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# ADD BED
# =====================================

def add_bed():

    st.subheader("➕ Add New Bed")

    ward_type = st.selectbox(
        "Ward Type",
        [
            "General Ward",
            "ICU",
            "Emergency",
            "Private Room"
        ]
    )

    if st.button("Add Bed"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO beds
        (
            ward_type,
            status,
            patient_name
        )
        VALUES (?, ?, ?)
        """,
        (
            ward_type,
            "Available",
            ""
        ))

        conn.commit()
        conn.close()

        st.success("Bed Added Successfully")


# =====================================
# VIEW BEDS
# =====================================

def view_beds():

    st.subheader("🛏 Bed Inventory")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM beds",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Beds Available")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================
# ALLOCATE BED
# =====================================

def allocate_bed():

    st.subheader("🏥 Allocate Bed")

    bed_id = st.number_input(
        "Bed ID",
        min_value=1,
        step=1
    )

    patient_name = st.text_input(
        "Patient Name"
    )

    if st.button("Allocate Bed"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE beds
        SET status=?,
            patient_name=?
        WHERE bed_id=?
        """,
        (
            "Occupied",
            patient_name,
            bed_id
        ))

        conn.commit()
        conn.close()

        st.success("Bed Allocated Successfully")


# =====================================
# RELEASE BED
# =====================================

def release_bed():

    st.subheader("✅ Release Bed")

    bed_id = st.number_input(
        "Bed ID",
        min_value=1,
        step=1,
        key="release"
    )

    if st.button("Release Bed"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE beds
        SET status=?,
            patient_name=''
        WHERE bed_id=?
        """,
        (
            "Available",
            bed_id
        ))

        conn.commit()
        conn.close()

        st.success("Bed Released Successfully")


# =====================================
# EMERGENCY RESERVATION
# =====================================

def emergency_reservation():

    st.subheader("🚨 Emergency Reservation")

    bed_id = st.number_input(
        "Emergency Bed ID",
        min_value=1,
        step=1,
        key="emergency"
    )

    if st.button("Reserve Emergency Bed"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE beds
        SET status=?
        WHERE bed_id=?
        """,
        (
            "Reserved",
            bed_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Emergency Bed Reserved"
        )


# =====================================
# BED ANALYTICS
# =====================================

def bed_analytics():

    st.subheader("📊 Bed Analytics")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM beds",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Data Found")
        return

    total_beds = len(df)

    occupied = len(
        df[df["status"] == "Occupied"]
    )

    available = len(
        df[df["status"] == "Available"]
    )

    reserved = len(
        df[df["status"] == "Reserved"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Beds",
        total_beds
    )

    col2.metric(
        "Occupied",
        occupied
    )

    col3.metric(
        "Available",
        available
    )

    col4.metric(
        "Reserved",
        reserved
    )

    st.subheader("Bed Status Distribution")

    chart_data = pd.DataFrame({
        "Status": [
            "Occupied",
            "Available",
            "Reserved"
        ],
        "Count": [
            occupied,
            available,
            reserved
        ]
    })

    st.bar_chart(
        chart_data.set_index("Status")
    )


# =====================================
# SEARCH BED
# =====================================

def search_bed():

    st.subheader("🔍 Search Bed")

    bed_id = st.number_input(
        "Enter Bed ID",
        min_value=1,
        step=1,
        key="search_bed"
    )

    if st.button("Search"):

        conn = get_connection()

        df = pd.read_sql_query(
            """
            SELECT *
            FROM beds
            WHERE bed_id=?
            """,
            conn,
            params=(bed_id,)
        )

        conn.close()

        if df.empty:
            st.error("Bed Not Found")
        else:
            st.dataframe(df)


# =====================================
# MAIN FUNCTION
# =====================================

def bed_management():

    create_bed_table()

    st.title("🛏 Bed Management System")

    menu = st.sidebar.selectbox(
        "Bed Menu",
        [
            "Add Bed",
            "View Beds",
            "Allocate Bed",
            "Release Bed",
            "Emergency Reservation",
            "Search Bed",
            "Bed Analytics"
        ]
    )

    if menu == "Add Bed":
        add_bed()

    elif menu == "View Beds":
        view_beds()

    elif menu == "Allocate Bed":
        allocate_bed()

    elif menu == "Release Bed":
        release_bed()

    elif menu == "Emergency Reservation":
        emergency_reservation()

    elif menu == "Search Bed":
        search_bed()

    elif menu == "Bed Analytics":
        bed_analytics()