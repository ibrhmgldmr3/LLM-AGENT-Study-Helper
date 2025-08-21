#-------------------------------------------------------------------
    # Sakarya üniversitesi
    #Yapay Zeka Dersi
    #Yapay Zeka Ödevi
    #Öğrenci: İbrahim Güldemir   
    #Öğrenci No: B221210052
    #Şube: 1-b
#-------------------------------------------------------------------


import json
import os
import time
import streamlit as st
from ogrenme_asistani import KonuBilgiOlusturucu


# --- Sayfa Ayarları ---
st.set_page_config(page_title="📚 AI Öğrenme Asistanı", layout="wide", page_icon="📘")

# --- Başlık ve Açıklama ---
st.title("📘 AI Destekli Öğrenme Asistanı")
st.markdown("Konu anlatımları, uygulamalar, hatalar ve testlerle **kişiselleştirilmiş** öğrenme deneyimi!")

# --- Session State Başlat ---
if "olusturucu" not in st.session_state:
    st.session_state.olusturucu = KonuBilgiOlusturucu()

# --- Konu Seçimi ---
with st.container():
    st.subheader("🎯 Öğrenmek istediğin konuyu seç")
    with st.form("konu_formu", clear_on_submit=False):
        st.markdown("**Konu, seviye ve anlatım tipi seçin:**")
        konu = st.text_input("Öğrenmek istediğin konu", placeholder="Örn: Yapay Zeka")
        seviye = st.selectbox("Seviyeni seç", ["Ortaokul", "Lise", "Üniversite"])
        secim = st.radio("Anlatım tipi", ["özet", "kapsamlı"], horizontal=True)
        gonder = st.form_submit_button("📤 İçerik Oluştur")

# --- Fonksiyonlar ---
def konu_olustur(konu, seviye, secim):
    try:
        progress = st.progress(0, text="🚀 İçerik oluşturuluyor...")
        olusturucu = st.session_state.olusturucu
        
        sonuc = olusturucu.konu_uret_ve_kaydet(
            konu=konu,
            seviye=seviye,
            secim=secim,
        )

        st.session_state.konu = konu
        st.session_state.seviye = seviye
        st.session_state.secim = secim
        st.session_state.sonuc = sonuc
        st.session_state.test_hazir = True

        progress.progress(100, text="✅ İçerikler Hazır!")

        st.success("✅ İçerikler başarıyla oluşturuldu!")
        
        return True
    except Exception as e:
        st.error(f"🚨 Bir hata oluştu: {str(e)}")
        return False

def test_yukle():
    try:
        dosya_adi = f"datas/test_sorulari.json"
        if os.path.exists(dosya_adi):
            with open(dosya_adi, "r", encoding="utf-8") as f:
                test_sorulari = json.load(f)
            st.session_state.test_sorulari = test_sorulari
            st.success("✅ Test soruları yüklendi!")
        else:
            st.error("🚨 Test dosyası bulunamadı!")
    except Exception as e:
        st.error(f"🚨 Test yüklenirken hata: {str(e)}")

