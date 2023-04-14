import streamlit as st
import requests
import os

API_URL = "https://api.openai.com/v1/audio/transcriptions"
API_KEY = os.getenv("OPENAI_API_KEY")

st.title("Transcripción de Notas de Voz con OpenAI Whisper")

audio_file = st.file_uploader("Carga tu archivo de audio", type=["wav", "mp3"])

if audio_file:
    audio_bytes = audio_file.read()

    if st.button("Transcribir"):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "multipart/form-data",
        }

        files = {"file": ("audio.mp3", audio_bytes)}

        data = {"model": "whisper-1"}

        response = requests.post(API_URL, headers=headers, data=data, files=files)

        if response.ok:
            resultado = response.json()["data"][0]["text"]
            st.write("Transcripción:")
            st.write(resultado)
        else:
            st.write("¡Ha ocurrido un error al transcribir la nota de voz!")
