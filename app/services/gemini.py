import base64
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

load_dotenv()

def generate(libro):
    gemini_api=os.getenv("API_KEY_GEMINI")
    client = genai.Client(api_key=gemini_api)
    text = "" 
    model = "gemini-2.0-flash-thinking-exp-01-21"

    prompt_data = {
        "libro": libro,
        "tarea": "Resumen y categoria",
        "formato": {
            "resumen": "Breve y animada (20-50 palabras)",
            "categoria": "Una sola"
        },
    }
    
    prompt_json = json.dumps(prompt_data, ensure_ascii=False)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_json),
                types.Part.from_text(text="Responde solo con un JSON que tenga las claves 'resumen' y 'categoria'. No incluyas texto adicional ni markdown.")
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=1024,
        response_mime_type="text/plain",
    )

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                text += chunk.text
    except Exception as e:
        return {"error": str(e)}
    
    try:
        # Clean up the response to extract just the JSON part
        text = text.strip()
        if "```json" in text:
            # Extract JSON from markdown code block
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            # Extract from generic code block
            text = text.split("```")[1].split("```")[0].strip()
            
        # Parse the JSON
        result_dict = json.loads(text)
        return result_dict
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "text": text}
    except Exception as e:
        return {"error": str(e)}
