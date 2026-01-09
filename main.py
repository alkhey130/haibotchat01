from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from app.email_service import send_email
import os

app = FastAPI()

# 🌍 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Clé API Groq (METTRE DANS .env PLUS TARD)
client = Groq(api_key="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")

# =======================
# 🤖 CHATBOT
# =======================

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": req.message}
            ]
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}

# =======================
# 📩 FORMULAIRE CONTACT
# =======================

class ContactRequest(BaseModel):
    name: str
    email: str
    service: str
    message: str

@app.post("/contact")
def contact(req: ContactRequest):
    try:
        send_email(
            name=req.name,
            email=req.email,
            service=req.service,
            message=req.message
        )
        return {"status": "Message envoyé avec succès"}
    except Exception as e:
        return {"error": str(e)}
