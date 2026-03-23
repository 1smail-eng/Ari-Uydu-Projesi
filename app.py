import streamlit as st
import pyrebase
import time

# Sayfa Ayarları
st.set_page_config(page_title="Valet Hero", page_icon="🚀")

# 🛠️ Firebase Bağlantısı (Secrets'tan çekiyoruz)
try:
    # Streamlit Secrets'taki [firebase] başlığı altındaki verileri alır
    firebaseConfig = st.secrets["firebase"]
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
except Exception as e:
    st.error(f"⚠️ Firebase bağlantı hatası! Secrets kısmını kontrol et. Hata: {e}")

# --- ARAYÜZ ---
st.title("🚀 VALET HERO")
st.subheader("Hızlı Ödeme ve Takip Paneli")

# Kullanıcı Girişi
name = st.text_input("Adınız Soyadınız:", placeholder="Örn: İsmail Barış Danacı")

# Ödeme Butonu
if st.button("💳 50 TL Öde ve Başlat"):
    if name:
        try:
            # Firebase'e veri gönderimi
            data = {
                "komut": "YAK",
                "kullanici": name,
                "zaman": time.strftime("%H:%M:%S")
            }
            # 'cihaz' düğümü altına veriyi yazıyoruz
            db.child("cihaz").update(data)
            
            # Başarı mesajı ve animasyon
            st.balloons()
            st.success(f"✅ Harika! {name}, ödeme başarıyla alındı.")
            st.info("📡 Masandaki OLED ekrana sinyal gönderildi!")
            
        except Exception as e:
            st.error(f"❌ Veri gönderilemedi: {e}")
    else:
        st.warning("⚠️ Lütfen bir isim girmeden ödeme yapma!")

# Alt Bilgi
st.markdown("---")
st.caption("Valet Hero v2.0 - Firebase & Streamlit Bridge")
