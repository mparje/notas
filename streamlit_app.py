import streamlit as st
import speech_recognition as sr
from tempfile import NamedTemporaryFile


def transcribir_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio_data, language="es-ES")
            return texto
        except sr.UnknownValueError:
            st.error("No se pudo entender el audio")
        except sr.RequestError as e:
            st.error(f"Error al solicitar resultados; {e}")


st.title("Transcriptor de notas de voz en español")

uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["wav", "mp3"])

if uploaded_file is not None:
    tfile = NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    st.audio(tfile.name, format="audio/wav")
    texto_transcrito = transcribir_audio(tfile.name)
    st.write("Texto transcrito:")
    st.write(texto_transcrito)
