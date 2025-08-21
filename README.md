# Yapay Zeka Ödevi

## Proje Hakkında
Bu proje, yapay zeka dersi için hazırlanmış öğrenme asistanı uygulamasıdır. Uygulama, kullanıcıların seçtikleri konuları öğrenmelerine yardımcı olmak için yapay zeka destekli içerikler oluşturur. Kullanıcılar, istedikleri konuyu, seviyeyi ve anlatım türünü seçerek kişiselleştirilmiş öğrenme materyalleri elde edebilirler.

## Özellikler
- Konuya özel detaylı anlatımlar
- Gerçek hayat uygulamaları
- Sık yapılan hatalar ve çözümleri
- Örnek sorular ve açıklamaları
- Çoktan seçmeli testler
- Öğrenme kaynakları önerileri

## Kurulum
Projeyi çalıştırmak için aşağıdaki adımları izleyin:

```
bash
# Repository'yi klonlayın
git clone https://github.com/kullaniciadi/yapay_zeka_odev.git

# Proje dizinine gidin
cd yapay_zeka_odev

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
```

## Kullanım
Projeyi şu şekilde çalıştırabilirsiniz:

```
bash
python -m streamlit run .\streamlit_arayuz.py
```

## Dosya Yapısı
'''
yapay_zeka_odev/
├── data/                # Veri dosyaları
├── models/              # Model dosyaları
├── notebooks/           # Jupyter notebook dosyaları
├── src/                 # Kaynak kodlar
├── requirements.txt     # Gerekli kütüphaneler
└── README.md            # Bu dosya
'''

## Gereksinimler
Python 3.8+
Streamlit
LangChain
OpenAI API / OpenRouter API erişimi
python-dotenv

## Proje Özeti

Bu proje, kullanıcılara kişiselleştirilmiş öğrenme deneyimi sunmak için yapay zeka teknolojilerini kullanan bir öğrenme asistanı uygulamasıdır. İşte temel işlevleri:

1. **İçerik Oluşturma**: [ogrenme_asistani.py](\ogrenme_asistani.py) dosyasındaki `KonuBilgiOlusturucu` sınıfı, LangChain ve OpenAI/OpenRouter API'larını kullanarak seçilen konu hakkında kapsamlı içerikler üretir.

2. **Kullanıcı Arayüzü**: [streamlit_arayuz.py](\streamlit_arayuz.py) dosyası, Streamlit kütüphanesi kullanılarak geliştirilmiş kullanıcı dostu bir arayüz sunar.

3. **Test Uygulaması**: [pages/test_uygulama.py](\pages\test_uygulama.py) dosyası, oluşturulan içeriklere ait testleri kullanıcıya sunar ve sonuçları değerlendirir.

Kullanıcılar, herhangi bir konu seçip (örneğin "veri yapıları"), seviye (Ortaokul, Lise, Üniversite) ve anlatım tipini (özet veya kapsamlı) belirleyerek ihtiyaçlarına uygun öğrenme materyalleri elde edebilirler.## Proje Özeti

Bu proje, kullanıcılara kişiselleştirilmiş öğrenme deneyimi sunmak için yapay zeka teknolojilerini kullanan bir öğrenme asistanı uygulamasıdır. İşte temel işlevleri:

1. **İçerik Oluşturma**: [ogrenme_asistani.py](\ogrenme_asistani.py) dosyasındaki `KonuBilgiOlusturucu` sınıfı, LangChain ve OpenAI/OpenRouter API'larını kullanarak seçilen konu hakkında kapsamlı içerikler üretir.

2. **Kullanıcı Arayüzü**: [streamlit_arayuz.py](\streamlit_arayuz.py) dosyası, Streamlit kütüphanesi kullanılarak geliştirilmiş kullanıcı dostu bir arayüz sunar.

3. **Test Uygulaması**: [pages/test_uygulama.py](\pages\test_uygulama.py) dosyası, oluşturulan içeriklere ait testleri kullanıcıya sunar ve sonuçları değerlendirir.

Kullanıcılar, herhangi bir konu seçip (örneğin "veri yapıları"), seviye (Ortaokul, Lise, Üniversite) ve anlatım tipini (özet veya kapsamlı) belirleyerek ihtiyaçlarına uygun öğrenme materyalleri elde edebilirler.

## Geliştirici
[İbrahim Güldemir] - [ibrahimguldemir123@gmail.com]

## Lisans
Bu proje [LİSANS TÜRÜ] lisansı altında lisanslanmıştır.
