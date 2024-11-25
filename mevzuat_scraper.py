import requests
from bs4 import BeautifulSoup
import re

class MevzuatScraper:
    def __init__(self):
        self.base_url = "https://www.gib.gov.tr"
        self.search_url = "https://www.gib.gov.tr/arama"
        
    def search_mevzuat(self, query):
        """Mevzuat sitesinde arama yapar ve ilgili sonuçları döndürür."""
        try:
            params = {
                'keys': query,
                'field_category_tid[]': '846',  # Mevzuat kategorisi
            }
            
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = []
            
            # Arama sonuçlarını bul
            results = soup.find_all('div', class_='views-row')
            
            for result in results:
                title_elem = result.find('a')
                if title_elem:
                    title = title_elem.text.strip()
                    link = self.base_url + title_elem['href']
                    
                    # İçeriği al
                    content = self._get_content(link)
                    
                    search_results.append({
                        'title': title,
                        'link': link,
                        'content': content
                    })
            
            return search_results
            
        except requests.RequestException as e:
            print(f"Arama sırasında hata oluştu: {e}")
            return []
    
    def _get_content(self, url):
        """Verilen URL'den içeriği çeker ve temizler."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ana içerik alanını bul
            content_div = soup.find('div', class_='field-item even')
            
            if content_div:
                # HTML etiketlerini temizle
                content = content_div.get_text(separator=' ', strip=True)
                # Fazla boşlukları temizle
                content = re.sub(r'\s+', ' ', content)
                return content
            
            return ""
            
        except requests.RequestException as e:
            print(f"İçerik çekilirken hata oluştu: {e}")
            return ""
