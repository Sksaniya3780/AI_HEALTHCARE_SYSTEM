import streamlit as st
import sqlite3
import bcrypt

from config.settings import DATABASE_PATH


def register_page():

    st.subheader("📝 Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Role",
        ["Patient", "Doctor", "Admin"]
    )

    if st.button("Register"):

        if not name or not email or not password:
            st.warning("Please fill all fields")
            return

        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=?",
                (email,)
            )

            if cursor.fetchone():
                st.error("Email already registered")
                conn.close()
                return

            hashed_password = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            ).decode()

            cursor.execute(
                """
                INSERT INTO users
                (username, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    hashed_password,
                    role
                )
            )

            conn.commit()
            conn.close()

            st.success(
                "Registration Successful! Please Login."
            )

        except Exception as e:
            st.error(f"Registration Error: {e}")