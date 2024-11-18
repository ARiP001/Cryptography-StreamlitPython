import mysql.connector
import bcrypt
import streamlit as st

# Access secrets
db_host = st.secrets["general"]["DB_HOST"]
db_port = st.secrets["general"]["DB_PORT"]
db_name = st.secrets["general"]["DB_NAME"]
db_user = st.secrets["general"]["DB_USER"]
db_password = st.secrets["general"]["DB_PASSWORD"]

# Establish a connection
connection = mysql.connector.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_name
)


def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return True
    return False

def create_account(username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    conn.close()
