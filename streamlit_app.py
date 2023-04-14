import streamlit as st
import requests
import soundfile as sf
import io
import os

# Token de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modelo de transcripción de OpenAI
OPENAI_MODEL = "whisper-1"

# Título de la aplicación
st.title("Transcripción de audio con OpenAI")

# Archivo de audio para subir
uploaded_file = st.file_uploader("Selecciona un archivo de audio MP3", type="mp3")

# Si se ha subido un archivo
if uploaded_file is not None:
    # Leer el archivo de audio en memoria
    audio_data, sample_rate = sf.read(io.BytesIO(uploaded_file.read()), dtype='float32', channels=1)

    # Encabezados de solicitud
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "multipart/form-data",
    }

    # Realizar la solicitud a la API de OpenAI
    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers=headers,
        data={
            "file": ("audio.mp3", io.BytesIO(uploaded_file.read()), "audio/mp3"),
            "model": OPENAI_MODEL,
        },
    )

    # Obtener la transcripción del archivo de audio
    transcription = response.json()["data"][0]["text"]

    # Mostrar la transcripción
    st.write("Transcripción:")
    st.write(transcription)
