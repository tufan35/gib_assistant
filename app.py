import streamlit as st
import os
from ai_assistant import AIAssistant
import logging

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)

def initialize_session_state():
    if 'huggingface_token' not in st.session_state:
        st.session_state.huggingface_token = os.getenv('HUGGING_FACE_TOKEN', '')
    if 'anthropic_token' not in st.session_state:
        st.session_state.anthropic_token = os.getenv('ANTHROPIC_API_KEY', '')
    if 'openai_token' not in st.session_state:
        st.session_state.openai_token = os.getenv('OPENAI_API_KEY', '')
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'huggingface'
    if 'api_tokens_expanded' not in st.session_state:
        st.session_state.api_tokens_expanded = True

def save_token(token_name, token_value):
    if token_name in st.session_state:
        st.session_state[token_name] = token_value
        logging.info(f"{token_name} kaydedildi")
        return True
    return False

def main():
    st.set_page_config(
        page_title="GİB AI Asistan",
        page_icon="💼",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("GİB AI Asistan 💼")
    
    # Sidebar
    with st.sidebar:
        st.header("Ayarlar")
        
        with st.expander("API Token Ayarları", expanded=st.session_state.api_tokens_expanded):
            # HuggingFace Token
            huggingface_token = st.text_input(
                "HuggingFace Token",
                value=st.session_state.huggingface_token,
                type="password",
                key="huggingface_input"
            )
            if st.button("HuggingFace Token Kaydet"):
                if save_token('huggingface_token', huggingface_token):
                    st.success("HuggingFace token kaydedildi!")
                else:
                    st.error("Token kaydedilemedi!")
            
            # Anthropic Token
            anthropic_token = st.text_input(
                "Anthropic Token",
                value=st.session_state.anthropic_token,
                type="password",
                key="anthropic_input"
            )
            if st.button("Anthropic Token Kaydet"):
                if save_token('anthropic_token', anthropic_token):
                    st.success("Anthropic token kaydedildi!")
                else:
                    st.error("Token kaydedilemedi!")
            
            # OpenAI Token
            openai_token = st.text_input(
                "OpenAI Token",
                value=st.session_state.openai_token,
                type="password",
                key="openai_input"
            )
            if st.button("OpenAI Token Kaydet"):
                if save_token('openai_token', openai_token):
                    st.success("OpenAI token kaydedildi!")
                else:
                    st.error("Token kaydedilemedi!")
        
        # Model Seçimi
        st.subheader("Model Seçimi")
        model_option = st.selectbox(
            "AI Model",
            ["huggingface", "anthropic", "openai"],
            index=["huggingface", "anthropic", "openai"].index(st.session_state.selected_model)
        )
        
        if model_option != st.session_state.selected_model:
            st.session_state.selected_model = model_option
            st.experimental_rerun()
    
    # Token kontrolü ve uyarı mesajları
    token_warnings = {
        "huggingface": (st.session_state.huggingface_token, "HuggingFace"),
        "anthropic": (st.session_state.anthropic_token, "Anthropic"),
        "openai": (st.session_state.openai_token, "OpenAI")
    }
    
    selected_token, provider_name = token_warnings[st.session_state.selected_model]
    if not selected_token:
        st.warning(f"{provider_name} API token'ı eksik. Lütfen sidebar'dan token'ı girin.")
        return
    
    # Ana uygulama
    tabs = st.tabs(["Soru-Cevap", "Dosya Analizi"])
    
    with tabs[0]:
        st.subheader("Soru-Cevap")
        question = st.text_area("Sorunuzu yazın:", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            search_gib = st.checkbox("GİB Mevzuat'ta ara", value=False)
        with col2:
            search_mevbank = st.checkbox("Mevbank'ta ara", value=False)
        
        if st.button("Yanıtla", key="answer_button"):
            if question:
                try:
                    assistant = AIAssistant(
                        model_provider=st.session_state.selected_model,
                        api_token=selected_token
                    )
                    with st.spinner("Yanıt hazırlanıyor..."):
                        result = assistant.get_answer(question, search_gib=search_gib, search_mevbank=search_mevbank)
                        if result:
                            answer = result[0].get('generated_text', '').strip()
                            st.write(answer)
                            
                            # Mevzuat sonuçlarını göster
                            if hasattr(result[0], 'mevzuat') and result[0]['mevzuat']:
                                with st.expander("İlgili Mevzuat Bilgileri", expanded=True):
                                    for bilgi in result[0]['mevzuat']:
                                        st.markdown(f"**{bilgi['baslik']}**")
                                        st.write(bilgi['icerik'])
                                        st.markdown("---")
                        else:
                            st.error("Yanıt alınamadı. Lütfen tekrar deneyin.")
                except Exception as e:
                    logging.error(f"Hata: {str(e)}")
                    st.error(f"Bir hata oluştu: {str(e)}")
            else:
                st.warning("Lütfen bir soru girin.")
    
    with tabs[1]:
        st.subheader("Dosya Analizi")
        uploaded_file = st.file_uploader("PDF veya XML dosyası yükleyin:", type=['pdf', 'xml'])
        
        if uploaded_file:
            file_type = uploaded_file.type.split('/')[-1]
            file_content = uploaded_file.read()
            
            col1, col2 = st.columns(2)
            with col1:
                search_gib = st.checkbox("GİB Mevzuat'ta ara", value=False, key="file_gib")
            with col2:
                search_mevbank = st.checkbox("Mevbank'ta ara", value=False, key="file_mevbank")
            
            analysis_question = st.text_area(
                "Dosya hakkında spesifik bir soru sormak isterseniz yazın (opsiyonel):",
                height=100
            )
            
            if st.button("Analiz Et", key="analyze_button"):
                try:
                    assistant = AIAssistant(
                        model_provider=st.session_state.selected_model,
                        api_token=selected_token
                    )
                    with st.spinner("Dosya analiz ediliyor..."):
                        result = assistant.analyze_file(
                            file_content, 
                            file_type, 
                            analysis_question,
                            search_gib=search_gib,
                            search_mevbank=search_mevbank
                        )
                        
                        if result.get('success'):
                            with st.expander("Dosya İçeriği", expanded=False):
                                st.text(result['content'])
                            
                            st.subheader("Analiz Sonucu:")
                            st.write(result['analysis'])
                            
                            # Mevzuat sonuçlarını göster
                            if result.get('mevzuat'):
                                with st.expander("İlgili Mevzuat Bilgileri", expanded=True):
                                    for bilgi in result['mevzuat']:
                                        st.markdown(f"**{bilgi['baslik']}**")
                                        st.write(bilgi['icerik'])
                                        st.markdown("---")
                        else:
                            st.error(f"Analiz sırasında bir hata oluştu: {result.get('error')}")
                except Exception as e:
                    logging.error(f"Dosya analizi hatası: {str(e)}")
                    st.error(f"Dosya analizi sırasında bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
