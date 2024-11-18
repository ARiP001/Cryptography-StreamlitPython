from PIL import Image
from stegano import lsb
import streamlit as st

def steganography_app():
    st.header("Enkripsi Gambar")
    menu = st.selectbox("Pilih Fitur", ["Enkripsi", "Dekripsi"])

    if menu == "Enkripsi":
        # File uploader for the image
        uploaded_image = st.file_uploader("Unggah Gambar (PNG, JPG, JPEG, WEBP):", type=["png", "jpg", "jpeg", "webp"])
        secret_message = st.text_area("Masukkan Pesan Rahasia:")
        
        if uploaded_image and secret_message:
            try:
                # Open the uploaded file as an image
                img = Image.open(uploaded_image).convert("RGB")  # Convert to RGB for compatibility
                
                # Perform steganography to hide the message
                encoded_image = lsb.hide(img, secret_message)
                
                # Save the encoded image to a file
                encoded_image_path = "encoded_image.png"
                encoded_image.save(encoded_image_path, format="PNG")
                
                # Display the encoded image
                st.image(encoded_image, caption="Gambar dengan Pesan Tersembunyi")

                # Provide a download button for the encoded image
                with open(encoded_image_path, "rb") as file:
                    st.download_button("Unduh Gambar Terenkripsi", file.read(), "encrypted_image.png")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat enkripsi: {e}")

    elif menu == "Dekripsi":
        # File uploader for the encrypted image
        uploaded_image = st.file_uploader("Unggah Gambar dengan Pesan Tersembunyi (PNG, JPG, JPEG, WEBP):", type=["png", "jpg", "jpeg", "webp"])
        if uploaded_image:
            try:
                # Open the uploaded file as an image
                img = Image.open(uploaded_image)
                
                # Extract the hidden message
                decoded_message = lsb.reveal(img)
                
                if decoded_message:
                    st.success(f"Pesan Rahasia: {decoded_message}")
                else:
                    st.warning("Tidak ada pesan rahasia yang ditemukan.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat dekripsi: {e}")
# import streamlit as st
# from PIL import Image
# from stegano import lsb
# from io import BytesIO
# import os

# def steganography_app():
#     st.title("Steganography - Enkripsi & Dekripsi Gambar")
#     menu = st.selectbox("Pilih Fitur", ["Enkripsi Pesan", "Dekripsi Pesan"])

#     if menu == "Enkripsi Pesan":
#         uploaded_image = st.file_uploader("Unggah Gambar (PNG, JPG, JPEG, WEBP):", type=["png", "jpg", "jpeg", "webp"])
#         secret_message = st.text_area("Masukkan Pesan Rahasia:")

#         if uploaded_image and secret_message:
#             try:
#                 # Read the image using BytesIO from the uploaded file
#                 img = Image.open(BytesIO(uploaded_image.getvalue())).convert('RGB')

#                 # Temporarily save the image to work around library limitations
#                 temp_image_path = "temp_image.png"
#                 img.save(temp_image_path)

#                 # Encrypt the message into the image using LSB
#                 encoded_image = lsb.hide(temp_image_path, secret_message)
                
#                 # Save the encoded image to a file for downloading
#                 encoded_image_path = "encoded_image.png"
#                 encoded_image.save(encoded_image_path)
                
#                 # Display the encoded image in Streamlit
#                 st.image(encoded_image, caption="Gambar dengan Pesan Tersembunyi")

#                 # Provide a download button for the encoded image
#                 with open(encoded_image_path, "rb") as file:
#                     st.download_button("Unduh Gambar Terenkripsi", file.read(), "encrypted_image.png")

#                 # Clean up temporary files
#                 if os.path.exists(temp_image_path):
#                     os.remove(temp_image_path)

#             except Exception as e:
#                 st.error(f"Terjadi kesalahan saat enkripsi: {e}")

#     elif menu == "Dekripsi Pesan":
#         uploaded_image = st.file_uploader("Unggah Gambar dengan Pesan Tersembunyi (PNG, JPG, JPEG, WEBP):", type=["png", "jpg", "jpeg", "webp"])

#         if uploaded_image:
#             try:
#                 # Read the image using BytesIO from the uploaded file
#                 img = Image.open(BytesIO(uploaded_image.getvalue()))

#                 # Temporarily save the image to ensure compatibility with the library
#                 temp_image_path = "temp_decoded_image.png"
#                 img.save(temp_image_path)

#                 # Extract the hidden message using LSB
#                 decoded_message = lsb.reveal(temp_image_path)
                
#                 if decoded_message:
#                     st.success(f"Pesan Rahasia: {decoded_message}")
#                 else:
#                     st.warning("Tidak ada pesan rahasia yang ditemukan.")

#                 # Clean up temporary files
#                 if os.path.exists(temp_image_path):
#                     os.remove(temp_image_path)

#             except Exception as e:
#                 st.error(f"Terjadi kesalahan saat dekripsi: {e}")
