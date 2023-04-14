import streamlit as st
import requests
import json


def transcribe_audio(audio_file):
    url = 'https://api.rev.ai/speechtotext/v1/jobs'
    headers = {
        'Authorization': f'Bearer {REVAI_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'media_url': audio_file,
        'metadata': 'Streamlit Testing'
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise ValueError(f'Request failed with error {response.status_code}, {response.text}')

    job_id = response.json()['id']
    st.write(f'Job ID: {job_id}')

    url = f'https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript'
    headers['Accept'] = 'application/vnd.rev.transcript.v1.0+json'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f'Request failed with error {response.status_code}, {response.text}')

    result = response.json()
    text = ''
    for monologue in result['monologues']:
        for element in monologue['elements']:
            if element['type'] == 'text':
                text += element['value'] + ' '
    return text.strip()


def sort_text(text):
    url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'prompt': text,
        'temperature': 0.5,
        'max_tokens': 60,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise ValueError(f'Request failed with error {response.status_code}, {response.text}')
    
    result = response.json()
    text = result['choices'][0]['text']
    return text.strip()


st.set_page_config(page_title='Transcriber App', page_icon=':memo:', layout='wide')
st.title('Transcriber App')

# Set your API keys here
REVAI_ACCESS_TOKEN = '<YOUR_REVAI_ACCESS_TOKEN>'
OPENAI_API_KEY = '<YOUR_OPENAI_API_KEY>'

audio_file = st.file_uploader('Upload audio file', type=['mp3', 'wav'])
if audio_file:
    transcript = transcribe_audio(audio_file)
    st.header('Transcript')
    st.write(transcript)

    if st.button('Sort Text'):
        sorted_text = sort_text(transcript)
        st.header('Sorted Text')
        st.write(sorted_text)
