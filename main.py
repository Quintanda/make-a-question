from fastapi import FastAPI, Request
from google import genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

@app.get("/responder")
def responder(question: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Você é um professor. Responda a seguinte solciitação de forma detalhada, completo, com exemplos e didática, inclua informações adicionais e não esqueça de nenhum aspecto relacionado a solicitação. Não escreva nada além do ensinamento. Faça o texto em Markdown: {question}")
    return {"resposta": response.text}
