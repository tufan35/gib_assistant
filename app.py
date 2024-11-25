import streamlit as st
from mevzuat_scraper import MevzuatScraper
from ai_assistant import AIAssistant

# Sayfa yapılandırması
st.set_page_config(
    page_title="GİB Mevzuat Yardımcısı",
    page_icon="📚",
    layout="wide"
)

# Başlık ve açıklama
st.title("📚 GİB Mevzuat Yardımcısı")
st.markdown("""
Bu uygulama, Gelir İdaresi Başkanlığı mevzuatları hakkında sorularınızı yanıtlamak için yapay zeka teknolojisini kullanır.
* Sorunuzu Türkçe olarak girin
* Sistem ilgili mevzuatı tarayacak
* Yapay zeka en uygun cevabı oluşturacak
""")

# Singleton sınıfları oluştur
@st.cache_resource
def load_ai_assistant():
    return AIAssistant()

@st.cache_resource
def load_scraper():
    return MevzuatScraper()

# Asistanları yükle
ai_assistant = load_ai_assistant()
scraper = load_scraper()

# Kullanıcı sorusu
user_question = st.text_input("Sorunuzu buraya yazın (Örnek: KDV1 beyannamesi nasıl hazırlanır?)")

if user_question:
    with st.spinner("Mevzuat araştırılıyor..."):
        # Mevzuatta ara
        search_results = scraper.search_mevzuat(user_question)
        
        if not search_results:
            st.error("Üzgünüm, bu konuyla ilgili mevzuat bulunamadı.")
        else:
            # En iyi cevabı bul
            with st.spinner("Cevap hazırlanıyor..."):
                answer = ai_assistant.get_best_answer(user_question, search_results)
                
                # Cevabı göster
                st.success("Cevap bulundu!")
                
                # Ana cevap
                st.markdown("### Cevap")
                st.write(answer['answer'])
                
                # Güven skoru
                confidence_percentage = round(answer['confidence'] * 100, 2)
                st.progress(answer['confidence'])
                st.caption(f"Güven Skoru: %{confidence_percentage}")
                
                # Kaynak bilgisi
                if answer['source'] and answer['link']:
                    st.markdown("### Kaynak")
                    st.markdown(f"[{answer['source']}]({answer['link']})")
                    
                # Tüm sonuçları göster
                with st.expander("Tüm Arama Sonuçları"):
                    for idx, result in enumerate(search_results, 1):
                        st.markdown(f"**{idx}. {result['title']}**")
                        st.markdown(f"[Bağlantı]({result['link']})")
                        st.markdown("---")
