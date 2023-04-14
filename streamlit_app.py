import streamlit as st
import requests
import os
import json
import openai

# Establecer las credenciales de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Definir la función para transcribir el audio usando Rev.ai
def transcribe_audio(audio_file):
    url = "https://api.rev.ai/speechtotext/v1/jobs"
    headers = {
        "Authorization": "Bearer " + os.getenv("REV_AI_API_KEY"),
        "Content-Type": "application/json",
    }
    data = {
        "media": {"type": "multipart/form-data", "data": audio_file},
        "metadata": "Testing",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    response_data = json.loads(response.text)
    job_id = response_data["id"]
    transcript = None
    while transcript is None:
        response = requests.get(
            f"https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript",
            headers=headers,
        )
        response.raise_for_status()
        response_data = json.loads(response.text)
        if response_data["status"] == "transcribed":
            transcript_url = response_data["links"]["self"]
            response = requests.get(transcript_url, headers=headers)
            response.raise_for_status()
            transcript_data = json.loads(response.text)
            transcript = transcript_data["monologues"][0]["elements"]
    return transcript


# Definir la función para ordenar el texto
def order_text(transcript):
    prompt = " ".join([elem["value"] for elem in transcript])
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message.strip()


# Definir la aplicación Streamlit
def app():
    st.set_page_config(page_title="Transcribir y ordenar texto de audio")
    st.title("Transcribir y ordenar texto de audio")

    # Subir el archivo de audio
    st.header("Subir archivo de audio")
    audio_file = st.file_uploader("Seleccionar archivo de audio", type=["mp3", "wav"])
    if audio_file is not None:
        st.success("Archivo cargado correctamente")

        # Transcribir el audio
        st.header("Transcribir audio")
        if st.button("Transcribir"):
            transcript = transcribe_audio(audio_file)
            st.write(transcript)

        # Ordenar el texto transcribido
        st.header("Ordenar texto transcribido")
        if st.button("Ordenar texto"):
            message = order_text(transcript)
            st.write(message)


if __name__ == "__main__":
    app()
