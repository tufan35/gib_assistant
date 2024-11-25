# GİB Mevzuat Yardımcısı

Bu proje, Gelir İdaresi Başkanlığı (GİB) mevzuatları hakkında sorulan soruları yapay zeka yardımıyla yanıtlayan bir web uygulamasıdır.

## Özellikler

- GİB mevzuat sitesinde otomatik arama
- Türkçe doğal dil işleme ile soru cevaplama
- Web tabanlı kullanıcı arayüzü
- Kaynak gösterimi ve güven skoru
- Tüm arama sonuçlarına erişim

## Proje Güncellemeleri

### KDV1 Beyannamesi Adımları
- KDV1 beyannamesi hazırlama adımları detaylandırıldı.
- Her adım için alt başlıklar ve örnekler eklendi.
- Yanıtların daha uzun ve detaylı olması sağlandı.

### Model Parametreleri
- `max_new_tokens` parametresi 1024'e çıkarıldı, böylece daha uzun yanıtlar üretilebiliyor.
- `temperature` 0.1 olarak ayarlandı, bu da daha yaratıcı yanıtlar sağlıyor.
- `do_sample` parametresi True yapıldı, yanıtların daha doğal olmasını sağlıyor.

### Diğer Değişiklikler
- `ai_assistant.py`, `app.py`, ve `mevzuat_scraper.py` dosyalarında iyileştirmeler yapıldı.
- Yeni log dosyaları (`ai_assistant.log` ve `scraper.log`) eklendi.
- Bağımlılıklar güncellendi.

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
streamlit run app.py
```

## Teknik Detaylar

- Kullanılan AI Modeli: Mistral-7B-Instruct-v0.2
- Model parametreleri optimize edildi:
  - `max_new_tokens`: 1024
  - `temperature`: 0.1
  - `do_sample`: True
- Yanıtların daha doğal ve detaylı olması sağlandı.

### API Token Ekleme
- Hugging Face API'sini kullanabilmek için bir API token gereklidir.
- Token'ınızı `.env` dosyasına `HUGGING_FACE_TOKEN` olarak ekleyin:
  ```plaintext
  HUGGING_FACE_TOKEN=your_hugging_face_token_here
  ```
- Token'ı almak için [Hugging Face](https://huggingface.co/settings/tokens) hesabınıza giriş yaparak yeni bir token oluşturabilirsiniz.

## Kullanım

1. Web arayüzünde sorunuzu Türkçe olarak girin
2. Sistem otomatik olarak:
   - İlgili mevzuatı arar
   - En uygun cevabı oluşturur
   - Kaynak ve güven skorunu gösterir

## Teknik Detaylar

- **Web Scraping**: BeautifulSoup4
- **Web Arayüzü**: Streamlit
- **Dil**: Python 3.8+

## Notlar

- Uygulama sadece GİB'in resmi web sitesindeki mevzuatları kullanır
- Cevaplar bilgilendirme amaçlıdır, resmi işlemler için GİB'in resmi kanallarını kullanın
- Güven skoru düşük olan cevapları dikkatlice değerlendirin

## Katkıda Bulunma
Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın.

## Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.
