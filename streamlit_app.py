import streamlit as st
import requests
import os

# Obtener el token de la API desde una variable de entorno
ACCESS_TOKEN = os.getenv("REVAI_ACCESS_TOKEN")

st.title("Transcripción de audio con Rev.ai")

# Agregar la opción para subir archivo
file = st.file_uploader("Seleccionar archivo de audio", type=["mp3", "wav"])

if file:
    # Configurar la solicitud
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "multipart/form-data"
    }

    # Enviar la solicitud para subir el archivo a Rev.ai
    response = requests.post("https://api.rev.ai/speechtotext/v1beta/sync", headers=headers, data=file.read())

    # Obtener el ID del trabajo de transcripción
    job_id = response.json()["id"]

    # Configurar la solicitud para obtener el resultado de la transcripción
    headers["Accept"] = "application/vnd.rev.transcript.v1.0+text"
    params = {"filter": "transcript"}

    # Esperar hasta que la transcripción esté lista
    while True:
        response = requests.get(f"https://api.rev.ai/speechtotext/v1beta/jobs/{job_id}", headers=headers, params=params)
        status = response.json()["status"]
        if status == "transcribed":
            break

    # Obtener el resultado de la transcripción y mostrarlo en la página
    transcript = response.json()["monologues"][0]["elements"]
    result = ""
    for element in transcript:
        result += element["value"]
    st.write("Texto transcrito:")
    st.write(result)
