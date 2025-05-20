from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from pymongo import MongoClient
import os

# Configuração da API do Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Conexão com MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["make-a-question"]  # nome do banco
collection = db["questions"]  # nome da coleção

# Inicializando o app FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Você pode trocar "*" por um domínio específico depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de entrada (melhor que usar query param)
class Pergunta(BaseModel):
    question: str

@app.post("/responder")
def responder(pergunta: Pergunta):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "Você é um professor. Responda a seguinte solicitação de forma detalhada, "
        "completa, com exemplos e didática, inclua informações adicionais e não esqueça "
        "de nenhum aspecto relacionado à solicitação. Não escreva nada além do ensinamento. "
        "Faça o texto em Markdown:\n\n"
        f"{pergunta.question}"
    )

    response = model.generate_content(prompt)

    # Dados a serem inseridos no Mongo
    registro = {
        "pergunta": pergunta.question,
        "resposta": response.text
    }

    # Inserção no MongoDB
    result = collection.insert_one(registro)

    return {"mensagem": "Resposta salva com sucesso!", "id": str(result.inserted_id)}
