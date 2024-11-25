import requests
from dotenv import load_dotenv
import time
import logging

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_assistant.log'),
        logging.StreamHandler()
    ]
)

class AIAssistant:
    def __init__(self):
        # Hugging Face token'ını yükle
        load_dotenv()
        self.hf_token = "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"
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        # API headers
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        logging.info("AI asistan hazır!")
    
    def _make_api_request(self, prompt, max_retries=3):
        """Hugging Face API'sine istek gönder."""
        api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        for attempt in range(max_retries):
            try:
                logging.info(f"API isteği yapılıyor (deneme {attempt + 1}/{max_retries})")
                
                # Model parametrelerini güncelle
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 1024,  # Daha uzun yanıtlar için artırıldı
                        "temperature": 0.1,      # Daha tutarlı yanıtlar için düşürüldü
                        "top_p": 0.1,
                        "do_sample": True,
                        "return_full_text": False,
                        "repetition_penalty": 1.2
                    }
                }
                
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"API hatası: {str(e)}")
                    return None
                time.sleep(1)
    
    def get_quick_answer(self, question):
        """GPT'den hızlı bir cevap al."""
        try:
            system_prompt = """Sen GİB (Gelir İdaresi Başkanlığı) KDV uzmanısın. KDV beyannameleri konusunda detaylı ve net bilgiler veriyorsun.
            TÜM YANITLARINI TÜRKÇE OLARAK VERMELİSİN. İNGİLİZCE KULLANMA!
            HER SORUYA TAM VE EKSİKSİZ YANIT VER, YARIM BIRAKMA!

            KDV1 BEYANNAMESİ HAZIRLAMA ADIMLARI (TÜM ADIMLARI EKSİKSİZ TAMAMLA):
            1. İnteraktif Vergi Dairesi Giriş:
               - https://ivd.gib.gov.tr adresine gidin
               - e-Devlet şifreniz veya GİB şifreniz ile giriş yapın
               - Güvenlik doğrulamasını tamamlayın
               - Ana sayfada "Beyanname İşlemleri" bölümüne ilerleyin

            2. Beyanname Seçimi ve Dönem:
               - Sol menüden "Beyanname İşlemleri"ne tıklayın
               - "Beyanname Hazırla" seçeneğini seçin
               - Açılan listeden "KDV-1" beyannamesini bulun ve tıklayın
               - Vergilendirme dönemini seçin (örn: 2023/Kasım)
               - Normal/Düzeltme beyanname seçimini yapın

            3. Matrah Bilgileri - Teslimler ve Hizmetler:
               - Tablo I'de yer alan "Mal ve Hizmet Teslimleri" bölümünü doldurun
               - KDV hariç tutarları ilgili satırlara girin
               - Teslim türüne göre KDV oranlarını (%1, %8, %18, %20) seçin
               - Hesaplanan KDV tutarlarını kontrol edin
               - Varsa tevkifat uygulanan işlemleri belirtin

            4. Matrah Bilgileri - İstisnalar:
               - Kısmi istisna kapsamındaki işlemleri girin
               - Tam istisna kapsamındaki işlemleri belirtin
               - İhraç kayıtlı teslimleri ayrı olarak gösterin
               - İstisna türüne göre belge tarih ve numaralarını ekleyin
               - İstisna kapsamındaki tutarları KDV'siz olarak girin

            5. İndirimler - Alış ve İthalat:
               - Yurt içi mal ve hizmet alımlarına ait KDV'yi girin
               - İthalat işlemlerine ait ödenen KDV'yi ekleyin
               - Tevkifata tabi işlemlerden doğan KDV'yi belirtin
               - İade hakkı doğuran işlemlere ait KDV'yi ayırın
               - Kısmi istisna kapsamında indirilecek KDV'yi hesaplayın

            6. İndirimler - Devreden ve İade:
               - Önceki dönemden devreden KDV tutarını girin
               - Bu döneme ait indirilecek KDV'yi ekleyin
               - İade edilebilir KDV tutarını hesaplayın
               - Tecil edilebilir KDV varsa belirtin
               - Sonraki döneme devreden KDV'yi kontrol edin

            7. Ekler ve Bildirimler:
               - Form BA-BS bildirimlerini hazırlayın
               - İhraç kayıtlı teslim bildirimlerini doldurun
               - KDV tevkifat bildirimini tamamlayın
               - İade talep edilen işlemlere ait listeleri ekleyin
               - Belgelerin tarih ve numaralarını kontrol edin

            8. Beyanname Ekleri:
               - Gerekli tüm listeleri hazırlayın
               - İade talep ediliyorsa YMM raporunu ekleyin
               - İhracat istisnası varsa gümrük beyannamelerini iliştirin
               - İstisna belgelerinin fotokopilerini ekleyin
               - Tevkifat ile ilgili belgeleri düzenleyin

            9. Kontrol ve Hatalar:
               - Sistem kontrollerini çalıştırın
               - Matematiksel hataları kontrol edin
               - Uyarı mesajlarını tek tek inceleyin
               - Tutarsızlıkları düzeltin
               - Beyanname ve eklerinin uyumunu kontrol edin

            10. Onaylama ve Gönderim:
                - Beyanname önizlemesini yapın
                - Tüm bilgileri son kez gözden geçirin
                - Elektronik imza ile imzalayın
                - Beyannameyi gönderin
                - Tahakkuk fişini alın ve saklayın

            KDV1 BEYANNAMESİ VERME SÜRELERİ:
            - Her ayın 1-26'sı arasında verilir
            - Bir önceki ayın işlemlerini kapsar
            - Son gün tatile denk gelirse, takip eden ilk iş günü son gündür
            - Beyanname verme ve ödeme süreleri farklı olabilir
            - Sürelere uyulmaması halinde cezai işlem uygulanır"""

            prompt = f"""<s>[INST] {system_prompt}

            Soru: {question}

            Yukarıdaki bilgileri kullanarak detaylı ve eksiksiz cevap ver. Yanıtını kesinlikle Türkçe olarak vermelisin, İngilizce kullanma! Tüm adımları eksiksiz açıkla, yarım bırakma! Her adımı en az 3-4 satır detaylı açıkla. [/INST]</s>"""
            
            logging.info("GPT'den hızlı cevap alınıyor")
            result = self._make_api_request(prompt)
            
            if isinstance(result, list) and len(result) > 0:
                answer = result[0].get('generated_text', '').strip()
            else:
                answer = "Üzgünüm, şu anda cevap üretemiyorum."
            
            needs_update = any(word in answer.lower() for word in ['güncel', 'son', 'yeni', 'değişiklik'])
            
            logging.info(f"Cevap üretildi. Güncelleme gerekiyor mu: {needs_update}")
            
            return {
                'answer': answer,
                'needs_update': needs_update
            }
            
        except Exception as e:
            logging.error(f"GPT cevabı alınırken hata oluştu: {e}")
            return {
                'answer': "Üzgünüm, şu anda cevap üretemiyorum. Lütfen tekrar deneyin.",
                'needs_update': True
            }
    
    def answer_question(self, question, context):
        """Verilen bağlam içinde soruyu cevaplar."""
        try:
            system_prompt = "Sen GİB (Gelir İdaresi Başkanlığı) KDV uzmanısın. Sadece verilen bağlamdaki bilgileri kullanarak cevap ver."

            prompt = f"""<s>[INST] {system_prompt}

            Bağlam: {context}

            Soru: {question}

            Sadece bağlamdaki bilgileri kullanarak doğrudan ve net cevap ver. [/INST]</s>"""
            
            logging.info("Bağlam ile cevap üretiliyor")
            result = self._make_api_request(prompt)
            
            if isinstance(result, list) and len(result) > 0:
                answer = result[0].get('generated_text', '').strip()
            else:
                answer = "Üzgünüm, şu anda cevap üretemiyorum."
            
            return {
                'answer': answer,
                'confidence': 0.9 if answer else 0.0
            }
            
        except Exception as e:
            logging.error(f"Soru cevaplanırken hata oluştu: {e}")
            return {
                'answer': "Üzgünüm, bu soruyu şu anda cevaplayamıyorum.",
                'confidence': 0.0
            }
    
    def get_best_answer(self, question, search_results, confidence_threshold=0.7):
        """Tüm arama sonuçları içinde en iyi cevabı bulur."""
        best_answer = None
        max_confidence = 0
        
        logging.info(f"{len(search_results)} arama sonucu işleniyor")
        for result in search_results:
            answer = self.answer_question(question, result['content'])
            
            if answer['confidence'] > max_confidence and answer['confidence'] >= confidence_threshold:
                max_confidence = answer['confidence']
                best_answer = {
                    'answer': answer['answer'],
                    'confidence': answer['confidence'],
                    'source': result.get('source', 'Bilinmeyen Kaynak'),
                    'link': result.get('link', ''),
                    'date': result.get('date', '')
                }
        
        if best_answer is None:
            logging.warning("Arama sonuçlarında uygun cevap bulunamadı")
            return {
                'answer': "Üzgünüm, bu soru için güncel mevzuatta bir cevap bulamadım.",
                'confidence': 0.0,
                'source': '',
                'link': '',
                'date': ''
            }
        
        logging.info(f"En iyi cevap bulundu. Güven skoru: {best_answer['confidence']:.2f}")
        return best_answer
