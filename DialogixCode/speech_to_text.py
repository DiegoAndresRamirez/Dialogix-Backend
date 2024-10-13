import speech_recognition as sr

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
