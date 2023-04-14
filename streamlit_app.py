import streamlit as st
import requests
import soundfile as sf
import io
import os
import streamlit_webrtc as webrtc

# Token de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modelo de transcripción de OpenAI
OPENAI_MODEL = "whisper-1"

# Título de la aplicación
st.title("Transcripción de audio con OpenAI")

# Configurar la captura de audio con streamlit-webrtc
webrtc_ctx = webrtc.Streamer(
    audio=True,
    video=False,
    desired_audio_format="wav",
    key="audio",
)

# Si se está capturando audio
if webrtc_ctx.audio_receiver:
    # Esperar a que se capture algún audio
    st.info("Habla para grabar un archivo de audio")

    # Iniciar la grabación
    webrtc_ctx.audio_receiver.start()

    # Esperar a que se capture suficiente audio
    st.info("Deja de hablar para detener la grabación")
    webrtc_ctx.audio_receiver.wait_for_frames(10)

    # Detener la grabación
    webrtc_ctx.audio_receiver.stop()

    # Obtener los datos de audio capturados
    audio_data = webrtc_ctx.audio_receiver.get_frames()

    # Guardar los datos de audio en un archivo temporal
    with io.BytesIO() as f:
        sf.write(f, audio_data, samplerate=44100)
        f.seek(0)

        # Encabezados de solicitud
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "multipart/form-data",
        }

        # Realizar la solicitud a la API de OpenAI
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            data={
                "file": ("audio.wav", f, "audio/wav"),
                "model": OPENAI_MODEL,
            },
        )

        # Obtener la transcripción del archivo de audio
        transcription = response.json()["data"][0]["text"]

        # Mostrar la transcripción
        st.write("Transcripción:")
        st.write(transcription)
