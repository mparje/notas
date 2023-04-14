import base64
import json
import os
import requests
import srtreamlit as st
import openai

# Definir la clave de la API de Rev.ai
rev_api_key = '02l5R8_G98YSnNk_J5iQXhuVMMVo6cKcraDdGz-XrGRKGZUVlSO1PLmst2krtbrprwhZlLSsYhqK4jAhs8XIYQTUShtdY'

# Obtener la API key de OpenAI desde una variable de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio(file):
    # Leer los datos de audio desde el archivo
    with open(file, "rb") as f:
        audio_data = f.read()

    # Convertir los datos de audio a una cadena codificada en base64
    audio_b64 = base64.b64encode(audio_data).decode()

    # Configurar la URL de la API y los headers
    url = "https://api.rev.ai/speechtotext/v1/jobs"
    headers = {
        "Authorization": f"Bearer {os.getenv('REV_AI_API_KEY')}",
        "Content-Type": "application/json"
    }

    # Configurar los parámetros de la solicitud
    data = {
        "media": {
            "type": "audio",
            "content": audio_b64
        },
        "metadata": "Test"
    }

    # Hacer la solicitud a la API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Leer la respuesta de la API y obtener el ID del trabajo de transcripción
    response_data = json.loads(response.content)
    job_id = response_data["id"]

    # Esperar hasta que el trabajo de transcripción esté completo
    while True:
        response = requests.get(f"{url}/{job_id}", headers=headers)
        response_data = json.loads(response.content)
        status = response_data["status"]
        if status == "transcribed":
            break
        elif status == "failed":
            raise Exception("La transcripción falló")

        time.sleep(1)

    # Obtener el texto transcrito
    transcript = response_data["monologues"][0]["elements"]
    text = " ".join([element["value"] for element in transcript])

    # Ordenar el texto usando el modelo text-davinci-002
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    sorted_text = response.choices[0].text.strip()

    # Devolver el texto transcrito y ordenado
    return sorted_text


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
