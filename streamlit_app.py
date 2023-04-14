import streamlit as st
import requests
import os
import json

# Obtener la API key de OpenAI desde una variable de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")

# Función para enviar el archivo de audio a la API de Rev.ai y obtener la transcripción
def transcribe_audio(file):
    # URL de la API de Rev.ai
    url = "https://api.rev.ai/speechtotext/v1/jobs"

    # Configuración de la solicitud
    headers = {
        "Authorization": f"Bearer {rev_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "media": {
            "type": "audio",
            "content": file.read()
        },
        "metadata": "Transcription"
    }

    # Envío de la solicitud
    response = requests.post(url, headers=headers, json=data)

    # Obtener el ID del trabajo
    job_id = response.json()["id"]

    # Esperar a que el trabajo esté completo
    while True:
        url = f"https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript"
        headers = {"Authorization": f"Bearer {rev_api_key}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            break

    # Obtener la transcripción
    transcript = response.json()["monologues"][0]["elements"]

    # Convertir la transcripción en una sola cadena de texto
    text = " ".join([element["value"] for element in transcript])

    return text

# Función para ordenar el texto con OpenAI
def sort_text(text):
    # URL de la API de OpenAI
    url = "https://api.openai.com/v1/engines/text-davinci-003/completions"

    # Configuración de la solicitud
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "prompt": f"Ordena la siguiente lista:\n{text}\n1.",
        "temperature": 0.7,
        "max_tokens": 60,
        "n": 1,
        "stop": "\n"
    }

    # Envío de la solicitud
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Obtener el texto ordenado
    sorted_text = response.json()["choices"][0]["text"].strip()

    return sorted_text

# Configuración de la página de Streamlit
st.set_page_config(page_title="Transcripción de Audio", page_icon=":microphone:", layout="wide")

# Título y descripción
st.title("Transcripción de Audio y Ordenamiento de Texto")
st.markdown("Esta aplicación usa la API de Rev.ai para transcribir audio y la API de OpenAI para ordenar el texto transcrito.")

# Selección de archivo de audio
audio_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3", "wav"])

# Si se ha seleccionado un archivo
if audio_file is not None:
    # Transcribir el audio
    st.markdown("Transcribiendo audio...")
    text = transcribe_audio(audio_file)

    # Mostrar la transcripción
    st.markdown("## Transcripción")
    st.write(text)

    # Ordenar el texto
    st.markdown("Ordenando texto...")
    sorted_text = sort_text(text)

