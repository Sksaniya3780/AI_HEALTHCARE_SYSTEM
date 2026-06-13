import streamlit as st
import sqlite3
import bcrypt

from config.settings import DATABASE_PATH


def login_page():

    st.subheader("🔐 Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    email,
                    password,
                    role
                FROM users
                WHERE email = ?
                """,
                (email,)
            )

            user = cursor.fetchone()

            conn.close()

            if user:

                stored_password = user[3]

                if bcrypt.checkpw(
                    password.encode(),
                    stored_password.encode()
                ):

                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user[0]
                    st.session_state["user_name"] = user[1]
                    st.session_state["role"] = user[4]

                    st.success(
                        f"Welcome {user[1]}"
                    )

                    st.rerun()

                else:
                    st.error("Invalid Password")

            else:
                st.error("User Not Found")

        except Exception as e:
            st.error(f"Login Error: {e}")