from transformers import pipeline

class Chatbot:
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering")
        self.context = ""

    def save(self, response: str):
        self.context += response + "\n"

    def response(self, question: str):
        if not self.context:
            return "No tengo suficiente contexto. ¿Puedes darme más detalles?"
        result = self.qa_pipeline(question=question, context=self.context)
        return result["answer"]