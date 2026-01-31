import streamlit as st
import io
from pypdf import PdfReader
from generator import EditalGenerator
import os

st.set_page_config(page_title="Gerador de Editais TJMG", layout="wide")

def extract_text_from_files(uploaded_files):
    text = ""
    for file in uploaded_files:
        try:
            if file.type == "application/pdf":
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            else:
                # Assume text based
                stringio = io.StringIO(file.getvalue().decode("utf-8"))
                text += stringio.read() + "\n"
        except Exception as e:
            st.error(f"Erro ao ler arquivo {file.name}: {e}")
    return text

def main():
    st.title("🏛️ Gerador de Editais de Estágio - TJMG")
    st.markdown("Ferramenta de IA para elaboração de minutas de edital.")

    # Sidebar
    st.sidebar.header("Configurações")
    
    # API Key Handling
    api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Se não estiver no .env, insira aqui.")
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    st.sidebar.subheader("Base Normativa")
    uploaded_files = st.sidebar.file_uploader(
        "Upload de Modelos/Diretrizes (PDF/TXT)", 
        accept_multiple_files=True,
        type=['pdf', 'txt']
    )
    
    context_text = ""
    if uploaded_files:
        with st.spinner("Processando arquivos..."):
            context_text = extract_text_from_files(uploaded_files)
        st.sidebar.success(f"{len(uploaded_files)} arquivos carregados.")
        with st.sidebar.expander("Ver contexto extraído"):
            st.text(context_text[:500] + "...")

    # Main Form
    st.subheader("Parâmetros do Edital")
    
    col1, col2 = st.columns(2)
    
    with col1:
        comarca = st.text_input("Unidade / Comarca", placeholder="Ex: Comarca de Belo Horizonte")
        area = st.selectbox("Área de Formação", ["Direito", "Psicologia", "Serviço Social", "Administração", "Outra"])
        if area == "Outra":
            area = st.text_input("Especifique a Área")
        vagas = st.text_input("Número de Vagas", placeholder="Ex: 02 (duas) vagas + Cadastro de Reserva")
    
    with col2:
        bolsa = st.text_input("Valor da Bolsa", value="R$ 1.250,56")  # Valores de exemplo
        auxilio = st.text_input("Auxílio Transporte", value="R$ 176,00")
        carga_horaria = st.selectbox("Carga Horária", ["20 horas semanais", "25 horas semanais", "30 horas semanais"])
        supervisor = st.text_input("Supervisor/Responsável", placeholder="Nome e Cargo")

    extra_info = st.text_area("Outros Detalhes / Regras Específicas", placeholder="Ex: Prova será online; Data provável da inscrição...")

    if st.button("Gerar Minuta de Edital", type="primary"):
        if not api_key:
            st.error("Por favor, configure a chave de API do Gemini.")
            return

        params = {
            "comarca": comarca,
            "area": area,
            "vagas": vagas,
            "bolsa": bolsa,
            "auxilio": auxilio,
            "carga_horaria": carga_horaria,
            "supervisor": supervisor,
            "extra_info": extra_info
        }

        try:
            generator = EditalGenerator(api_key=api_key)
            with st.spinner("A IA está redigindo o edital... Aguarde."):
                result = generator.generate_edital(params, context_text)
            
            st.subheader("Minuta Gerada")
            st.markdown(result)
            
            st.download_button(
                label="📥 Baixar em Markdown",
                data=result,
                file_name=f"edital_{area}_{comarca}.md",
                mime="text/markdown"
            )
            
            # Future: Convert to DOCX here
            
        except Exception as e:
            st.error(f"Erro na geração: {e}")

if __name__ == "__main__":
    main()
