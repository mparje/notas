import streamlit as st
import requests
import json

# Define la función para obtener el token de acceso de Rev.ai
def get_access_token():
    # Coloca tu Client ID y Client Secret de Rev.ai aquí
    client_id = "tu_client_id"
    client_secret = "tu_client_secret"
    
    url = "https://api.rev.ai/oauth/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    access_token = response.json()['access_token']
    
    return access_token

# Define la función para enviar el archivo de audio a Rev.ai y obtener el ID de trabajo
def transcribe_audio(audio_file):
    url = "https://api.rev.ai/speechtotext/v1/jobs"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    
    data = {
        "media_url": audio_file,
        "metadata": "Streamlit Demo"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        job_id = response.json()["id"]
        return job_id
    else:
        st.error("Se produjo un error al enviar el archivo de audio a Rev.ai.")
        return None

# Define la función para obtener la transcripción a partir del ID de trabajo
def get_transcript(job_id):
    url = f"https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/vnd.rev.transcript.v1.0+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        transcript = response.json()
        return transcript
    else:
        st.error("Se produjo un error al obtener la transcripción de Rev.ai.")
        return None

# Define la aplicación de Streamlit
def app():
    st.set_page_config(page_title="Transcriptor de audio con Streamlit")
    
    st.title("Transcriptor de audio con Streamlit")
    
    audio_file = st.file_uploader("Cargar archivo de audio", type=["mp3", "wav", "m4a"])
    
    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        
        if st.button("Transcribir"):
            st.write("Transcribiendo...")
            job_id = transcribe_audio(audio_file)
            if job_id is not None:
                st.write("¡La transcripción está lista!")
                transcript = get_transcript(job_id)
                if transcript is not None:
                    for i in range(len(transcript["monologues"])):
                        speaker = transcript["monologues"][i]["speaker"]
                        text = transcript["monologues"][i]["elements"][0]["value"]
                        st.write(f"{speaker}: {text}")
            else:
                st.error("No se pudo iniciar la transcripción.")
    else:
        st.info("Cargue un archivo de audio para comenzar.")
        
if __name__ == "__main__":
    app()
