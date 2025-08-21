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
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class KonuBilgiOlusturucu:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL") 
    
        
        self.llm = ChatOpenAI(
            model_name="meta-llama/llama-4-maverick:free",
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=0.5,
            max_tokens=1500,
        )
        
        # Promptlar
        self.prompt_anlatim = ChatPromptTemplate.from_template("{konu} konusunu {seviye} seviyesinde {secim} şekilde açıkla.")
        self.prompt_uygulama = ChatPromptTemplate.from_template("{anlatim} anlatımına göre {konu} konusunun gerçek dünya uygulamalarını açıkla.")
        self.prompt_hatalar = ChatPromptTemplate.from_template("{uygulama} bilgilerine göre {konu} konusuyla ilgili sık yapılan hataları açıkla.")
        self.prompt_sorular = ChatPromptTemplate.from_template(
            "Önceki hataları göz önünde bulundur: {hatalar}.\n"
            "{konu} konusuyla ilgili 3 tane açıklamalı soru oluştur. Formatı şöyle olsun:\n"
            "Örnek: ...?\nCevap: X\nAçıklama: ..."
        )
        self.prompt_kaynak = ChatPromptTemplate.from_template("{konu} konusuyla ilgili güvenilir öğrenme kaynakları öner.")
        self.prompt_test10 = ChatPromptTemplate.from_template(
            "Aşağıdaki konuda 10 tane çoktan seçmeli test sorusu oluştur. Her biri şu formatta olsun:\n\n"
            "Soru: ...\nA) ...\nB) ...\nC) ...\nD) ...\nDoğru Cevap: X\nAçıklama: ...\n\nKonu: {konu}"
        )

    def konu_uret_ve_kaydet(self, konu, seviye, secim, dosya_adi="konu_bilgileri_lcel.json", test_dosya_adi="test_sorulari.json"):
        girdi = {
            "konu": konu,
            "seviye": seviye,
            "secim": secim
        }
        
        try:
            os.makedirs("datas", exist_ok=True)

            # Her sorguyu ayrı çalıştır ve güvenlik+retry kontrolü uygula
            anlatim_cikti = self._guvenli_invoke(self.prompt_anlatim, girdi, "anlatim")
            uygulama_cikti = self._guvenli_invoke(self.prompt_uygulama, {"konu": konu, "anlatim": anlatim_cikti}, "uygulama")
            kaynaklar_cikti = self._guvenli_invoke(self.prompt_kaynak, {"konu": konu}, "kaynaklar")
            hatalar_cikti = self._guvenli_invoke(self.prompt_hatalar, {"konu": konu, "uygulama": uygulama_cikti}, "hatalar")
            sorular_cikti = self._guvenli_invoke(self.prompt_sorular, {"konu": konu, "hatalar": hatalar_cikti}, "sorular")
            test10_cikti = self._guvenli_invoke(self.prompt_test10, {"konu": konu}, "test_soruları")

            sonuc = {
                "konu": konu,
                "seviye": seviye,
                "secim": secim,
                "anlatim": anlatim_cikti,
                "uygulama": uygulama_cikti,
                "kaynaklar": kaynaklar_cikti,
                "hatalar": hatalar_cikti,
                "sorular": sorular_cikti,
                "test10": test10_cikti,  
            }

            with open(f"datas/{dosya_adi}", "w", encoding="utf-8") as f:
                json.dump(sonuc, f, ensure_ascii=False, indent=4)

            test_sorular = self.test_hazirla(test10_cikti)
            with open(f"datas/{test_dosya_adi}", "w", encoding="utf-8") as test_f:
                json.dump(test_sorular, test_f, ensure_ascii=False, indent=4)

            return sonuc
        
        except Exception as e:
            print(f"[HATA]: {e}")
            raise

    def _guvenli_invoke(self, prompt, girdi, adim_adi, max_retry=3):
        """Her adım için güvenli invoke işlemi, retry destekli"""
        deneme = 0
        while deneme < max_retry:
            try:
                sonuc = (prompt | self.llm).invoke(girdi).content
                if not sonuc or sonuc.isspace():
                    raise ValueError(f"{adim_adi} adımında boş sonuç döndü!")
                if len(sonuc) > 5000:
                    sonuc = sonuc[:5000] + "\n\n[UYARI: Metin uzunluğu sınırlandı.]"
                return sonuc
            except Exception as e:
                deneme += 1
                print(f"[Uyarı] {adim_adi} adımı {deneme}. denemede hata verdi: {e}")
                if deneme < max_retry:
                    time.sleep(2)  # 2 saniye bekle ve tekrar dene
                else:
                    raise RuntimeError(f"{adim_adi} adımı {max_retry} deneme sonunda başarısız oldu.")

                "Örnek: ...?\nCevap: X\nAçıklama: ..."

    def test_hazirla(self, test10_metni):
        """Test metninden soru yapısını ayrıştırır ve güvenlik uygular"""
        if not test10_metni or test10_metni.isspace():
            print("[UYARI]: Boş test metni geldi.")
            return []
        
        # Gelen metni düzeltmeye çalış
        test10_metni = test10_metni.strip()
        
        # Ham veriyi kaydet
        with open("datas/test10_metni.txt", "w", encoding="utf-8") as f:
            f.write(test10_metni)
        
        sorular = []
        
        # "Soru X:" formatını kontrol et - mevcut formatta metin "Soru 1:" şeklinde geliyor
        if "Soru 1:" in test10_metni or "Soru 1 :" in test10_metni:
            print("[BİLGİ]: 'Soru X:' formatında metinler tespit edildi.")
            import re
            # Regex ile "Soru X:" veya "Soru X :" formatındaki başlıkları bul
            soru_blokları = re.split(r'Soru \d+\s*:', test10_metni)
            # İlk eleman genellikle boş olur (başlangıç kısmı), onu atla
            if soru_blokları and not soru_blokları[0].strip():
                soru_blokları = soru_blokları[1:]
        else:
            # Eski yöntem: "Soru:" ile bölme (eğer format değişirse)
            if not test10_metni.startswith("Soru:") and "Soru:" in test10_metni:
                test10_metni = "Soru:" + test10_metni.split("Soru:", 1)[1]
            soru_blokları = test10_metni.split("Soru:")[1:]
        
        if not soru_blokları:
            print("[UYARI]: Sorular düzgün ayrıştırılamadı.")
            return []

        for soru_metni in soru_blokları:
            try:
                satirlar = [s.strip() for s in soru_metni.strip().split('\n') if s.strip()]
                if len(satirlar) < 6:
                    print(f"[UYARI]: Yetersiz satır sayısı: {len(satirlar)}")
                    continue

                soru = satirlar[0]
                secenekler = {}
                
                # Seçenekleri bul
                for satir in satirlar[1:6]:  # İlk 5 satıra bak
                    if len(satir) > 2 and satir[0].isalpha() and satir[1] == ')':
                        secenekler[satir[0]] = satir[2:].strip()
                
                # Doğru cevap ve açıklama bul
                dogru = ""
                aciklama = ""
                
                for satir in satirlar:
                    if "Doğru Cevap:" in satir or "Doğru cevap:" in satir:
                        dogru_kisim = satir.split(":", 1)[1].strip()
                        # Sadece ilk karakteri al (A, B, C, D)
                        dogru = dogru_kisim[0] if dogru_kisim else ""
                    if "Açıklama:" in satir or "Açıklama :" in satir:
                        aciklama = satir.split(":", 1)[1].strip()

                if soru and len(secenekler) >= 2 and dogru:  # En az 2 seçenek olmalı
                    sorular.append({
                        "soru": soru,
                        "secenekler": secenekler,
                        "dogru": dogru,
                        "aciklama": aciklama
                    })
                    print(f"[BİLGİ]: Soru ayrıştırıldı: '{soru[:30]}...'")
                else:
                    print(f"[UYARI]: Eksik veri - soru:{bool(soru)}, seçenek:{len(secenekler)}, doğru:{bool(dogru)}")
                    
            except Exception as e:
                print(f"[Uyarı]: Soru ayrıştırılırken hata: {e}")
                continue
        
        print(f"[BİLGİ]: Toplam {len(sorular)}/{len(soru_blokları)} soru başarıyla ayrıştırıldı.")
        return sorular