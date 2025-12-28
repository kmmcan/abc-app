import streamlit as st
import sqlite3
from datetime import datetime
import os
import io

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

st.title("Hatim Sayımı")

col1, col2 = st.columns(2)

with col1:
    SECIMLER = [
    "Kur'an Hatmi", "70bin Tevhid Hatmi", "Delailül Hayrat Hatmi",
    "18bin Salatu Selam", "Salavat-ı Şerif", "Seyyid'ül İstiğfar",
    "Estağfirullah", "Salatu Tefriciye", "Salatu Tuncina",
    "Şifa Salatu Selamı", "Salatu Fatih", "Salli Barik",
    "Salavatı Kübra", "..ve sayısız Salavat Hizbi",
    "..ve sayısız Salatu Selam", "..ve sayısız Tevhid",
    "İhlas", "Fatiha", "Ayetel Kürsi", "Kevser", "Felak", "Nas",
    "Yasin", "Duhan", "Fetih", "Muhammed", "Rahman", "Vakıa",
    "Mülk", "Secde", "Nebe", "Kıyame", "Cuma", "Buruc",
    "Mutaffifin", "Kehf", "hasbiyallahu la ilahe",
    "hasbunallahu", "Hz Yunus asm duası",
    "Subhanallahi vebihamdihi subhanallahil azim",
    "subhanallahi vebihamdihi",
    "Subhanallahi velhamdülillahi..",
    "la havle vela kuvvete"]

    secim = st.radio("Seçim", SECIMLER)
    
with col2:
    deger = st.number_input("Sayı gir", step=1.0)
    kaydet = st.button("Kaydet")  #kaydet butonu sayının altında olsun diye
    mesaj_alani = st.empty()   # 👈 kaydedildi mesajı burada çıksın

# ----------------------------
# Kayıt
# ----------------------------
if kaydet:
    cursor.execute(
        "INSERT INTO girisler (secim, deger, zaman) VALUES (?, ?, ?)",
        (secim, deger, datetime.now().isoformat())
    )
    conn.commit()
    mesaj_alani.success("Kaydedildi")

# girilenleri görebilmek için
import pandas as pd
import io

st.subheader("Admin Paneli")

admin_key = st.text_input("Admin şifresi", type="password")

if admin_key == "281267":   # ← şifreyi değiştir

    st.success("Admin girişi başarılı")

    # ---------------------------
    # VERİLERİ ÇEK
    # ---------------------------
    cursor.execute("""
    SELECT secim, deger, zaman
    FROM girisler
    ORDER BY zaman DESC
    """)

    rows = cursor.fetchall()

    if rows:
        table_data = []

        for secim_db, deger, zaman in rows:
            row = {s: None for s in SECIMLER}  # tüm sütunları boş başlat
            row[secim_db] = deger              # seçileni doldur
            row["Zaman"] = zaman               # zaman ekle
            table_data.append(row)
            
        df = pd.DataFrame(table_data)

        # ---------------------------
        # TABLO
        # ---------------------------
        st.subheader("Kayıtlar")
        st.dataframe(df, use_container_width=True, height=400)

        # ---------------------------
        # TOPLAMLAR
        # ---------------------------
        st.subheader("Toplamlar")

        cursor.execute("""
        SELECT secim, SUM(deger)
        FROM girisler
        GROUP BY secim
        """)

        totals = cursor.fetchall()

        for secim, toplam in totals:
            st.write(f"**{secim}** toplamı: {toplam}")

        # ---------------------------
        # CSV İNDİR
        # ---------------------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "CSV indir",
            csv,
            "veriler.csv",
            "text/csv"
        )

        # ---------------------------
        # VERİTABANI TEMİZLE
        # ---------------------------
        st.subheader("Veritabanı Temizleme")

        if st.button("TÜM VERİLERİ SİL"):
            cursor.execute("DELETE FROM girisler")
            conn.commit()
            st.success("Tüm kayıtlar silindi")

    else:
        st.info("Henüz veri yok")

elif admin_key != "":
    st.error("Yanlış şifre")










