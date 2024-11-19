import os
import streamlit as st
from auth import login_page, registration_page
from encryption import caesar_encrypt, caesar_decrypt, rsa_encrypt, rsa_decrypt, super_encrypt, super_decrypt, generate_rsa_keys
from steganography import encrypt_image, decrypt_image  # Now we use the split functions
from fileEncryption import encrypt_file, decrypt_file  

# Decryption Menu using radio
def decryption_menu():
    st.header("Story")
    st.text("Fufufafa adalah seorang mahasiswa Informatika yang baik, rajin, suka menolong, dan tidak sombong. Namun, selain menjadi mahasiswa yang baik, rajin, suka menolong, dan tidak sombong, Fufufafa memiliki sebuah hobi yang cukup unik yaitu berenang, berenang di dunia virtual. Suatu hari ketika sedang menyelami dunia virtual, ia menemukan sebuah arsip yang terkunci. Awalnya dia bingung kenapa arsip tersebut tidak bisa diakses, tapi karena dia telah belajar mata kuliah kriptogafi oleh dosen Bagus, dia langsung tahu bahwa arsip tersebut sebenarnya terenkripsi dan cara agar bisa membuka filenya yaitu dengan menggunakan alat kriptografi. Dengan cekatan fufufafa mengambil alat yang dibutuhkan dari kantong ajaibnya. YUK kawan-kawan bantu fufufafa memecahkan arsip tersebut supaya bisa dibuka")
    st.markdown("[akses arsip di sini](https://drive.google.com/drive/folders/1U9oEdCKqGX-gYcX0S1awwWacz8aSVt8F?usp=sharing)", unsafe_allow_html=True)

    st.text("Pada Arsip tersebut ternyata terdapat tulisan (unlock: dua bulan terakhir gabung tanpa spasi)")
    st.text("Note : hanya gunakan menu dekripsi clue untuk menyelesaikan quest ini")


    st.header("Menu Dekripsi")
    menu = st.radio("Pilih Menu Dekripsi", ["Dekripsi Teks", "Dekripsi Gambar", "Dekripsi File"])

    if menu == "Dekripsi Teks":
        text_decryption_menu()
    elif menu == "Dekripsi Gambar":
        decrypt_image()  # Calling the decryption function for image
    elif menu == "Dekripsi File":
        file_decryption_menu()  # Now this function is defined

# Encryption Menu using radio
def encryption_menu():
    st.header("Menu Enkripsi")
    menu = st.radio("Pilih Menu Enkripsi", ["Enkripsi Teks", "Enkripsi Gambar", "Enkripsi File"])

    if menu == "Enkripsi Teks":
        text_encryption_menu()
    elif menu == "Enkripsi Gambar":
        encrypt_image()  # Calling the encryption function for image
    elif menu == "Enkripsi File":
        file_encryption_menu()  # Only encryption for files, no mode switch

# Decryption Menu for Text
def text_decryption_menu():
    st.subheader("Dekripsi teks")
    sub_menu = st.radio("Pilih Metode Dekripsi", ["Caesar Cipher", "RSA", "Super Dekripsi"])

    if sub_menu == "Caesar Cipher":
        st.header("Caesar Cipher")
        encrypted_text = st.text_input("Masukkan Teks Terenkripsi")
        key = st.number_input("Masukkan Key (1-25)", min_value=1, max_value=25, step=1)
        
        if st.button("Proses"):
            if encrypted_text:
                result = caesar_decrypt(encrypted_text, key)
                st.write(f"Hasil Dekripsi: {result}")
            else:
                st.warning("Masukkan teks untuk diproses.")

    elif sub_menu == "RSA":
        st.header("RSA")
        encrypted_text = st.text_input("Masukkan Teks Terenkripsi")
        private_key_input = st.text_area("Masukkan Private Key (PEM format)")

        if st.button("Dekripsi"):
            if encrypted_text and private_key_input:
                try:
                    result = rsa_decrypt(encrypted_text, private_key_input)
                    st.success(f"Hasil Dekripsi: {result}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat dekripsi: {e}")
            else:
                st.warning("Masukkan teks terenkripsi dan private key untuk melanjutkan.")

    elif sub_menu == "Super Dekripsi":
        st.header("Super Dekripsi")
        caesar_key = st.number_input("Masukkan Key Caesar (1-25)", min_value=1, max_value=25, step=1)
        private_key_input = st.text_area("Masukkan Private Key (PEM format)")
        
        encrypted_text = st.text_input("Masukkan Teks Terenkripsi")
        
        if st.button("Dekripsi"):
            if encrypted_text and private_key_input:
                try:
                    result = super_decrypt(encrypted_text, caesar_key, private_key_input)
                    st.success(f"Hasil Super Dekripsi: {result}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat dekripsi: {e}")
            else:
                st.warning("Masukkan teks terenkripsi dan private key untuk melanjutkan.")

