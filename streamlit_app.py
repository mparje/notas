import streamlit as st
import openai
import os
import tempfile
import webrtc_audio

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribir_audio(audio):
    respuesta = openai.Completion.create(
        engine="davinci",
        audio=audio,
        prompt="Transcribe el siguiente audio a texto:",
        temperature=0.5,
        max_tokens=1024,
        n_greedy=1,
        stop=None,
    )

    return respuesta.choices[0].text

st.title("Transcripción de Notas de Voz en Vivo con OpenAI Whisper")

# Configuramos el stream de audio para capturar el audio del micrófono
stream_audio = webrtc_audio.AudioProcessor(
    on_recv=lambda data: audio_queue.put(data)
)

# Creamos una cola de audio para almacenar los fragmentos de audio capturados
audio_queue = webrtc_audio.QueueProcessor()

# Creamos una instancia de grabador de audio para grabar el audio capturado
recorder = webrtc_audio.Recorder(
    audio_processor=stream_audio,
    filename_template=tempfile.mktemp(prefix="streamlit-webrtc-", suffix=".webm"),
    file_format="webm",
)

# Creamos un botón para iniciar y detener la grabación de audio
if st.button("Iniciar/Detener Grabación"):
    recorder.start() if recorder.state == recorder.STATE_STOPPED else recorder.stop()

# Creamos un botón para transcribir el audio capturado
if st.button("Transcribir Audio"):
    audio = b"".join(list(audio_queue.queue))
    resultado = transcribir_audio(audio)
    st.write("Transcripción:")
    st.write(resultado)
