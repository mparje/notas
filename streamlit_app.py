import streamlit as st
import speech_recognition as sr
import openai
import os

# Configura las credenciales de autenticación para la API de GPT
openai.api_key = os.getenv("API_KEY")

# Configura el título de la aplicación
st.title("Transcripción y depuración de audio")

# Permite al usuario subir un archivo de audio
archivo = st.file_uploader("Sube un archivo de audio en formato WAV o FLAC", type=["wav", "flac"])

if archivo:
    # Crea un objeto de reconocimiento de voz
    r = sr.Recognizer()

    # Lee el audio desde el archivo
    audio = sr.AudioFile(archivo)
    with audio as source:
        audio_data = r.record(source)

    # Transcribe el audio utilizando la API de reconocimiento de voz de Google
    texto = r.recognize_google(audio_data, language='es-ES')

    # Depura el texto transrito utilizando GPT
    prompt = "Actúa como un secretario que transcribe y redacta en forma ordenada y precisa los pensamientos desordenados del usuario:\n\n" + texto
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    texto_dep = respuesta.choices[0].text.strip()

    # Muestra el texto transcrito y depurado en la aplicación
    st.write("Texto transcrito:")
    st.write(texto)
    st.write("Texto depurado:")
    st.write(texto_dep)
