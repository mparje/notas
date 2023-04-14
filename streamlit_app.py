import streamlit as st
import requests
import json
import os
import time

# Función para enviar el archivo de audio a la API de Rev.ai
def transcribe_audio(audio_file):
    url = 'https://api.rev.ai/speechtotext/v1/jobs'
    headers = {
        'Authorization': f'Bearer {os.environ["REVAI_ACCESS_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps({
        'media_url': audio_file,
        'metadata': 'Streamlit Testing'
    }))
    job_id = response.json()['id']
    status = None
    while status != 'transcribed':
        status_url = f'https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript'
        headers['Accept'] = 'application/vnd.rev.transcript.v1.0+json'
        response = requests.get(status_url, headers=headers)
        status = response.json()['status']
        time.sleep(1)
    transcript_url = f'https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript'
    headers['Accept'] = 'application/vnd.rev.transcript.v1.0+json'
    response = requests.get(transcript_url, headers=headers)
    return response.json()


# Función para ordenar el texto con la API de OpenAI
def sort_text(text):
    url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}'
    }
    data = {
        'prompt': text,
        'temperature': 0.5,
        'max_tokens': 50,
        'top_p': 1.0,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['text']


# Interfaz de usuario
def app():
    st.title("Transcriptor de audio")
    audio_file = st.file_uploader("Sube un archivo de audio", type=["mp3"])
    if audio_file:
        st.audio(audio_file, format='audio/mp3')
        transcript = transcribe_audio(audio_file)
        text = ''
        for monologue in transcript['monologues']:
            for element in monologue['elements']:
                if element['type'] == 'text':
                    text += element['value'] + ' '
        st.subheader("Texto transcrito:")
        st.write(text)
        sorted_text = sort_text(text)
        st.subheader("Texto ordenado:")
        st.write(sorted_text)

if __name__ == '__main__':
    app()