# --- İçerik Oluşturulduysa ---
if gonder and konu:
    basarili = konu_olustur(konu, seviye, secim)
    if basarili:
        st.markdown("---")
        st.subheader("📖 Konu İçeriği")

        tabs = st.tabs(["📘 Anlatım", "🌍 Gerçek Hayat Uygulamaları", "⚠️ Sık Yapılan Hatalar", "🧪 Örnek Sorular", "🔗 Öğrenme Kaynakları"])

        with tabs[0]:  # Anlatım
            anlatim = st.session_state.sonuc.get("anlatim", "Anlatım bulunamadı.")
            if anlatim:
                for satir in anlatim.split("\n"):
                    if satir.strip():
                        st.markdown(f"### {satir}")

        with tabs[1]:  # Uygulamalar
            uygulama = st.session_state.sonuc.get("uygulama", "Uygulama bilgisi bulunamadı.")
            st.markdown(uygulama)

        with tabs[2]:  # Hatalar
            hatalar = st.session_state.sonuc.get("hatalar", "Hatalar bilgisi bulunamadı.")
            st.markdown(hatalar)

        with tabs[3]:  # Örnek Sorular
            sorular = st.session_state.sonuc.get("sorular", "Örnek sorular bulunamadı.")
            if sorular:
                for soru in sorular.split("\n\n"):
                    if soru.strip():
                        st.markdown(f"### {soru}")

        with tabs[4]:  # Kaynaklar
            kaynaklar = st.session_state.sonuc.get("kaynaklar", "Kaynak bilgisi bulunamadı.")
            st.markdown(kaynaklar)

        st.download_button(
            label="📥 İçeriği JSON olarak indir",
            data=json.dumps(st.session_state.sonuc, ensure_ascii=False, indent=4),
            file_name=f"{konu}_icerik.json",
            mime="application/json"
        )

        st.markdown("---")
        st.subheader("📝 Test İşlemleri")
        
        if "test_hazir" in st.session_state and st.session_state.test_hazir:
            st.success("✅ Test soruları hazır!")
            st.markdown("Test sorularını görmek için aşağıdaki butona tıklayın.")
            
            if st.button("📋 Test Sorularını Gör"):
                st.switch_page("pages/test_uygulama.py")
        st.markdown("---")
        st.subheader("🛠️ Sorun Giderme Araçları")
        def test_kurtarma_dosyadan():
            """Test10_metni.txt dosyasından test sorularını kurtarır"""
            try:
                dosya_yolu = os.path.join("datas", "test10_metni.txt")
                if not os.path.exists(dosya_yolu):
                    st.error(f"❗ Test metni dosyası bulunamadı: {dosya_yolu}")
                    return False
                
                with open(dosya_yolu, "r", encoding="utf-8") as f:
                    test10_metni = f.read()
                
                if not test10_metni.strip():
                    st.error("❗ Test metni dosyası boş!")
                    return False
                
                # Manuel olarak soruları ayrıştır
                import re
                sorular = []
                soru_bloklari = re.split(r'Soru \d+\s*:', test10_metni)
                
                # İlk eleman boş olabilir
                if soru_bloklari and not soru_bloklari[0].strip():
                    soru_bloklari = soru_bloklari[1:]
                
                # Her soru bloğunu işle
                for idx, blok in enumerate(soru_bloklari):
                    try:
                        satirlar = [s.strip() for s in blok.strip().split('\n') if s.strip()]
                        if len(satirlar) < 6:
                            continue
                        
                        soru = satirlar[0]
                        secenekler = {}
                        dogru = ""
                        aciklama = ""
                        
                        for satir in satirlar:
                            if len(satir) > 2 and satir[0].isalpha() and satir[1] == ')':
                                secenekler[satir[0]] = satir[2:].strip()
                            elif "Doğru Cevap:" in satir or "Doğru cevap:" in satir:
                                dogru_kisim = satir.split(":", 1)[1].strip()
                                dogru = dogru_kisim[0] if dogru_kisim else ""
                            elif "Açıklama:" in satir or "Açıklama :" in satir:
                                aciklama = satir.split(":", 1)[1].strip()
                        
                        if soru and len(secenekler) >= 2 and dogru:
                            sorular.append({
                                "soru": soru,
                                "secenekler": secenekler,
                                "dogru": dogru,
                                "aciklama": aciklama
                            })
                    except Exception as e:
                        st.warning(f"Soru {idx+1} işlenirken hata: {str(e)}")
                
                if not sorular:
                    st.warning("⚠️ Hiçbir soru kurtarılamadı!")
                    return False
                    
                # Soruları kaydet
                test_dosya_yolu = os.path.join("datas", "test_sorulari.json")
                with open(test_dosya_yolu, "w", encoding="utf-8") as f:
                    json.dump(sorular, f, ensure_ascii=False, indent=4)
                    
                # Session state'e kaydet
                st.session_state.test_sorulari = sorular
                st.session_state.test_hazir = True
                
                st.success(f"✅ {len(sorular)} soru başarıyla kurtarıldı ve kaydedildi!")
                return True
                
            except Exception as e:
                st.error(f"🚨 Dosyadan test kurtarma hatası: {str(e)}")
                return False
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Test10 Metninden Soruları Yeniden Oluştur"):
                test_kurtarma_dosyadan()
        with col2:
            if st.button("🔍 Test Dosya Durumunu Kontrol Et"):
                try:
                    txt_yol = os.path.join("datas", "test10_metni.txt")
                    json_yol = os.path.join("datas", "test_sorulari.json")
                    
                    if os.path.exists(txt_yol):
                        with open(txt_yol, "r", encoding="utf-8") as f:
                            txt_icerik = f.read()
                        st.info(f"📄 test10_metni.txt dosyası mevcut ({len(txt_icerik)} karakter)")
                    else:
                        st.warning("❌ test10_metni.txt dosyası bulunamadı!")
                        
                    if os.path.exists(json_yol):
                        with open(json_yol, "r", encoding="utf-8") as f:
                            json_icerik = json.load(f)
                        st.info(f"📊 test_sorulari.json dosyası mevcut ({len(json_icerik)} soru)")
                    else:
                        st.warning("❌ test_sorulari.json dosyası bulunamadı!")
                except Exception as e:
                    st.error(f"Kontrol hatası: {str(e)}")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ by İBRAHİM GÜLDEMİR | 2025")
