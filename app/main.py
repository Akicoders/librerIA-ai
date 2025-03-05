from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
from app.routes.chatbot import Chatbot
from app.routes.books import router as books_router

class Question(BaseModel):
    question: str

class Response(BaseModel):
    response: str

class Context(BaseModel):
    name: str
    book: str
    author: str

chatbot = Chatbot()

app = FastAPI()
app.include_router(books_router)

@app.post("/say_hello")
def say_hello(context: Context):
    chatbot.context = f"El usuario se llama {context.name}. Quiere leer el libro '{context.book}' de {context.author}."
    response = chatbot.response("Saluda al usuario. Dile que estás listo para empezar.")
    chatbot.save(f"Saludo inicial: {response}")
    return Response(response=response)

@app.post("/chatbot")
def chat(question: Question):
    response = chatbot.response(question.question)
    chatbot.save(f"Pregunta: {question.question}\nRespuesta: {response}")
    return Response(response=response)
