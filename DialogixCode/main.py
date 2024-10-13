from speech_to_text import get_audio_input
from send_to_gemini import send_to_gemini
from text_to_speech import speak_text
from config import GEMINI_API_URL

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

