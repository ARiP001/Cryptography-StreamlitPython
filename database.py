import psycopg2
import bcrypt
import streamlit as st

# Access secrets
db_host = st.secrets["general"]["DB_HOST"]
db_port = st.secrets["general"]["DB_PORT"]
db_name = st.secrets["general"]["DB_NAME"]
db_user = st.secrets["general"]["DB_USER"]
db_password = st.secrets["general"]["DB_PASSWORD"]

def get_connection():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return True
    return False

def create_account(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result[0] > 0:
        conn.close()
        raise ValueError(f"Username '{username}' already exists. Please choose a different username.")

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Insert the new user
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    conn.close()
