# GİB Mevzuat Yardımcısı

Bu proje, Gelir İdaresi Başkanlığı (GİB) mevzuatları hakkında sorulan soruları yapay zeka yardımıyla yanıtlayan bir web uygulamasıdır.

## Özellikler

- GİB mevzuat sitesinde otomatik arama
- Türkçe doğal dil işleme ile soru cevaplama
- Web tabanlı kullanıcı arayüzü
- Kaynak gösterimi ve güven skoru
- Tüm arama sonuçlarına erişim

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
streamlit run app.py
```

## Kullanım

1. Web arayüzünde sorunuzu Türkçe olarak girin
2. Sistem otomatik olarak:
   - İlgili mevzuatı arar
   - En uygun cevabı oluşturur
   - Kaynak ve güven skorunu gösterir

## Teknik Detaylar

- **AI Model**: HuggingFace Türkçe BERT (savasy/bert-base-turkish-squad)
- **Web Scraping**: BeautifulSoup4
- **Web Arayüzü**: Streamlit
- **Dil**: Python 3.8+

## Notlar

- Uygulama sadece GİB'in resmi web sitesindeki mevzuatları kullanır
- Cevaplar bilgilendirme amaçlıdır, resmi işlemler için GİB'in resmi kanallarını kullanın
- Güven skoru düşük olan cevapları dikkatlice değerlendirin
