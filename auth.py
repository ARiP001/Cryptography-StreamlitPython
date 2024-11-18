import streamlit as st
import re
from database import check_login, create_account

def login_page():
    st.title("Login")
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if username and password:
            if check_login(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Username atau password salah.")
        else:
            st.warning("Mohon masukkan username dan password.")

    if st.button("Belum punya akun? Daftar"):
        st.session_state["page"] = "register"

    
def registration_page():
    st.title("Create a New Account")
    with st.form(key="register_form"):
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")

    if submit_button:
        if username and password:
            if password != confirm_password:
                st.error("Password and confirmation password do not match.")
            elif len(password) < 8 or len(password) > 20:
                st.error("Password must be between 8-20 characters.")
            elif not re.search(r'\d', password):
                st.error("Password must contain at least one number.")
            elif not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                st.error("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
            else:
                success, message = create_account(username, password)
                if success:
                    st.success(message)
                    st.session_state["page"] = "login"
                else:
                    st.error(message)
        else:
            st.warning("Please complete all fields.")

    if st.button("Back to Login"):
        st.session_state["page"] = "login"
