from PIL import Image
from stegano import lsb
import streamlit as st

def steganography_app():
    st.header("Enkripsi Gambar")
    menu = st.selectbox("Pilih Fitur", ["Enkripsi", "Dekripsi"])

    if menu == "Enkripsi":
        uploaded_image = st.file_uploader("Unggah Gambar (PNG, JPG, JPEG, WEBP):", type=["png", "jpg", "jpeg", "webp"])
        secret_message = st.text_area("Masukkan Pesan Rahasia:")
        if uploaded_image and secret_message:
            try:
                img = Image.open(uploaded_image).convert("RGB")  # Convert to RGB to ensure compatibility
                encoded_image = lsb.hide(img, secret_message)
                encoded_image_path = "encoded_image.png"
                encoded_image.save(encoded_image_path, format="PNG")  # Save as PNG for compatibility
                st.image(encoded_image, caption="Gambar dengan Pesan Tersembunyi")
                with open(encoded_image_path, "rb") as file:
                    st.download_button("Unduh Gambar Terenkripsi", file.read(), "encrypted_image.png")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat enkripsi: {e}")

    elif menu == "Dekripsi":
        uploaded_image = st.file_uploader("Unggah Gambar dengan Pesan Tersembunyi (PNG, JPG, JPEG, WEBP):", type=["png", "jpg", "jpeg", "webp"])
        if uploaded_image:
            try:
                decoded_message = lsb.reveal(Image.open(uploaded_image))
                st.success(f"Pesan Rahasia: {decoded_message}")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat dekripsi: {e}")
