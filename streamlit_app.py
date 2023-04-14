import streamlit as st
import os
import requests
import json

def transcribe_audio(audio_file, api_key):
    url = "https://api.amberscript.com/v1/trascription"
    headers = {
        "x-api-key": api_key
    }
    data = {
        "language": "es",
        "audio_url": "",
    }
    
    with open(audio_file, "rb") as file:
        response = requests.post(url, headers=headers, data=data, files={"audio_file": file})
    
    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json["text"]
    else:
        return "Error en la transcripción del archivo de audio."

st.set_page_config(page_title="Transcripción de audio", page_icon=":microphone:", layout="wide")

st.title("Transcripción de audio")

# Obtener el token de la API desde una variable de entorno
ACCESS_TOKEN = os.getenv("REVAI_ACCESS_TOKEN")

audio_file = st.file_uploader("Subir archivo de audio", type=["mp3", "wav"])
if audio_file is not None:
    result = transcribe_audio(audio_file, api_key)
    st.subheader("Texto transcrito:")
    st.write(result)
