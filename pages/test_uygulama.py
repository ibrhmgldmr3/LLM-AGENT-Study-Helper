#-------------------------------------------------------------------
    # Sakarya üniversitesi
    #Yapay Zeka Dersi
    #Yapay Zeka Ödevi
    #Öğrenci: İbrahim Güldemir   
    #Öğrenci No: B221210052
    #Şube: 1-b
#-------------------------------------------------------------------


import streamlit as st
import json
import os

st.set_page_config(page_title="📝 Test Uygulaması", layout="wide")
st.title("🧪 Çoktan Seçmeli Test")

# Ana klasör ve datas klasörü yollarını düzgün tanımlayalım
ana_klasor = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
datas_klasor = os.path.join(ana_klasor, "datas")

# Test sorularını yükle (önce session state, yoksa dosyadan)
test_sorulari = None

# 1. Session state'den kontrol et
if "test_sorulari" in st.session_state:
    test_sorulari = st.session_state.get("test_sorulari", None)
    st.success("Session state'den test soruları yüklendi.")
# 2. Yoksa dosyadan yüklemeyi dene
else:
    try:
        # Farklı olası dosya yollarını kontrol et
        olasi_yollar = [
            os.path.join(datas_klasor, "test_sorulari.json"),  # En olası konum
            os.path.join(ana_klasor, "test_sorulari.json"),
            os.path.join(ana_klasor, "datas", "test_sorulari.json"),
            "datas/test_sorulari.json",
            "test_sorulari.json",
        ]
        
        dosya_bulundu = False
        for yol in olasi_yollar:
            st.write(f"Kontrol ediliyor: {yol}")
            if os.path.exists(yol):
                with open(yol, "r", encoding="utf-8") as f:
                    test_sorulari = json.load(f)
                    
                # Yüklenen verileri kontrol et
                if test_sorulari and len(test_sorulari) > 0:
                    st.success(f"Test soruları {yol} dosyasından yüklendi. {len(test_sorulari)} soru bulundu.")
                else:
                    st.warning(f"Dosya bulundu ama içi boş veya geçersiz format: {yol}")
                dosya_bulundu = True
                break
                
        if not dosya_bulundu:
            st.error("Hiçbir test dosyası bulunamadı!")
            
    except Exception as e:
        st.error(f"Dosya yüklenirken hata: {str(e)}")


# Test soruları yoksa durdur
if not test_sorulari:
    st.error("Test soruları bulunamadı. Lütfen önce test oluşturun!")

    # Yönlendirme butonu ekle
    if st.button("⬅️ Ana Sayfaya Dön"):
        st.switch_page("streamlit_arayuz.py")

    st.stop()

# Session state'e kaydet (ileride kullanmak için)
st.session_state.test_sorulari = test_sorulari

# Cevapları tutmak için boş sözlük
if "cevaplar" not in st.session_state:
    st.session_state.cevaplar = {}

# Testi göster
with st.form("test_form"):
    for idx, soru in enumerate(test_sorulari):
        st.subheader(f"Soru {idx+1}")
        st.markdown(soru.get("soru", "Soru bulunamadı"))
        
        secenekler = soru.get("secenekler", {})
        secenek_listesi = []
        secenek_metinleri = []
        
        # Şıkları düzenliyoruz (A, B, C, D sırasında)
        for harf in ["A", "B", "C", "D"]:
            if harf in secenekler:
                secenek_listesi.append(harf)
                secenek_metinleri.append(f"{harf}) {secenekler[harf]}")
        
        # Seçenekler yoksa atla
        if not secenek_listesi:
            st.warning(f"Soru {idx+1} için şıklar bulunamadı.")
            continue
            
        # Radio buton göster
        secim = st.radio(
            f"Cevabını seç:",
            options=secenek_listesi,
            format_func=lambda x: f"{x}) {secenekler.get(x, '')}",
            key=f"soru_{idx}",
            index=None  # Önceden seçili değer yok
        )
        
        # Seçimi session state'e kaydet
        if secim:
            st.session_state.cevaplar[idx] = secim
        
        st.divider()

    # Form gönderme butonu
    submit = st.form_submit_button("✅ Testi Bitir ve Sonuçları Göster")

# Sonuçları göster
if submit:
    dogru_sayisi = 0
    toplam_soru = len(test_sorulari)
    
    st.subheader("📊 Test Sonuçları:")
    
    for idx, soru in enumerate(test_sorulari):
        st.markdown(f"**Soru {idx+1}:** {soru.get('soru', 'Soru bulunamadı')}")
        
        # Kullanıcının cevabı
        kullanici_cevabi = st.session_state.cevaplar.get(idx)
        dogru_cevap = soru.get("dogru", "").strip()
        
        # Bazen doğru cevap "A" yerine "A)" gibi gelebiliyor, düzeltme yapalım
        if dogru_cevap and dogru_cevap[-1] == ")":
            dogru_cevap = dogru_cevap[0]
        
        if kullanici_cevabi:
            if kullanici_cevabi == dogru_cevap:
                dogru_sayisi += 1
                st.success(f"✅ Doğru cevap: {dogru_cevap}")
            else:
                st.error(f"❌ Senin cevabın: {kullanici_cevabi}, Doğru cevap: {dogru_cevap}")
        else:
            st.warning("Bu soruyu cevaplamadın!")
        
        # Açıklama
        aciklama = soru.get("aciklama", "")
        if aciklama:
            st.info(f"💡 Açıklama: {aciklama}")
        
        st.divider()
    
    # Toplam skor
    yuzde = int((dogru_sayisi / toplam_soru) * 100) if toplam_soru > 0 else 0
    st.metric("Toplam Skor", f"{dogru_sayisi}/{toplam_soru} (%{yuzde})")
    
    # Başarı mesajı
    if yuzde >= 80:
        st.balloons()
        st.success("🎓 Harika! Konuyu çok iyi anlamışsın.")
    elif yuzde >= 50:
        st.success("👍 İyi iş! Biraz daha çalışarak daha da gelişebilirsin.")
    else:
        st.warning("📚 Bu konuyu biraz daha çalışman gerekiyor.")
    
    # Ana sayfaya dönüş butonu
    if st.button("⬅️ Ana Sayfaya Dön"):
        st.switch_page(r"C:\projeler\yapay_zeka_odev\streamlit_arayuz.py")
