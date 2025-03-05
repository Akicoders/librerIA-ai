import base64
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def generate(libro):
    client = genai.Client(
        api_key=os.getenv("API_KEY_GEMINI"),
    )
    text = ""
    model = "gemini-2.0-flash-thinking-exp-01-21"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"""Dame la siguiente información únicamente para el libro: {libro}. No escribas nada más que los datos. Sé preciso y al grano.

Autor:
Fecha de publicacion:
Categoria:
Descripcion corta del libro:
"""
                ),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        text += chunk.text
        print(chunk.text)
    return text
