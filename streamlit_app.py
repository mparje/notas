import requests
import streamlit as st

# Configurar la URL y la clave de API de Rev.ai
url = "https://api.rev.ai/speechtotext/v1/jobs"
headers = {
    "Authorization": "Bearer 02l5R8_G98YSnNk_J5iQXhuVMMVo6cKcraDdGz-XrGRKGZUVlSO1PLmst2krtbrprwhZlLSsYhqK4jAhs8XIYQTUShtdY",
    "Content-Type": "application/json"
}

# Definir la interfaz de usuario de la aplicación
st.title("Transcripción de Audio a Texto")
st.write("Esta aplicación utiliza la API de Rev.ai para transcribir archivos de audio a texto. Introduce la URL del archivo de audio que quieres transcribir:")

audio_url = st.text_input("URL del archivo de audio")

# Manejar el envío del formulario
if st.button("Transcribir"):
    # Configurar los datos para enviar la solicitud POST a la API de Rev.ai
    data = {
        "source_config": {
            "url": audio_url
        },
        "metadata": "Transcripción de audio a texto"
    }

    # Enviar la solicitud POST a la API de Rev.ai
    response = requests.post(url, headers=headers, json=data)

    # Manejar la respuesta de la API
    if response.status_code == 200:
        job_id = response.json()["id"]
        st.write("Se ha iniciado una nueva tarea de transcripción con ID:", job_id)
    else:
        st.write("Se ha producido un error al enviar la solicitud. Código de estado:", response.status_code)
