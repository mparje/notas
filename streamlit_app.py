import streamlit as st
import soundfile as sf
import deepspeech
import openai
import time
import os

# Cargamos el modelo de DeepSpeech en español
model_file_path = 'path/to/deepspeech-0.9.3-models.pbmm'
model = deepspeech.Model(model_file_path)
model.enableExternalScorer('path/to/deepspeech-0.9.3-models.scorer')

# Configuramos los parámetros de la API de OpenAI
openai.api_key = os.getenv("API_KEY")
model_engine = "text-davinci-003"

# Función para transcribir el archivo de audio
def transcribe_audio(file_path):
    audio, sample_rate = sf.read(file_path)
    audio_length = len(audio) * (1 / sample_rate)

    # Transcribimos el archivo con DeepSpeech
    text = model.stt(audio)
    return text

# Función para depurar el texto con OpenAI
def clean_text(text):
    prompt = "Actúa como un secretario que transcribe y redacta en forma ordenada y precisa los pensamientos desordenados del usuario:\n\n" + text
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=2048,
        n = 1,
        stop=None,
        timeout=20,
    )
    return response.choices[0].text.strip()

# Creamos la app de Streamlit
st.title("Transcripción y depuración de audio")

# Subimos el archivo de audio
audio_file = st.file_uploader("Sube un archivo de audio en formato WAV", type=["wav"])

if audio_file is not None:
    # Transcribimos el archivo de audio
    st.write("Transcribiendo archivo de audio...")
    with open("audio.wav", "wb") as f:
        f.write(audio_file.read())
    text = transcribe_audio("audio.wav")
    st.write("Texto transcritp: ")
    st.write(text)

    # Depuramos el texto con OpenAI
    st.write("Depurando el texto...")
    cleaned_text = clean_text(text)
    st.write("Texto depurado: ")
    st.write(cleaned_text)
else:
    st.write("Sube un archivo de audio para comenzar.")
