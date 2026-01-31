import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class EditalGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Please provide it in the sidebar or .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_edital(self, params, context_text=""):
        """
        Generates the edital draft based on parameters and optional context.
        """
        
        prompt = f"""
        Você é um assistente especializado do Tribunal de Justiça de Minas Gerais (TJMG).
        Sua tarefa é elaborar uma MINUTA DE EDITAL para seleção de estagiários.

        ### Contexto Normativo (Diretrizes/Modelos):
        {context_text if context_text else "Utilize o padrão geral de editais de estágio, com seções de Disposições Preliminares, Vagas, Inscrições, Provas, Classificação e Disposições Finais."}

        ### Parâmetros do Edital:
        - Unidade/Comarca: {params.get('comarca')}
        - Área de Formação: {params.get('area')}
        - Número de Vagas: {params.get('vagas')}
        - Valor da Bolsa: {params.get('bolsa')}
        - Auxílio Transporte: {params.get('auxilio')}
        - Carga Horária: {params.get('carga_horaria')}
        - Supervisor/Responsável: {params.get('supervisor')}
        - Outros Detalhes: {params.get('extra_info')}

        ### Instruções:
        1. Gere o documento completo, formatado em Markdown.
        2. Use linguagem formal e jurídica adequada.
        3. Certifique-se de preencher os campos com as informações fornecidas.
        4. Onde houver informações fáticas faltando (como datas específicas de prova), deixe lacunas (ex: [DATA]) ou [PREENCHER].
        5. Inclua um cabeçalho apropriado para o TJMG.

        Gero o texto da minuta abaixo:
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao gerar o edital: {str(e)}"
