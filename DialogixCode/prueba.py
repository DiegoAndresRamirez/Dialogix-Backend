import speech_recognition as sr
import requests
import pyttsx3

# Clave API de Gemini
API_KEY = "AIzaSyA01S4Dy7yR-MNZptdQHkjqFb0Thkls0RA"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            print("Reconociendo...")
            text = recognizer.recognize_google(audio, language='es-ES')
            print(f"Texto reconocido: {text}")
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            return None
        except sr.RequestError as e:
            print(f"Error de solicitud a Google Speech Recognition; {e}")
            return None

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

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    conversation_history = []  # Lista para almacenar el historial de la conversación
    max_history_length = 5  # Número máximo de interacciones a mantener en el historial

    while True:  # Bucle para escuchar continuamente
        print("Di algo... (di 'salir' para terminar)")
        user_input = get_audio_input()
        
        if user_input:
            if "salir" in user_input.lower():  # Verifica si el usuario dijo "salir"
                print("Saliendo...")
                break
            
            # Agregar la entrada del usuario al historial
            conversation_history.append(f"Tú: {user_input}")

            # Limitar el tamaño del historial
            if len(conversation_history) > max_history_length:
                conversation_history.pop(0)  # Eliminar el mensaje más antiguo

            # Crear el prompt con el historial de conversación
            prompt = "Responde en español. Eres un profesor de inglés y estás hablando con una persona inexperta en el idioma. No necesito que respondas con ejemplos complicados; solo texto, sin caracteres especiales:\n"
            prompt += "\n".join(conversation_history) + "\nAsistente:"
            
            # Enviar a Gemini y obtener la respuesta
            response = send_to_gemini(prompt)
            
            if response:
                # Agregar la respuesta al historial
                conversation_history.append(f"Asistente: {response}")
                
                # Imprimir y hablar la respuesta
                print(f"Respuesta de Gemini: {response}")
                speak_text(response)

if __name__ == "__main__":
    main()
