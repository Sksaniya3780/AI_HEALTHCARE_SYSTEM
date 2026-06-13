import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

DATABASE = "healthcare.db"


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =====================================
# CREATE RESOURCE TABLE
# =====================================

def create_resource_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources(
        resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_name TEXT,
        category TEXT,
        quantity INTEGER,
        available INTEGER,
        allocated INTEGER
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# ADD RESOURCE
# =====================================

def add_resource():

    st.subheader("➕ Add Resource")

    resource_name = st.text_input(
        "Resource Name"
    )

    category = st.selectbox(
        "Category",
        [
            "Ventilator",
            "Oxygen Unit",
            "Medical Equipment",
            "Emergency Equipment",
            "ICU Equipment"
        ]
    )

    quantity = st.number_input(
        "Total Quantity",
        min_value=1,
        value=10
    )

    if st.button("Add Resource"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO resources
        (
            resource_name,
            category,
            quantity,
            available,
            allocated
        )
        VALUES (?,?,?,?,?)
        """,
        (
            resource_name,
            category,
            quantity,
            quantity,
            0
        ))

        conn.commit()
        conn.close()

        st.success(
            "Resource Added Successfully"
        )


# =====================================
# VIEW RESOURCES
# =====================================

def view_resources():

    st.subheader("📦 Hospital Resources")

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM resources",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Resources Found")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================
# ALLOCATE RESOURCE
# =====================================

def allocate_resource():

    st.subheader("🏥 Allocate Resource")

    resource_id = st.number_input(
        "Resource ID",
        min_value=1,
        step=1
    )

    qty = st.number_input(
        "Allocate Quantity",
        min_value=1,
        value=1
    )

    if st.button("Allocate"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT available, allocated
        FROM resources
        WHERE resource_id=?
        """,
        (resource_id,)
        )

        row = cursor.fetchone()

        if row:

            available = row[0]
            allocated = row[1]

            if qty <= available:

                cursor.execute("""
                UPDATE resources
                SET available=?,
                    allocated=?
                WHERE resource_id=?
                """,
                (
                    available - qty,
                    allocated + qty,
                    resource_id
                ))

                conn.commit()

                st.success(
                    "Resource Allocated"
                )

            else:

                st.error(
                    "Insufficient Quantity Available"
                )

        conn.close()


# =====================================
# RELEASE RESOURCE
# =====================================

def release_resource():

    st.subheader("🔄 Release Resource")

    resource_id = st.number_input(
        "Resource ID",
        min_value=1,
        step=1,
        key="release_resource"
    )

    qty = st.number_input(
        "Release Quantity",
        min_value=1,
        value=1,
        key="release_qty"
    )

    if st.button("Release"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT available, allocated
        FROM resources
        WHERE resource_id=?
        """,
        (resource_id,)
        )

        row = cursor.fetchone()

        if row:

            available = row[0]
            allocated = row[1]

            if qty <= allocated:

                cursor.execute("""
                UPDATE resources
                SET available=?,
                    allocated=?
                WHERE resource_id=?
                """,
                (
                    available + qty,
                    allocated - qty,
                    resource_id
                ))

                conn.commit()

                st.success(
                    "Resource Released"
                )

            else:

                st.error(
                    "Release Quantity Exceeds Allocation"
                )

        conn.close()


# =====================================
# SEARCH RESOURCE
# =====================================

def search_resource():

    st.subheader("🔍 Search Resource")

    resource_name = st.text_input(
        "Resource Name"
    )

    if st.button("Search Resource"):

        conn = get_connection()

        df = pd.read_sql_query(
            """
            SELECT *
            FROM resources
            WHERE resource_name LIKE ?
            """,
            conn,
            params=(f"%{resource_name}%",)
        )

        conn.close()

        if df.empty:
            st.error("Resource Not Found")
        else:
            st.dataframe(df)


# =====================================
# FORECAST DEMAND
# =====================================

def demand_forecasting():

    st.subheader("🤖 AI Demand Forecasting")

    current_patients = st.number_input(
        "Current Patients",
        min_value=1,
        value=100
    )

    growth_rate = st.slider(
        "Expected Patient Growth (%)",
        0,
        100,
        20
    )

    predicted_patients = int(
        current_patients *
        (1 + growth_rate / 100)
    )

    predicted_oxygen = predicted_patients // 5
    predicted_ventilators = predicted_patients // 10

    st.success(
        f"Predicted Patients: {predicted_patients}"
    )

    st.info(
        f"Estimated Oxygen Units Needed: "
        f"{predicted_oxygen}"
    )

    st.info(
        f"Estimated Ventilators Needed: "
        f"{predicted_ventilators}"
    )


# =====================================
# RESOURCE RECOMMENDATION
# =====================================

def resource_recommendation():

    st.subheader(
        "💡 Resource Recommendations"
    )

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM resources",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Resource Data")
        return

    low_resources = df[
        df["available"] < 5
    ]

    if len(low_resources) == 0:

        st.success(
            "All Resources Adequately Stocked"
        )

    else:

        st.error(
            "Low Resource Alert"
        )

        st.dataframe(
            low_resources[
                [
                    "resource_name",
                    "available"
                ]
            ]
        )


# =====================================
# ANALYTICS
# =====================================

def resource_analytics():

    st.subheader(
        "📊 Resource Analytics"
    )

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM resources",
        conn
    )

    conn.close()

    if df.empty:
        st.warning("No Data Available")
        return

    st.metric(
        "Total Resources",
        len(df)
    )

    st.metric(
        "Total Available",
        int(df["available"].sum())
    )

    st.metric(
        "Total Allocated",
        int(df["allocated"].sum())
    )

    category_data = (
        df.groupby("category")["quantity"]
        .sum()
    )

    st.bar_chart(category_data)


# =====================================
# MAIN FUNCTION
# =====================================

def resource_allocation():

    create_resource_table()

    st.title(
        "📦 Resource Allocation System"
    )

    menu = st.sidebar.selectbox(
        "Resource Menu",
        [
            "Add Resource",
            "View Resources",
            "Allocate Resource",
            "Release Resource",
            "Search Resource",
            "Demand Forecasting",
            "Recommendations",
            "Resource Analytics"
        ]
    )

    if menu == "Add Resource":
        add_resource()

    elif menu == "View Resources":
        view_resources()

    elif menu == "Allocate Resource":
        allocate_resource()

    elif menu == "Release Resource":
        release_resource()

    elif menu == "Search Resource":
        search_resource()

    elif menu == "Demand Forecasting":
        demand_forecasting()

    elif menu == "Recommendations":
        resource_recommendation()

    elif menu == "Resource Analytics":
        resource_analytics()