import streamlit as st
from ai_assistant import AIAssistant
from mevzuat_scraper import MevzuatScraper
import logging

def main():
    st.title("Mevzuat ve Vergi Asistanı")
    
    # Sidebar bilgileri
    st.sidebar.title("Hakkında")
    st.sidebar.info(
        "Bu yapay zeka asistanı, Türk vergi ve mevzuat sorularınıza yardımcı olur. "
        "Yapay zeka bilgi tabanını kullanarak cevaplar verir ve resmi "
        "Türk devlet sitelerinden güncel bilgileri arayabilir."
    )
    
    # Log görüntüleyici
    with st.sidebar.expander("Logları Görüntüle", expanded=False):
        try:
            with open('ai_assistant.log', 'r') as log_file:
                logs = log_file.read()
                st.code(logs)
        except FileNotFoundError:
            st.warning("Henüz log dosyası oluşturulmamış.")
    
    # Asistanları başlat
    @st.cache_resource
    def load_assistants():
        return AIAssistant(), MevzuatScraper()
    
    ai_assistant, scraper = load_assistants()
    
    # Kullanıcı girişi
    user_question = st.text_input(
        "Sorunuzu yazın:",
        placeholder="Örnek: KDV oranları nelerdir?"
    )
    
    # Arama seçenekleri
    search_options = st.columns(2)
    with search_options[0]:
        search_mevzuat = st.checkbox("mevzuat.gov.tr'de ara", value=False)
    with search_options[1]:
        search_resmigazete = st.checkbox("resmigazete.gov.tr'de ara", value=False)
    
    if user_question:
        # Yapay zeka cevabını al
        with st.spinner("Yapay zeka cevabı hazırlanıyor..."):
            quick_answer = ai_assistant.get_quick_answer(user_question)
            
            # Cevabı göster
            st.write("### Yapay Zeka Cevabı:")
            st.write(quick_answer['answer'])
            
            # Eğer kullanıcı resmi kaynaklarda arama yapmak istiyorsa
            if search_mevzuat or search_resmigazete:
                st.info("Resmi kaynaklarda güncel bilgi aranıyor...")
                
                with st.spinner("Mevzuat araması yapılıyor..."):
                    # Kullanıcı seçimine göre arama yap
                    search_results = scraper.search_mevzuat(
                        user_question,
                        search_mevzuat=search_mevzuat,
                        search_resmigazete=search_resmigazete
                    )
                    
                    if not search_results:
                        st.warning("Seçilen kaynaklarda ilgili mevzuat bulunamadı.")
                    else:
                        with st.spinner("Güncel bilgiler analiz ediliyor..."):
                            # Güncel bilgilerle cevap oluştur
                            updated_answer = ai_assistant.get_best_answer(user_question, search_results)
                            
                            st.write("### Güncel Mevzuat Bilgisi:")
                            st.write(updated_answer['answer'])
                            
                            # Kaynak bilgilerini göster
                            if updated_answer['source'] and updated_answer['link']:
                                st.info(f"Kaynak: {updated_answer['source']}")
                                st.markdown(f"[Detaylı bilgi için tıklayın]({updated_answer['link']})")
                                
                                if updated_answer['date']:
                                    st.text(f"Yayın tarihi: {updated_answer['date']}")
                            
                            # Güven skorunu göster
                            if 'confidence' in updated_answer:
                                st.progress(updated_answer['confidence'])
                                st.caption(f"Güven skoru: {updated_answer['confidence']:.2%}")
                            
                            # Tüm sonuçları göster
                            with st.expander("Tüm arama sonuçlarını görüntüle"):
                                for idx, result in enumerate(search_results, 1):
                                    st.markdown(f"### {idx}. {result['title']}")
                                    st.markdown(f"Kaynak: {result['source']}")
                                    if result.get('date'):
                                        st.markdown(f"Tarih: {result['date']}")
                                    st.markdown(f"[Bağlantı]({result['link']})")
                                    st.markdown("---")

if __name__ == "__main__":
    main()