# Encryption Menu for Text
def text_encryption_menu():
    st.header("Enkripsi Teks")
    sub_menu = st.radio("Pilih Metode Enkripsi", ["Caesar Cipher", "RSA", "Super Enkripsi"])

    if sub_menu == "Caesar Cipher":
        st.header("Caesar Cipher")
        text = st.text_input("Masukkan Teks")
        key = st.number_input("Masukkan Key (1-25)", min_value=1, max_value=25, step=1)
        
        if st.button("Proses"):
            if text:
                result = caesar_encrypt(text, key)
                st.write(f"Hasil Enkripsi: {result}")
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

        text = st.text_input("Masukkan Teks untuk Enkripsi")
        
        if st.button("Enkripsi"):
            if text:
                result = rsa_encrypt(text, st.session_state["public_key"])
                st.success(f"Hasil Enkripsi: {result}")
            else:
                st.warning("Masukkan teks untuk dienkripsi!")

    elif sub_menu == "Super Enkripsi":
        st.header("Super Enkripsi")
        caesar_key = st.number_input("Masukkan Key Caesar (1-25)", min_value=1, max_value=25, step=1)
        
        if "public_key" not in st.session_state or "private_key" not in st.session_state:
            public_key, private_key = generate_rsa_keys()
            st.session_state["public_key"] = public_key
            st.session_state["private_key"] = private_key

        st.write("Kunci Publik:")
        st.code(st.session_state["public_key"])
        st.write("Kunci Privat:")
        st.code(st.session_state["private_key"])

        text = st.text_input("Masukkan Teks untuk Enkripsi")
        
        if st.button("Enkripsi"):
            if text:
                result = super_encrypt(text, caesar_key, st.session_state["public_key"])
                st.success(f"Hasil Super Enkripsi: {result}")
            else:
                st.warning("Masukkan teks untuk dienkripsi!")

# File Encryption Menu (Now only for encryption, no radio)

def file_encryption_menu():
    st.header("Enkripsi File dengan AES")

    key = st.text_input("Masukkan Key AES (16, 24, atau 32 karakter)", type="password", key="aes_key_input")

    # Add a button to generate a random key
    if st.button("Buat Key Acak"):
        random_key = os.urandom(16).hex()  # Generate a 16-byte key and display it in hexadecimal format
        st.session_state["random_key"] = random_key
        st.success(f"Key Acak: {random_key}")
        st.warning("Pastikan Anda menyimpan key ini untuk keperluan dekripsi!")

    # Use the generated random key if present
    if "random_key" in st.session_state:
        key = st.session_state["random_key"]

    if len(key) not in [16, 24, 32]:
        st.warning("Key AES harus memiliki panjang 16, 24, atau 32 karakter.")

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


# File Decryption Menu
def file_decryption_menu():
    st.header("Dekripsi File dengan AES")

    key = st.text_input("Masukkan Key AES (16, 24, atau 32 karakter)", type="password", key="aes_key_input")

    if len(key) not in [16, 24, 32]:
        st.warning("Key AES harus memiliki panjang 16, 24, atau 32 karakter.")

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

# Main flow
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    # Sidebar navigation for the game menus
    st.markdown("<h1 style='text-align: center;'>KRIPTOGAMEFI 🎮</h1>", unsafe_allow_html=True)

    menu_choice = st.sidebar.selectbox("Pilih Menu", ["Mainkan Game (dekripsi)", "Buat Clue (enkripsi)"])

    if menu_choice == "Mainkan Game (dekripsi)":
        decryption_menu()
    elif menu_choice == "Buat Clue (enkripsi)":
        encryption_menu()

    
    # Add space before the logout button using <br> tags
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False  # Logout the user
        st.success("You have logged out successfully!")

else:
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "register":
        registration_page()
