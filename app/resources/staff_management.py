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
# CREATE STAFF TABLE
# =====================================

def create_staff_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff(
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        department TEXT,
        shift TEXT,
        phone TEXT,
        attendance TEXT,
        leave_status TEXT
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# ADD STAFF
# =====================================

def add_staff():

    st.subheader("➕ Add Staff Member")

    with st.form("staff_form"):

        name = st.text_input("Staff Name")

        role = st.selectbox(
            "Role",
            [
                "Doctor",
                "Nurse",
                "Receptionist",
                "Lab Technician",
                "Pharmacist",
                "Admin"
            ]
        )

        department = st.text_input("Department")

        shift = st.selectbox(
            "Shift",
            [
                "Morning",
                "Afternoon",
                "Night"
            ]
        )

        phone = st.text_input("Phone Number")

        submit = st.form_submit_button(
            "Add Staff"
        )

        if submit:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO staff
            (
                name,
                role,
                department,
                shift,
                phone,
                attendance,
                leave_status
            )
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                name,
                role,
                department,
                shift,
                phone,
                "Present",
                "No Leave"
            ))

            conn.commit()
            conn.close()

            st.success(
                "Staff Added Successfully"
            )


# =====================================
# VIEW STAFF
# =====================================

def view_staff():

    st.subheader("👨‍⚕️ Staff Records")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM staff",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Staff Found")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================
# SEARCH STAFF
# =====================================

def search_staff():

    st.subheader("🔍 Search Staff")

    name = st.text_input(
        "Enter Staff Name"
    )

    if st.button("Search"):

        conn = get_connection()

        df = pd.read_sql_query(
            """
            SELECT *
            FROM staff
            WHERE name LIKE ?
            """,
            conn,
            params=(f"%{name}%",)
        )

        conn.close()

        if df.empty:
            st.error("Staff Not Found")
        else:
            st.dataframe(df)
            

# =====================================
# UPDATE SHIFT
# =====================================

def update_shift():

    st.subheader("🔄 Update Shift")

    staff_id = st.number_input(
        "Staff ID",
        min_value=1,
        step=1
    )

    shift = st.selectbox(
        "New Shift",
        [
            "Morning",
            "Afternoon",
            "Night"
        ]
    )

    if st.button("Update Shift"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE staff
        SET shift=?
        WHERE staff_id=?
        """,
        (
            shift,
            staff_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Shift Updated Successfully"
        )


# =====================================
# ATTENDANCE
# =====================================

def attendance_management():

    st.subheader("📅 Attendance")

    staff_id = st.number_input(
        "Staff ID",
        min_value=1,
        step=1,
        key="attendance"
    )

    attendance = st.selectbox(
        "Attendance Status",
        [
            "Present",
            "Absent"
        ]
    )

    if st.button("Update Attendance"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE staff
        SET attendance=?
        WHERE staff_id=?
        """,
        (
            attendance,
            staff_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Attendance Updated"
        )


# =====================================
# LEAVE MANAGEMENT
# =====================================

def leave_management():

    st.subheader("🏖 Leave Management")

    staff_id = st.number_input(
        "Staff ID",
        min_value=1,
        step=1,
        key="leave"
    )

    leave_status = st.selectbox(
        "Leave Status",
        [
            "No Leave",
            "Pending",
            "Approved"
        ]
    )

    if st.button("Update Leave"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE staff
        SET leave_status=?
        WHERE staff_id=?
        """,
        (
            leave_status,
            staff_id
        ))

        conn.commit()
        conn.close()

        st.success(
            "Leave Status Updated"
        )


# =====================================
# DELETE STAFF
# =====================================

def delete_staff():

    st.subheader("❌ Delete Staff")

    staff_id = st.number_input(
        "Staff ID",
        min_value=1,
        step=1,
        key="delete_staff"
    )

    if st.button("Delete Staff"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM staff
        WHERE staff_id=?
        """,
        (staff_id,)
        )

        conn.commit()
        conn.close()

        st.success(
            "Staff Deleted Successfully"
        )


# =====================================
# ANALYTICS
# =====================================

def staff_analytics():

    st.subheader("📊 Staff Analytics")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM staff",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Data Available")
        return

    total_staff = len(df)

    doctors = len(
        df[df["role"] == "Doctor"]
    )

    nurses = len(
        df[df["role"] == "Nurse"]
    )

    present = len(
        df[df["attendance"] == "Present"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Staff",
        total_staff
    )

    col2.metric(
        "Doctors",
        doctors
    )

    col3.metric(
        "Nurses",
        nurses
    )

    col4.metric(
        "Present",
        present
    )

    st.subheader(
        "Role Distribution"
    )

    st.bar_chart(
        df["role"].value_counts()
    )


# =====================================
# MAIN FUNCTION
# =====================================

def staff_management():

    create_staff_table()

    st.title(
        "👨‍⚕️ Staff Management System"
    )

    menu = st.sidebar.selectbox(
        "Staff Menu",
        [
            "Add Staff",
            "View Staff",
            "Search Staff",
            "Update Shift",
            "Attendance",
            "Leave Management",
            "Delete Staff",
            "Staff Analytics"
        ]
    )

    if menu == "Add Staff":
        add_staff()

    elif menu == "View Staff":
        view_staff()

    elif menu == "Search Staff":
        search_staff()

    elif menu == "Update Shift":
        update_shift()

    elif menu == "Attendance":
        attendance_management()

    elif menu == "Leave Management":
        leave_management()

    elif menu == "Delete Staff":
        delete_staff()

    elif menu == "Staff Analytics":
        staff_analytics()