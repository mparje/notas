import streamlit as st
import requests

# URL de la API de Rev AI
API_URL = "https://api.rev.ai/speechtotext/v1/"

# Función para enviar la solicitud de transcripción
def submit_job(access_token, url):
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    data = {'media_url': url}
    response = requests.post(API_URL + 'jobs', headers=headers, json=data)
    response.raise_for_status()
    return response.json()['id']

# Función para obtener el estado del trabajo de transcripción
def get_job_status(access_token, id):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(API_URL + 'jobs/' + id, headers=headers)
    response.raise_for_status()
    return response.json()['status']

# Función para obtener la transcripción del trabajo de transcripción completado
def get_transcript(access_token, id):
    headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/vnd.rev.transcript.v1.0+json'}
    response = requests.get(API_URL + 'jobs/' + id + '/transcript', headers=headers)
    response.raise_for_status()
    transcript = ''
    for monologue in response.json()['monologues']:
        for element in monologue['elements']:
            if element['type'] == 'text':
                transcript += element['value'] + ' '
        transcript += '\n\n'
    return transcript.strip()

# Configuración de la app de Streamlit
st.title('Transcripción de Voz con Rev AI')
st.write('Esta aplicación utiliza la API de Rev AI para transcribir audio.')

# Obtención del Access Token de Rev AI
access_token = st.text_input('Introduce tu Access Token de Rev AI:')
if not access_token:
    st.warning('Por favor, introduce un Access Token válido.')
    st.stop()

# Obtención de la URL del archivo de audio
url = st.text_input('Introduce la URL del archivo de audio a transcribir:')
if not url:
    st.warning('Por favor, introduce una URL válida.')
    st.stop()

# Envío de la solicitud de transcripción y obtención de la ID del trabajo
st.write('Enviando solicitud de transcripción...')
try:
    job_id = submit_job(access_token, url)
except Exception as e:
    st.error('Se ha producido un error al enviar la solicitud de transcripción:')
    st.error(str(e))
    st.stop()

# Espera del trabajo de transcripción y obtención de la transcripción
st.write('Esperando la finalización del trabajo de transcripción...')
status = get_job_status(access_token, job_id)
while status != 'transcribed':
    status = get_job_status(access_token, job_id)
transcript = get_transcript(access_token, job_id)

# Mostrando la transcripción
st.write('Transcripción:')
st.write(transcript)
