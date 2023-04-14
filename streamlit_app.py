import streamlit as st
import requests
import os

# Ruta de la API y URL para subir el archivo de audio
API_URL = "https://api.rev.ai/speechtotext/v1/jobs"
UPLOAD_URL = "https://www.rev.ai/FTC_Sample_1.mp3"

# Obtener el token de la API desde una variable de entorno
ACCESS_TOKEN = os.getenv("REVAI_ACCESS_TOKEN")

# Configuración de la aplicación de Streamlit
st.title("Transcriptor de audio con Rev AI")
st.write("Sube un archivo de audio para transcribirlo:")

# Subir archivo de audio
audio_file = st.file_uploader("Archivo de audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    # Configurar el encabezado para la solicitud de la API
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

    # Crear la carga útil para la solicitud de la API
    payload = {"source_config": {"url": UPLOAD_URL}, "metadata": "Transcripción de audio"}

    # Enviar la solicitud POST a la API para iniciar el trabajo de transcripción
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    # Extraer el ID del trabajo de transcripción de la respuesta JSON
    job_id = response.json()["id"]

    # Esperar a que el trabajo de transcripción se complete
    status = "in_progress"
    while status == "in_progress":
        response = requests.get(f"{API_URL}/{job_id}", headers=headers)
        response.raise_for_status()
        status = response.json()["status"]
        st.write(f"Estado del trabajo de transcripción: {status}")
    
    # Descargar la transcripción en formato JSON
    response = requests.get(f"{API_URL}/{job_id}/transcript", headers=headers, 
                            params={"speaker_labels": True, "timestamps": True})
    response.raise_for_status()

    # Imprimir la transcripción
    transcript = response.json()
    st.write(transcript)
