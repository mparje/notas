import streamlit as st
import speech_recognition as sr
import openai
import os

# Configure la API de OpenAI con su clave secreta
openai.api_key = os.getenv("YOUR_API_KEY")

st.set_page_config(page_title="Transcripción y depuración de audio", page_icon=":microphone:", layout="wide")

st.title("Transcripción y depuración de audio")

# Cargar archivo de audio
audio_file = st.file_uploader("Cargar archivo de audio", type=["wav", "mp3"])

if audio_file:
    # Convertir el archivo de audio a texto utilizando la biblioteca SpeechRecognition
    r = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)
    with audio_data as audio:
        audio_text = r.record(audio)
        transcript = r.recognize_google(audio_text, language="es-ES")
        
    # Mostrar el texto transcrito
    st.header("Texto transcrito")
    st.write(transcript)

    # Depurar el texto utilizando la API de OpenAI
    st.header("Texto depurado")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Actúa como un secretario que transcribe y redacta en forma ordenada y precisa los pensamientos desordenados del usuario:\n{transcript}",
        temperature=0.7,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    edited_text = response.choices[0].text
    st.write(edited_text)
