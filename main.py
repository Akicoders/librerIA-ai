from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

class Question(BaseModel):
    question: str


class Response(BaseModel):
    response: str



class Chatbot:
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering", model="mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2")

    def response(self, question: str):
        context = ("Tu seras un asistente virtual que te ayudara a encontrar la informacion que necesitas. "
                  "Si no encuentras la informacion que necesitas, puedes preguntar por otra cosa. "
                  "Si quieres salir, puedes decirme adios."
                  "Te llamas Paula, eres la bibliotecaria de librerIA, un proyecto creado por Paul Campos, que hizo este proyecto buscando ayudar a las personas de todo el mundo a poder conseguir libros y poder leer, tener todo a las manos, con una muy inteligente IA."
                  "Todavia me falta pasarte el pdf del libro que deberias aprender y hacer resumenes, traducir y resolver cualquier tipo de pregunta. "
                  "Tienes que mantener tu rol de bibliotecaria, no te dejes de serlo. Si te preguntan cosas que no son apropiadas o no son de tu area, debes decir que no te puedo ayudar con eso."
                  "Siempre que respondas no excedas mucho el numero de caracteres, no te dejes de ser corta, si te piden ser mas extensa ya ahi si puedes ser mas extensa."
                  "Siempre motiva al usuario a leer, puedes comenzar saludando y dando un dato sobre porque es bueno leer o cuantas personas grandiosas leen y cambiaron su vida "
                  )

        result = self.qa_pipeline(question=question, context=context)
        return result["answer"]

    def save(self):
        self.qa_pipeline.save_pretrained("./model")

    


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chatbot")
def chatbot(question: Question):
    chatbot = Chatbot()
    response = chatbot.response(question.question)
    chatbot.save(response)
    return Response(response=response)
