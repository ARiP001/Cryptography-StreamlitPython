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
    st.title("Daftar Akun Baru")
    with st.form(key="register_form"):
        username = st.text_input("Username Baru")
        password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Ulangi Password Baru", type="password")
        submit_button = st.form_submit_button("Daftar")

    if submit_button:
        if username and password:
            if password != confirm_password:
                st.error("Password dan konfirmasi password tidak sama.")
            elif len(password) < 8 or len(password) > 20:
                st.error("Password harus memiliki panjang 8-20 karakter.")
            elif not re.search(r'\d', password):
                st.error("Password harus mengandung setidaknya satu angka.")
            elif not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                st.error("Password harus mengandung setidaknya satu simbol unik (!@#$%^&*(),.?\":{}|<>).")
            else:
                create_account(username, password)
                st.success("Akun berhasil dibuat! Silakan login.")
                st.session_state["page"] = "login"
        else:
            st.warning("Mohon lengkapi semua kolom.")

    if st.button("Kembali ke Login"):
        st.session_state["page"] = "login"
