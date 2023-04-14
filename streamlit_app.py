import os
import streamlit as st
import openai
import soundfile as sf

st.title("App de Speech to Text con OpenAI")

# Obtener la clave de la API de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

st.write("Cargue un archivo MP3 para transcribir:")

# Función que carga el archivo de audio seleccionado por el usuario
def load_audio():
    uploaded_file = st.file_uploader("Seleccione un archivo de audio", type=["mp3"])
    if uploaded_file is not None:
        filename = "audio_file.mp3"
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filename

filename = load_audio()

if filename:
    st.write("Transcribiendo texto...")

    # Leer el archivo MP3 y convertirlo a WAV para poder enviarlo a la API de OpenAI
    with open(filename, "rb") as f:
        audio_data = f.read()
    wav_data, sample_rate = sf.read(audio_data, dtype='float32')
    temp_file = "temp_audio_file.wav"
    sf.write(temp_file, wav_data, sample_rate)

    # Leer el archivo WAV convertido y enviarlo a la API de OpenAI para obtener la transcripción
    with open(temp_file, "rb") as f:
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
