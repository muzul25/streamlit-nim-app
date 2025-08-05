import streamlit as st
import pandas as pd
import hashlib
import os

DB_FILE = "database.csv"
LOGO_PATH = "logo.png"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def load_database():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE, dtype=str)
    else:
        return pd.DataFrame(columns=["email", "Nama", "Username", "Password"])

def save_database(df):
    df.to_csv(DB_FILE, index=False)

def admin_login():
    st.subheader("Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            st.session_state["admin_logged_in"] = True
            st.success("Login berhasil.")
        else:
            st.error("Username atau password salah.")

def admin_dashboard():
    st.subheader("Admin - Upload/Update Database")
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, dtype=str)
        if set(["email", "Nama", "Username", "Password"]).issubset(df.columns):
            save_database(df)
            st.success("Database berhasil diupdate dan disimpan.")
        else:
            st.error("Kolom harus mencakup: email, Nama, Username, Password")

    st.subheader("Database Saat Ini")
    st.dataframe(load_database())

def peserta_dashboard():
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=300)
    st.subheader("Cek Informasi Peserta")
    email = st.text_input("Masukkan Email Anda")
    if st.button("Lihat Informasi") and email:
        df = load_database()
        result = df[df["email"] == email]
        if not result.empty:
            row = result.iloc[0]
            st.success("Data ditemukan:")
            st.text(f"Nama     : {row['Nama']}")
            st.text(f"Username : {row['Username']}")
            st.text(f"Password : {row['Password']}")
        else:
            st.error("email tidak ditemukan dalam database.")

st.set_page_config(page_title="Dashboard Peserta", page_icon=":bar_chart:", layout="centered")
st.title("Aplikasi Informasi Akun Peserta")

menu = st.sidebar.radio("Pilih Halaman", ["Peserta", "Admin"])

if menu == "Admin":
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if not st.session_state["admin_logged_in"]:
        admin_login()
    else:
        admin_dashboard()
else:
    peserta_dashboard()
