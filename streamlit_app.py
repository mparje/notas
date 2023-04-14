import streamlit as st
import requests
import pandas as pd
import os
import openai

# Definir la clave de la API de Rev.ai
rev_api_key = os.getenv("REV_API-KEY")
# Obtener la API key de OpenAI desde una variable de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")

# Función para transcribir audio usando la API de Rev.ai
def transcribe_audio(file):
    url = "https://api.rev.ai/speechtotext/v1/jobs"
    headers = {
        "Authorization": f"Bearer {os.getenv('REV_AI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "media_url": file,
        "metadata": "Test"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    job_id = response.json()["id"]
    
    url = f"https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript"
    headers = {
        "Authorization": f"Bearer {os.getenv('REV_AI_API_KEY')}"
    }
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "in_progress":
            continue
        elif data["status"] == "transcribed":
            return data["monologues"][0]["elements"]
        else:
            return None

# Función para ordenar texto usando la API de OpenAI
def sort_text(transcription):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Sort the following text in ascending order:\n\n{transcription}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Configuración de la aplicación de Streamlit
st.set_page_config(page_title="Transcripción y ordenamiento de audio", page_icon=":memo:", layout="wide")

st.title("Transcripción y ordenamiento de audio")

# Subida de archivo
uploaded_file = st.file_uploader("Subir archivo de audio", type=["mp3", "wav", "flac"])

if uploaded_file is not None:
    # Transcripción de audio usando la API de Rev.ai
    st.write("Transcribiendo audio...")
    elements = transcribe_audio(uploaded_file)
    transcription = " ".join([element["value"] for element in elements])
    
    # Ordenamiento de texto usando la API de OpenAI
    st.write("Ordenando texto...")
    sorted_text = sort_text(transcription)
    
    # Mostrar resultados
    st.write("Transcripción:")
    st.write(transcription)
    st.write("Texto ordenado:")
    st.write(sorted_text)


