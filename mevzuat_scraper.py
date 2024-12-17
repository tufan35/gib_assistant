import requests
from bs4 import BeautifulSoup
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class MevzuatScraper:
    def __init__(self):
        self.mevzuat_url = "https://www.mevzuat.gov.tr"
        self.resmigazete_url = "https://www.resmigazete.gov.tr"
        self.gib_url = "https://www.gib.gov.tr/mevzuat"
        self.mevbank_url = "https://www.mevbank.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        logging.info("Scraper initialized")

    def search_mevzuat(self, query, search_mevzuat=True, search_resmigazete=True):
        """Search both mevzuat.gov.tr and resmigazete.gov.tr based on user selection."""
        results = []
        
        try:
            if search_mevzuat:
                logging.info("Searching mevzuat.gov.tr")
                mevzuat_results = self._search_mevzuat_gov(query)
                results.extend(mevzuat_results)
            
            if search_resmigazete:
                logging.info("Searching resmigazete.gov.tr")
                resmigazete_results = self._search_resmigazete_gov(query)
                results.extend(resmigazete_results)
            
            logging.info(f"Found {len(results)} total results")
            return results
            
        except Exception as e:
            logging.error(f"Error during search: {e}")
            return []

    def search(self, query, search_gib=False, search_mevbank=False):
        """
        Verilen sorguya göre mevzuat araması yapar.
        
        Args:
            query (str): Arama sorgusu
            search_gib (bool): GİB mevzuatında arama yapılıp yapılmayacağı
            search_mevbank (bool): Mevbank'ta arama yapılıp yapılmayacağı
        
        Returns:
            list: Bulunan mevzuat bilgilerinin listesi
        """
        results = []
        
        try:
            if search_gib:
                gib_results = self._search_gib(query)
                results.extend(gib_results)
            
            if search_mevbank:
                mevbank_results = self._search_mevbank(query)
                results.extend(mevbank_results)
            
            return results
            
        except Exception as e:
            logging.error(f"Mevzuat arama hatası: {str(e)}")
            return []
    
    def _search_gib(self, query):
        """GİB mevzuatında arama yapar"""
        try:
            # GİB mevzuat araması implementasyonu
            results = []
            # TODO: GİB web sitesinden mevzuat arama fonksiyonunu implement et
            return results
        except Exception as e:
            logging.error(f"GİB arama hatası: {str(e)}")
            return []
    
    def _search_mevbank(self, query):
        """Mevbank'ta arama yapar"""
        try:
            # Mevbank araması implementasyonu
            results = []
            # TODO: Mevbank'tan mevzuat arama fonksiyonunu implement et
            return results
        except Exception as e:
            logging.error(f"Mevbank arama hatası: {str(e)}")
            return []

    def _search_mevzuat_gov(self, query):
        """Search on mevzuat.gov.tr"""
        try:
            search_url = f"{self.mevzuat_url}/arama.aspx"
            params = {'q': query}
            
            response = requests.get(search_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.select('.search-result'):
                title = result.select_one('.title')
                link = result.select_one('a')
                content = result.select_one('.content')
                date = result.select_one('.date')
                
                if title and link:
                    results.append({
                        'title': title.text.strip(),
                        'link': self.mevzuat_url + link['href'] if link['href'].startswith('/') else link['href'],
                        'content': content.text.strip() if content else '',
                        'date': date.text.strip() if date else '',
                        'source': 'mevzuat.gov.tr'
                    })
            
            logging.info(f"Found {len(results)} results from mevzuat.gov.tr")
            return results
            
        except Exception as e:
            logging.error(f"Error searching mevzuat.gov.tr: {e}")
            return []

    def _search_resmigazete_gov(self, query):
        """Search on resmigazete.gov.tr"""
        try:
            search_url = f"{self.resmigazete_url}/arama"
            params = {'q': query}
            
            response = requests.get(search_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.select('.gazette-result'):
                title = result.select_one('.title')
                link = result.select_one('a')
                content = result.select_one('.content')
                date = result.select_one('.date')
                
                if title and link:
                    results.append({
                        'title': title.text.strip(),
                        'link': self.resmigazete_url + link['href'] if link['href'].startswith('/') else link['href'],
                        'content': content.text.strip() if content else '',
                        'date': date.text.strip() if date else '',
                        'source': 'resmigazete.gov.tr'
                    })
            
            logging.info(f"Found {len(results)} results from resmigazete.gov.tr")
            return results
            
        except Exception as e:
            logging.error(f"Error searching resmigazete.gov.tr: {e}")
            return []

    def _get_content(self, url):
        """Get content from a specific URL"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.select_one('.content')
            
            return content.text.strip() if content else ""
            
        except Exception as e:
            logging.error(f"Error getting content from {url}: {e}")
            return ""
