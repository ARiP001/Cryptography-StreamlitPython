import psycopg2
import bcrypt
import streamlit as st

# Access secrets
db_host = st.secrets["general"]["DB_HOST"]
db_port = st.secrets["general"]["DB_PORT"]
db_name = st.secrets["general"]["DB_NAME"]
db_user = st.secrets["general"]["DB_USER"]
db_password = st.secrets["general"]["DB_PASSWORD"]

# Establish a connection
try:
    # Connect to the Supabase PostgreSQL database
    connection = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    cursor = connection.cursor()
    cursor.execute("SELECT 'Connection successful!'")
    result = cursor.fetchone()
    st.success(result[0])  # Display success message in Streamlit
    cursor.close()
    connection.close()
except Exception as e:
    st.error(f"Database connection failed: {e}")

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
