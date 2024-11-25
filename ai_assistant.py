from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch

class AIAssistant:
    def __init__(self):
        # Türkçe soru cevaplama modeli
        self.model_name = "savasy/bert-base-turkish-squad"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print("AI model yükleniyor...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        
        # Pipeline oluştur
        self.qa_pipeline = pipeline(
            'question-answering',
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )
        print("AI model yüklendi!")
    
    def answer_question(self, question, context):
        """Verilen bağlam içinde soruyu cevaplar."""
        try:
            # Bağlamı makul bir uzunlukta tut
            max_context_length = 512
            if len(context) > max_context_length:
                context = context[:max_context_length]
            
            # Soru-cevap işlemi
            result = self.qa_pipeline({
                'question': question,
                'context': context
            })
            
            return {
                'answer': result['answer'],
                'confidence': result['score']
            }
            
        except Exception as e:
            print(f"Soru cevaplanırken hata oluştu: {e}")
            return {
                'answer': "Üzgünüm, bu soruyu şu anda cevaplayamıyorum.",
                'confidence': 0.0
            }
    
    def get_best_answer(self, question, search_results, confidence_threshold=0.7):
        """Tüm arama sonuçları içinde en iyi cevabı bulur."""
        best_answer = None
        best_confidence = 0
        
        for result in search_results:
            answer = self.answer_question(question, result['content'])
            
            if answer['confidence'] > best_confidence:
                best_confidence = answer['confidence']
                best_answer = {
                    'answer': answer['answer'],
                    'confidence': answer['confidence'],
                    'source': result['title'],
                    'link': result['link']
                }
        
        # Güven skoru yeterli değilse genel bir cevap döndür
        if not best_answer or best_answer['confidence'] < confidence_threshold:
            return {
                'answer': "Bu konuda kesin bir bilgi bulamadım. Lütfen GİB'in resmi kanallarından teyit ediniz.",
                'confidence': 0.0,
                'source': None,
                'link': None
            }
        
        return best_answer
