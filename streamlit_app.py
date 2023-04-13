import streamlit as st
import speech_recognition as sr
import openai
import os

# Configurar las credenciales de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


# Configurar la página de Streamlit
st.set_page_config(page_title="Transcriptor de audio con Streamlit", page_icon=":microphone:", layout="wide")

# Configurar el título y la descripción
st.title("Transcriptor de audio en español")
st.markdown("""
Esta aplicación utiliza la librería de SpeechRecognition para transcribir audio en español durante dos minutos. Luego, utiliza el modelo text-davinci-002 de OpenAI para depurar el texto transcrito y ordenar las ideas.

Para utilizar la aplicación, haz clic en el botón "Iniciar grabación" y comienza a hablar o a reproducir un archivo de audio. Una vez que hayan pasado dos minutos, la transcripción se detendrá automáticamente y el texto transcrito se mostrará en la página.

**Nota:** Esta aplicación requiere una conexión a internet activa para poder utilizar el modelo de OpenAI.
""")

# Definir la función que transcribe el audio
def transcribir_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Comenzando a grabar...")
        audio = r.record(source, duration=120)
        st.write("Grabación finalizada.")
        st.write("Transcribiendo audio...")
        try:
            texto_transcrito = r.recognize_google(audio, language="es-ES")
            st.write("Texto transcrito:")
            st.write(texto_transcrito)
            return texto_transcrito
        except sr.UnknownValueError:
            st.error("No se pudo transcribir el audio.")
            return None

# Definir la función que depura el texto transcrito
def depurar_texto(texto_transcrito):
    st.write("Depurando texto...")
    prompt = f"Actúa como un secretario que transcribe y redacta en forma ordenada y precisa los pensamientos desordenados del usuario:\n\n{texto_transcrito}"
    modelo_openai = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7
    )
    texto_depurado = modelo_openai.choices[0].text
    st.write("Texto depurado:")
    st.write(texto_depurado)

# Agregar los botones para iniciar la grabación y depurar el texto
if st.button("Iniciar grabación"):
    texto_transcrito = transcribir_audio()
    if texto_transcrito is not None:
        depurar_texto(texto_transcrito)
