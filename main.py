import os # <--- Adicione esta linha lá no topo, junto com os outros imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

# ... (resto do código igual) ...

# ==========================================
# CÉREBRO DA YUNA 
# ==========================================
# Agora o código vai buscar a chave de forma segura!
CHAVE_API_GEMINI = os.environ.get("GEMINI_API_KEY")

cliente_gemini = genai.Client(api_key=CHAVE_API_GEMINI)

# ... (resto do código continua igual até o final) ...

# Inicializa o app FastAPI
app = FastAPI(title="API da Yuna - Pegada Ecológica")

# Libera a conexão com o seu HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PerguntaUsuario(BaseModel):
    texto: str

# ==========================================
# CÉREBRO DA YUNA (Extraído do seu projeto)
# ==========================================
# Substitua pela mesma chave que está no seu st.secrets do Streamlit
CHAVE_API_GEMINI = os.environ.get("GEMINI_API_KEY")

# Inicializa o cliente do Gemini
cliente_gemini = genai.Client(api_key=CHAVE_API_GEMINI)

# A sua instrução personalizada (mantendo a essência intacta!)
instrucao_sistema = """
Você é a Yuna, uma IA especialista em sustentabilidade e meio ambiente criada por Yago.
Sua missão é ajudar com estudos, curiosidades e atividades ecológicas.
Use sempre um tom amigável.
"""

def gerar_resposta_yuna(pergunta: str):
    try:
        # Usando o mesmo modelo e configuração do seu Streamlit
        resposta = cliente_gemini.models.generate_content(
            model="gemini-2.5-flash", 
            contents=pergunta,
            config=types.GenerateContentConfig(
                system_instruction=instrucao_sistema,
                temperature=0.7
            )
        )
        return resposta.text
    except Exception as e:
        return f"Desculpe, meu sistema ambiental encontrou um erro: {e}"

# ==========================================
# ROTA DE COMUNICAÇÃO COM O SITE HTML
# ==========================================
@app.post("/api/chat")
async def conversar_com_yuna(pergunta: PerguntaUsuario):
    # Pega o texto do site, processa no Gemini e devolve
    resposta_ia = gerar_resposta_yuna(pergunta.texto)
    return {"resposta": resposta_ia}
