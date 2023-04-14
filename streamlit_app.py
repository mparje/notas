import streamlit as st
import requests

# URL y clave de API de Rev.ai
API_URL = 'https://api.rev.ai/revspeech/v1beta/jobs'
API_KEY = '02l5R8_G98YSnNk_J5iQXhuVMMVo6cKcraDdGz-XrGRKGZUVlSO1PLmst2krtbrprwhZlLSsYhqK4jAhs8XIYQTUShtdY'



# Define la interfaz de usuario de la aplicación
st.title('Transcripción de Audio a Texto')
st.write('Esta aplicación utiliza la API de Rev.ai para transcribir archivos de audio a texto. Introduce la URL del archivo de audio que quieres transcribir:')

audio_url = st.text_input('URL del archivo de audio')

# Maneja el envío del formulario
if st.button('Transcribir'):
    # Configura los datos para enviar la solicitud POST a la API de Rev.ai
    headers = {'Authorization': f'Bearer {API_KEY}'}
    data = {
        'media_url': audio_url,
        'metadata': 'Transcripción de audio a texto',
        'callback_url': 'http://tu-URL-de-callback-aquí.com'
    }

    # Envía la solicitud POST a la API de Rev.ai
    response = requests.post(API_URL, headers=headers, json=data)

    # Maneja la respuesta de la API
    if response.status_code == 200:
        st.write('Se ha iniciado una nueva tarea de transcripción.')
        job_id = response.json()['id']
        st.write(f'ID de tarea: {job_id}')
    else:
        st.write('Se ha producido un error al enviar la solicitud.')
