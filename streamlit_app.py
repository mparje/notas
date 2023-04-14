import streamlit as st
import requests
import json
from io import BytesIO

st.set_page_config(page_title="Transcripción de audio", page_icon=":microphone:", layout="wide")

@st.cache(allow_output_mutation=True)
def get_bearer_token():
    url = 'https://api.rev.ai/oauth/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': '<YOUR_CLIENT_ID>',
        'client_secret': '<YOUR_CLIENT_SECRET>'
    }

    response = requests.post(url, headers=headers, data=data)
    response_json = json.loads(response.content)
    return response_json['access_token']

def transcribe_audio(audio_file):
    bearer_token = get_bearer_token()
    url = 'https://api.rev.ai/speechtotext/v1/jobs'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'media_url': 'https://www.rev.ai/FTC_Sample_1.mp3',
        'metadata': 'This is a test'
    }

    audio_bytes = audio_file.read()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception("Error en la solicitud de transcripción")
    response_json = json.loads(response.content)
    job_id = response_json['id']

    url = f'https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript'
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Error al obtener la transcripción")
        response_json = json.loads(response.content)
        status = response_json['status']
        if status == 'in_progress':
            st.text("Transcribiendo...")
        elif status == 'failed':
            st.text("La transcripción ha fallado")
            break
        elif status == 'completed':
            transcript_text = ""
            for i in response_json['monologues']:
                for j in i['elements']:
                    transcript_text += j['value'] + " "
            return transcript_text.strip()

def main():
    st.title("Transcripción de audio")
    st.markdown("---")

    uploaded_file = st.file_uploader("Sube un archivo de audio (mp3, wav, m4a)")

    if uploaded_file is not None:
        transcript = transcribe_audio(uploaded_file)
        st.markdown(f"**Transcripción:** {transcript}")

if __name__ == '__main__':
    main()
