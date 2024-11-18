import os
import streamlit as st
import uuid
from auth import login_page, registration_page
from encryption import caesar_encrypt, caesar_decrypt, rsa_encrypt, rsa_decrypt, super_encrypt, super_decrypt, generate_rsa_keys
from steganography import steganography_app
from fileEncryption import encrypt_file, decrypt_file

def main_menu():
    st.title("Aplikasi Enkripsi")
    menu = st.selectbox("Pilih Menu Utama", ["Enkripsi Teks", "Enkripsi Gambar", "Enkripsi File"])

    if menu == "Enkripsi Teks":
        text_encryption_menu()
    elif menu == "Enkripsi Gambar":
        steganography_app()
    elif menu == "Enkripsi File":
        file_encryption_menu()

def text_encryption_menu():
    st.title("Enkripsi Teks")
    sub_menu = st.selectbox("Pilih Metode Enkripsi", ["Caesar Cipher", "RSA", "Super Enkripsi"])

    if sub_menu == "Caesar Cipher":
        st.header("Caesar Cipher")
        text = st.text_input("Masukkan Teks")
        key = st.number_input("Masukkan Key (1-25)", min_value=1, max_value=25, step=1)
        mode = st.radio("Mode", ["Encrypt", "Decrypt"], key="caesar_mode")

        if st.button("Proses", key="caesar_proses"):
            if text:
                if mode == "Encrypt":
                    result = caesar_encrypt(text, key)
                else:
                    result = caesar_decrypt(text, key)
                st.write(f"Hasil: {result}")
            else:
                st.warning("Masukkan teks untuk diproses.")

    elif sub_menu == "RSA":
        st.header("RSA")
        if "public_key" not in st.session_state or "private_key" not in st.session_state:
            public_key, private_key = generate_rsa_keys()
            st.session_state["public_key"] = public_key
            st.session_state["private_key"] = private_key

        st.write("Kunci Publik:")
        st.code(st.session_state["public_key"])
        st.write("Kunci Privat:")
        st.code(st.session_state["private_key"])

        mode = st.radio("Mode", ["Encrypt", "Decrypt"], key="rsa_mode")
        if mode == "Encrypt":
            text = st.text_input("Masukkan Teks untuk Enkripsi")
            if st.button("Enkripsi", key="rsa_encrypt"):
                if text:
                    result = rsa_encrypt(text, st.session_state["public_key"])
                    st.success(f"Hasil Enkripsi: {result}")
                else:
                    st.warning("Masukkan teks untuk dienkripsi!")

        elif mode == "Decrypt":
            encrypted_text = st.text_input("Masukkan Teks Terenkripsi")
            private_key_input = st.text_area("Masukkan Private Key (PEM format)")

            if st.button("Dekripsi", key="rsa_decrypt"):
                if encrypted_text and private_key_input:
                    try:
                        result = rsa_decrypt(encrypted_text, private_key_input)
                        st.success(f"Hasil Dekripsi: {result}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat dekripsi: {e}")
                else:
                    st.warning("Masukkan teks terenkripsi dan private key untuk melanjutkan.")

    elif sub_menu == "Super Enkripsi":
        st.header("Super Enkripsi")
        caesar_key = st.number_input("Masukkan Key Caesar (1-25)", min_value=1, max_value=25, step=1)
        if "public_key" not in st.session_state or "private_key" not in st.session_state:
            public_key, private_key = generate_rsa_keys()
            st.session_state["public_key"] = public_key
            st.session_state["private_key"] = private_key

        st.write("Kunci Publik:")
        st.code(st.session_state["public_key"], language="plaintext")
        st.write("Kunci Privat:")
        st.code(st.session_state["private_key"], language="plaintext")

        mode = st.radio("Mode", ["Encrypt", "Decrypt"], key="super_mode")
        if mode == "Encrypt":
            text = st.text_input("Masukkan Teks untuk Enkripsi")
            if st.button("Enkripsi", key="super_encrypt"):
                if text:
                    result = super_encrypt(text, caesar_key, st.session_state["public_key"])
                    st.success(f"Hasil Super Enkripsi: {result}")
                else:
                    st.warning("Masukkan teks untuk dienkripsi!")

        elif mode == "Decrypt":
            encrypted_text = st.text_input("Masukkan Teks Terenkripsi")
            private_key_input = st.text_area("Masukkan Private Key (PEM format)")

            if st.button("Dekripsi", key="super_decrypt"):
                if encrypted_text and private_key_input:
                    try:
                        result = super_decrypt(encrypted_text, caesar_key, private_key_input)
                        st.success(f"Hasil Super Dekripsi: {result}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat dekripsi: {e}")
                else:
                    st.warning("Masukkan teks terenkripsi dan private key untuk melanjutkan.")

def file_encryption_menu():
    st.header("Enkripsi File dengan AES")
    
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    # Key input section
    key = st.text_input("Masukkan Key AES (16, 24, atau 32 karakter)", type="password", key="aes_key_input")
    generate_key_button = st.button("Buat Key Acak", key="generate_aes_key")

    if generate_key_button:
        random_key = os.urandom(16).hex()  # 32 bytes key in hexadecimal format
        st.session_state["aes_key"] = random_key
        st.success(f"Key Acak Telah Dibuat: {random_key}")
        st.warning("Pastikan Anda menyimpan key ini untuk keperluan dekripsi!")

    if "aes_key" in st.session_state:
        key = st.session_state["aes_key"]

    # Validasi panjang key
    if len(key) not in [16, 24, 32]:
        st.warning("Key AES harus memiliki panjang 16, 24, atau 32 karakter.")

    if mode == "Enkripsi":
        uploaded_file = st.file_uploader("Unggah File untuk Dienkripsi", type=None)
        if uploaded_file and st.button("Enkripsi File"):
            file_data = uploaded_file.read()
            try:
                nonce, ciphertext, tag = encrypt_file(file_data, key.encode())
                encrypted_file = nonce + ciphertext + tag

                st.success("File berhasil dienkripsi!")
                st.download_button(
                    label="Unduh File Terenkripsi",
                    data=encrypted_file,
                    file_name=f"{uploaded_file.name}.enc",
                    mime="application/octet-stream"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

    elif mode == "Dekripsi":
        uploaded_file = st.file_uploader("Unggah File Terenkripsi", type=None)
        if uploaded_file and st.button("Dekripsi File"):
            file_data = uploaded_file.read()
            try:
                nonce = file_data[:16]
                ciphertext = file_data[16:-16]
                tag = file_data[-16:]

                decrypted_data = decrypt_file(nonce, ciphertext, tag, key.encode())

                st.success("File berhasil didekripsi!")
                st.download_button(
                    label="Unduh File Didekripsi",
                    data=decrypted_data,
                    file_name=f"decrypted_{uploaded_file.name.replace('.enc', '')}",
                    mime="application/octet-stream"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_menu()
    if st.button("Logout"):
        st.session_state["logged_in"] = False
else:
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "register":
        registration_page()
