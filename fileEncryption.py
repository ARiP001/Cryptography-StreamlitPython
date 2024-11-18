from Crypto.Cipher import AES

# Fungsi untuk padding data agar sesuai dengan blok AES
def pad(data):
    return data + b"\0" * (16 - len(data) % 16)

# Fungsi untuk unpadding data setelah dekripsi
def unpad(data):
    return data.rstrip(b"\0")

# Fungsi untuk mengenkripsi file menggunakan AES
def encrypt_file(file_data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(pad(file_data))
    return nonce, ciphertext, tag

# Fungsi untuk mendekripsi file menggunakan AES
def decrypt_file(nonce, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return unpad(decrypted_data)
