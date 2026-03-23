import streamlit as st
from streamlit_folium import st_folium
import folium
import pyrebase
from datetime import datetime, timedelta

# --- SAYFA TASARIMI ---
st.set_page_config(page_title="Arı-Uydu Takip", layout="wide")
st.title("🐝 Arı-Uydu: Akıllı Kovan Tahmin Sistemi")

# Firebase Ayarları (Firebase Console'dan alacağın bilgiler)
config = {
    "apiKey": "BURAYA_API_KEY",
    "authDomain": "PROJEN.firebaseapp.com",
    "databaseURL": "https://PROJEN-default-rtdb.firebaseio.com",
    "storageBucket": "PROJEN.appspot.com"
}
db = pyrebase.initialize_app(config).database()

# --- YAN MENÜ (ABONELİK KONTROLÜ) ---
with st.sidebar:
    st.header("👤 Giriş Paneli")
    kullanici = st.text_input("Müşteri Adınız:")
    is_active = False

    if kullanici:
        # Firebase'den bitiş tarihini kontrol et
        bitis = db.child("aboneler").child(kullanici).child("bitis").get().val()
        if bitis and datetime.now() < datetime.strptime(bitis, "%Y-%m-%d"):
            is_active = True
            st.success("Abonelik Aktif ✅")
        else:
            st.error("Abonelik Süresi Dolmuş ❌")
            if st.button("50 TL Öde ve Abone Ol"):
                # Ödeme yapıldığında tarihi 30 gün uzat ve ESP32'ye bildir
                yeni_tarih = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                db.child("aboneler").child(kullanici).set({"bitis": yeni_tarih})
                db.child("toplam_kazanc").set((db.child("toplam_kazanc").get().val() or 0) + 50)
                db.child("son_abone").set(kullanici)
                st.rerun()

# --- ANA EKRAN (SADECE ABONE AKTİFSE) ---
if is_active:
    tab1, tab2 = st.tabs(["📍 Konum Analizi", "🔍 Otomatik Keşif"])
    
    with tab1:
        st.subheader("Kovanınızın Yerini Seçin")
        m = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles='Stamen Terrain')
        m.add_child(folium.LatLngPopup())
        map_res = st_folium(m, height=450, width=800)
        
        if st.button("Tahmin Al"):
            # Tahmin mantığını buraya ekleyeceğiz
            st.info("Tahmin: Bu bölgenin dolma ihtimali YÜKSEK! 🍯")

    with tab2:
        st.subheader("En Verimli Noktaları Bul")
        if st.button("Bölgemdeki En İyi 3 Yeri Göster"):
            st.write("1. Nokta: %94 Verim Potansiyeli")
            st.write("2. Nokta: %88 Verim Potansiyeli")
else:
    st.warning("Lütfen sol panelden giriş yapın veya aboneliğinizi başlatın.")