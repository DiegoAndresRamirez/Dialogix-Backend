import requests
from config import GEMINI_API_URL

def send_to_gemini(prompt_text):
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print("Respuesta de Gemini:", result)  # Imprimir la respuesta completa
        try:
            content = result['candidates'][0]['content']['parts'][0]['text']
            return content  # Devolver solo el texto de respuesta
        except (KeyError, IndexError):
            print("No se encontró la clave 'content' o 'text' en la respuesta.")
            return None
    else:
        print(f"Error al comunicarse con Gemini: {response.status_code}")
        return None
