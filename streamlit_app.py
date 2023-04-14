import streamlit as st
import requests
import json

# Función para transcribir audio
def transcribe_audio(audio_file):
    # URL de la API de Rev.ai
    url = "https://api.rev.ai/speechtotext/v1/jobs"
    # Token de acceso de Rev.ai
    access_token = "<REVAI_ACCESS_TOKEN>"
    # Encabezados de la solicitud POST
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Configuración de la fuente de audio
    source_config = {"url": audio_file}
    # Metadatos adicionales para la transcripción (opcional)
    metadata = "This is a test"
    # Datos para la solicitud POST
    data = {"source_config": source_config, "metadata": metadata}
    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Obtener el ID del trabajo de transcripción
    job_id = response.json()["id"]
    # URL de la API para verificar el estado del trabajo
    status_url = f"{url}/{job_id}/transcript"
    # Encabezados de la solicitud GET
    headers = {"Authorization": f"Bearer {access_token}"}
    # Esperar hasta que la transcripción esté completa
    while True:
        # Realizar la solicitud GET para obtener el estado del trabajo
        status_response = requests.get(status_url, headers=headers)
        # Obtener el estado actual del trabajo de transcripción
        status = status_response.json()["status"]
        # Si el estado es "in_progress", esperar 5 segundos y volver a intentar
        if status == "in_progress":
            time.sleep(5)
            continue
        # Si el estado es "completed", obtener el texto transcrito y salir del ciclo
        elif status == "completed":
            transcript_text = status_response.json()["monologues"][0]["elements"]
            transcript = " ".join([elem["value"] for elem in transcript_text])
            return transcript
        # Si el estado es diferente de "in_progress" o "completed", mostrar un mensaje de error y salir del ciclo
        else:
            st.error(f"Error al transcribir audio: estado del trabajo: {status}")
            return None

# Función principal de la aplicación Streamlit
def app():
    # Título de la aplicación
    st.title("Transcriptor de Audio con Rev.ai")
    # Selector de archivo de audio
    audio_file = st.file_uploader("Seleccione un archivo de audio", type=["mp3", "wav", "m4a"])
    # Botón para iniciar la transcripción
    if st.button("Transcribir"):
        if audio_file is not None:
            # Transcribir el archivo de audio seleccionado
            transcript = transcribe_audio(audio_file)
            if transcript is not None:
                # Mostrar el resultado de la transcripción
                st.write("Transcripción:")
                st.write(transcript)
        else:
            st.error("Seleccione un archivo de audio primero.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
