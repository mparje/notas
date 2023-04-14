import os
import streamlit as st
import openai
import sounddevice as sd
import soundfile as sf

st.title("App de Speech to Text con OpenAI")

# Obtener la clave de la API de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

st.write("Haga clic en el botón para empezar a grabar:")

# Función que graba el audio del usuario y lo guarda en un archivo WAV
def record_audio():
    duration = 5  # Duración de la grabación en segundos
    fs = 44100  # Frecuencia de muestreo del audio
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    filename = "grabacion.wav"
    sf.write(filename, recording, fs)
    return filename

if st.button("Grabar"):
    filename = record_audio()
    st.write("Grabación finalizada. Transcribiendo texto...")
    
    # Leer el archivo WAV y enviarlo a la API de OpenAI para obtener la transcripción
    with open(filename, "rb") as f:
        audio_data = f.read()
    response = openai.Completion.create(
        engine="davinci",
        prompt="Transcribe the following audio:",
        audio=audio_data,
        max_tokens=1024,
        n_best=1,
        temperature=0,
    )
    
    # Mostrar la transcripción en la página
    transcription = response.choices[0].text.strip()
    st.write("Transcripción:")
    st.write(transcription)
