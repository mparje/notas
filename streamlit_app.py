import streamlit as st
from pydub import AudioSegment
import numpy as np
import openai
import os

# Configurar OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Función para detectar voz utilizando pydub
def detect_voice(audio_path):
    # Cargar el archivo de audio utilizando pydub
    audio = AudioSegment.from_file(audio_path, format="mp3")
    samples = np.array(audio.get_array_of_samples())
    
    # Calcular el nivel de energía de la señal de audio
    energy = np.abs(samples).mean()
    
    # Determinar si la señal de audio es voz o no
    is_voice = energy > 50  # ajustar este valor según sea necesario
    
    return is_voice

# Función para transcribir la voz utilizando OpenAI
def transcribe_audio(audio_path):
    # Detectar si hay voz en el archivo de audio
    is_voice = detect_voice(audio_path)
    
    if not is_voice:
        return ""
    
    # Transcribir la voz utilizando OpenAI
    with open(audio_path, "rb") as f:
        response = openai.api_request(
            "v1/audio/transcriptions",
            method="POST",
            files={"file": f},
            data={"model": "whisper-1"},
        )
        
    # Obtener el texto transrito
    transcription = response["data"][0]["text"]
    
    return transcription

# Configurar la página de Streamlit
st.title("Transcripción de voz a texto")

# Permitir que el usuario suba un archivo de audio
audio_file = st.file_uploader("Cargar archivo de audio", type=["mp3"])

# Transcribir la voz si se ha subido un archivo de audio
if audio_file is not None:
    # Guardar el archivo de audio en disco
    with open("audio.mp3", "wb") as f:
        f.write(audio_file.read())
    
    # Transcribir la voz utilizando OpenAI
    transcription = transcribe_audio("audio.mp3")
    
    # Mostrar el resultado de la transcripción
    st.write("Texto transcrito:")
    st.write(transcription)
