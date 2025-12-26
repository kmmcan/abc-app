import streamlit as st
import sqlite3
from datetime import datetime
import os

# ----------------------------
# Veritabanı yolu
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

# ----------------------------
# Veritabanı bağlantısı
# ----------------------------
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ----------------------------
# Tablo oluştur
# ----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS girisler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    secim TEXT,
    deger REAL,
    zaman TEXT
)
""")
conn.commit()

# ----------------------------
# UI
# ----------------------------
st.title("A / B / C Sayı Girişi")

col1, col2 = st.columns(2)

with col1:
    secim = st.radio("Seçim", ["A", "B", "C"])

with col2:
    deger = st.number_input("Sayı gir", step=1.0)

# ----------------------------
# Kayıt
# ----------------------------
if st.button("Kaydet"):
    cursor.execute(
        "INSERT INTO girisler (secim, deger, zaman) VALUES (?, ?, ?)",
        (secim, deger, datetime.now().isoformat())
    )
    conn.commit()
    st.success("Kaydedildi ✅")
