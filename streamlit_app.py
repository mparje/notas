import streamlit as st
import speech_recognition as sr
import openai
import os

openai.api_key = os.getenv("api_key")

# Función para transcribir el audio
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

# Función para mejorar el texto utilizando GPT-3
def mejorar_texto(texto):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=(f"Mejora el siguiente texto:\n{texto}\n\n"),
      temperature=0.5,
      max_tokens=150,
      n = 1,
      stop=None,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].text.strip()

# Interfaz de usuario con Streamlit
st.title("Transcriptor de notas de voz en español")

uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    texto_transcrito = transcribir_audio(uploaded_file)
    st.write("Texto transcrito:")
    st.write(texto_transcrito)
    texto_mejorado = mejorar_texto(texto_transcrito)
    st.write("Texto mejorado:")
    st.write(texto_mejorado)
