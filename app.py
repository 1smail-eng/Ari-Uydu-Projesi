import streamlit as st
import pyrebase
import pandas as pd
import numpy as np
import time

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Arı-Uydu Takip Sistemi", page_icon="🐝", layout="wide")

# 2. Firebase Bağlantısı (Hata Kontrollü)
def firebase_baglan():
    try:
        config = st.secrets["firebase"]
        firebase = pyrebase.initialize_app(config)
        return firebase.database()
    except Exception as e:
        st.error(f"Firebase Hatası: {e}")
        return None

db = firebase_baglan()

# 3. Başlık Alanı
st.title("🛰️ Arı-Uydu Hassas Tarım & Takip")
st.markdown("---")

# 4. Sol Panel (Abonelik ve Ödeme)
if "abone_mi" not in st.session_state:
    st.session_state["abone_mi"] = False

with st.sidebar:
    st.header("👤 Kullanıcı Paneli")
    isim = st.text_input("Adınız Soyadınız:")
    eposta = st.text_input("E-posta Adresiniz:")
    
    st.info("💡 Uydu verileri için 50 TL abonelik gereklidir.")
    odeme_yap = st.button("💳 50 TL Öde ve Abone Ol")

    if odeme_yap:
        if isim and eposta:
            if db:
                # Veritabanına Kayıt
                yeni_kayit = {
                    "ad": isim,
                    "email": eposta,
                    "durum": "Aktif",
                    "tarih": time.ctime()
                }
                db.child("aboneler").push(yeni_kayit)
                # ESP32 için komut
                db.child("cihaz").update({"son_abone": isim, "komut": "YAK"})
            
            st.success(f"Tebrikler {isim}! Ödeme alındı.")
            st.balloons()
            st.session_state["abone_mi"] = True
        else:
            st.warning("Lütfen tüm alanları doldurunuz!")

# 5. Ana Ekran İçeriği
if st.session_state["abone_mi"]:
    st.subheader(f"👋 Hoş geldin {isim}! Güncel Uydu Verilerin:")
    
    sol, sag = st.columns(2)
    
    with sol:
        st.write("### 🌿 Bitki Canlılık Haritası (NDVI)")
        # Tarsus/Mersin koordinat simülasyonu
        harita_verisi = pd.DataFrame(
            np.random.randn(10, 2) / [50, 50] + [37.0, 34.8],
            columns=['lat', 'lon']
        )
        st.map(harita_verisi)
        
    with sag:
        st.write("### 📊 Verim Analizi")
        grafik_verisi = pd.DataFrame(
            np.random.randn(20, 3), 
            columns=['Polen', 'Nem', 'Sıcaklık']
        )
        st.line_chart(grafik_verisi)
else:
    st.warning("🔒 Lütfen sol panelden 50 TL ödeme yaparak uydu verilerini açın.")
    st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800", caption="Sistem Abonelik Bekliyor")

# 6. Alt Bilgi
st.markdown("---")
st.caption("© 2026 Arı-Uydu Teknolojileri | İsmail Barış Danacı")