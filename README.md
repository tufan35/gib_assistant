# GİB AI Asistan

GİB AI Asistan, Gelir İdaresi Başkanlığı ile ilgili sorularınızı yanıtlayan ve belge analizleri yapan bir yapay zeka uygulamasıdır.

## 📸 Ekran Görüntüleri

### Ana Ekran
![Ana Ekran](images/main_screen.png)

### Soru & Cevap
![Soru Cevap](images/qa_screen.png)

### Dosya Analizi
![Dosya Analizi](images/file_analysis.png)

## ✨ Özellikler

### Soru-Cevap
- Vergi mevzuatı ve GİB ile ilgili sorulara yanıt
- Mevzuat kaynaklarında arama:
  - GİB Mevzuat
  - Mevbank
- Farklı AI model seçenekleri:
  - Hugging Face (Mistral)
  - OpenAI (GPT-3.5/4)
  - Anthropic (Claude)

### Dosya Analizi
- PDF ve XML dosya desteği
- Dosya içeriğine göre mevzuat araması
- Detaylı analiz ve öneriler
- İlgili kanun maddelerine referanslar

## 🚀 Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/tufan35/gib_assistant.git
cd gib_assistant
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun:
```bash
cp .env.example .env
```

4. API anahtarlarınızı `.env` dosyasına ekleyin:
```
HUGGING_FACE_TOKEN=your_token_here
ANTHROPIC_API_KEY=your_token_here
OPENAI_API_KEY=your_token_here
```

## 📖 Kullanım

1. Uygulamayı başlatın:
```bash
streamlit run app.py
```

2. Web tarayıcınızda açılan arayüzü kullanın:
   - Soru-Cevap: Sorunuzu yazın ve mevzuat arama seçeneklerini belirleyin
   - Dosya Analizi: PDF/XML dosyanızı yükleyin ve analiz edin

## 🔧 Teknik Detaylar

- **Maksimum Dosya Boyutu**: 25MB
- **Desteklenen Dosya Formatları**: PDF, XML
- **Dil**: Python 3.8+
- **Ana Framework**: Streamlit

## 📄 Notlar

- API anahtarlarınızı güvenli tutun ve paylaşmayın
- Rate limit'lere dikkat edin
- Mevzuat araması için ilgili checkbox'ları işaretleyin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
