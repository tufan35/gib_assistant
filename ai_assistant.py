import requests
import json
import time
import logging
import os
import PyPDF2
from lxml import etree
import io
from mevzuat_scraper import MevzuatScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='ai_assistant.log'
)

class AIAssistant:
    def __init__(self, model_provider="huggingface", api_token=None):
        self.model_provider = model_provider
        self.api_token = api_token
        self.mevzuat_scraper = MevzuatScraper()
        
        self.model_configs = {
            "huggingface": {
                "api_url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                "headers": {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }
            },
            "anthropic": {
                "api_url": "https://api.anthropic.com/v1/messages",
                "headers": {
                    "anthropic-version": "2023-06-01",
                    "x-api-key": self.api_token,
                    "Content-Type": "application/json"
                }
            },
            "openai": {
                "api_url": "https://api.openai.com/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }
            }
        }
        
        self.current_config = self.model_configs.get(model_provider, self.model_configs["huggingface"])
        logging.info(f"AI asistan {model_provider} ile başlatıldı!")

    def _make_api_request(self, prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                logging.info(f"API isteği yapılıyor (deneme {attempt + 1}/{max_retries})")
                
                if self.model_provider == "huggingface":
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 2048,
                            "temperature": 0.1,
                            "top_k": 10,
                            "top_p": 0.95,
                            "repetition_penalty": 1.2,
                            "do_sample": True,
                            "return_full_text": False
                        }
                    }
                elif self.model_provider == "anthropic":
                    payload = {
                        "messages": [{"role": "user", "content": prompt}],
                        "model": "claude-2",
                        "max_tokens": 1024
                    }
                else:  # openai
                    payload = {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "system",
                                "content": "Sen bir GİB (Gelir İdaresi Başkanlığı) uzmanısın. Türk vergi mevzuatı ve beyanname süreçleri hakkında detaylı bilgi sahibisin."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 1024,
                        "temperature": 0.7
                    }
                
                response = requests.post(
                    self.current_config["api_url"],
                    headers=self.current_config["headers"],
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                
                if self.model_provider == "huggingface":
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return [{"generated_text": result[0].get("generated_text", "")}]
                    else:
                        return [{"generated_text": result[0]}]
                elif self.model_provider == "anthropic":
                    result = response.json()
                    return [{"generated_text": result["content"][0]["text"]}]
                else:  # openai
                    result = response.json()
                    return [{"generated_text": result["choices"][0]["message"]["content"]}]

            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"API hatası: {str(e)}")
                    return None
                time.sleep(2 ** attempt)
    
    def get_answer(self, question, search_gib=False, search_mevbank=False):
        try:
            mevzuat_bilgileri = []
            if search_gib or search_mevbank:
                mevzuat_bilgileri = self.mevzuat_scraper.search(
                    question,
                    search_gib=search_gib,
                    search_mevbank=search_mevbank
                )
            
            system_prompt = """Sen deneyimli bir Gelir İdaresi Başkanlığı (GİB) uzmanısın.
            
            Yanıtlarını şu formatta vermelisin:
            1. Her cevabı yeni bir satırda başlat
            2. Sadece sorulan sorunun cevabını ver
            3. Türkçe yanıt ver
            4. Maddeler halinde açıkla
            5. Varsa rakamları ve tarihleri belirt
            6. İlgili kanun maddelerini parantez içinde belirt"""
            
            # Mevzuat bilgilerini prompt'a ekle
            prompt = system_prompt + "\n\nSoru: " + question
            if mevzuat_bilgileri:
                prompt += "\n\nİlgili Mevzuat Bilgileri:\n" + "\n".join([
                    f"- {bilgi['baslik']}: {bilgi['icerik']}" 
                    for bilgi in mevzuat_bilgileri
                ])
            
            if self.model_provider == "huggingface":
                prompt = f"<s>[INST] {prompt}\n\nYanıtı maddeler halinde ve her maddeyi yeni satırda olacak şekilde ver: [/INST]</s>"
            elif self.model_provider == "openai":
                prompt = question
            else:
                prompt = prompt
            
            result = self._make_api_request(prompt)
            
            if isinstance(result, list) and len(result) > 0:
                result[0]['mevzuat'] = mevzuat_bilgileri
            
            return result
            
        except Exception as e:
            logging.error(f"get_answer hatası: {str(e)}")
            raise
    
    def analyze_file(self, file_content, file_type, question=None, search_gib=False, search_mevbank=False):
        try:
            if file_type == "pdf":
                content = self._extract_pdf_content(file_content)
            elif file_type == "xml":
                content = self._extract_xml_content(file_content)
            else:
                return {"error": "Desteklenmeyen dosya formatı"}
            
            mevzuat_bilgileri = []
            if search_gib or search_mevbank:
                search_text = question if question else content[:1000]  # Soru yoksa içeriğin ilk kısmını kullan
                mevzuat_bilgileri = self.mevzuat_scraper.search(
                    search_text,
                    search_gib=search_gib,
                    search_mevbank=search_mevbank
                )
            
            system_prompt = """Sen deneyimli bir Gelir İdaresi Başkanlığı (GİB) uzmanısın.
            
            Dosya analizini şu formatta yapmalısın:
            1. Her tespiti yeni bir satırda başlat
            2. Sadece dosya içeriği ile ilgili analiz yap
            3. Türkçe yanıt ver
            4. Maddeler halinde açıkla
            5. Varsa rakamları ve tarihleri belirt
            6. İlgili kanun maddelerini parantez içinde belirt"""
            
            # Mevzuat bilgilerini prompt'a ekle
            prompt = system_prompt + "\n\nDosya İçeriği:\n" + content
            if question:
                prompt += f"\n\nSoru: {question}"
            if mevzuat_bilgileri:
                prompt += "\n\nİlgili Mevzuat Bilgileri:\n" + "\n".join([
                    f"- {bilgi['baslik']}: {bilgi['icerik']}" 
                    for bilgi in mevzuat_bilgileri
                ])
            
            if self.model_provider == "huggingface":
                prompt = f"<s>[INST] {prompt}\n\nAnalizi maddeler halinde ve her maddeyi yeni satırda olacak şekilde ver: [/INST]</s>"
            elif self.model_provider == "openai":
                prompt = f"Dosya İçeriği:\n{content}\n\nSoru: {question}"
            else:
                prompt = prompt
            
            result = self._make_api_request(prompt)
            
            return {
                "success": True,
                "content": content,
                "analysis": result[0]['generated_text'] if result else "",
                "mevzuat": mevzuat_bilgileri
            }
            
        except Exception as e:
            logging.error(f"analyze_file hatası: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _extract_pdf_content(self, file_content):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logging.error(f"PDF okuma hatası: {str(e)}")
            raise
    
    def _extract_xml_content(self, file_content):
        try:
            root = etree.fromstring(file_content)
            return etree.tostring(root, pretty_print=True, encoding='unicode')
        except Exception as e:
            logging.error(f"XML okuma hatası: {str(e)}")
            raise
