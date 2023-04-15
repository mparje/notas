import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write

# Configuración del stream de audio
samplerate = 44100
duration = 5

# Función para grabar audio
def record_audio():
    with st.spinner('Grabando...'):
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
        sd.wait()
    return audio

# Función para guardar audio grabado en un archivo WAV
def save_audio(audio, filename):
    write(filename, samplerate, audio)

# Aplicación de Streamlit
def main():
    st.title("Grabadora de Audio")

    # Botón para grabar audio
    if st.button("Grabar"):
        audio = record_audio()
        save_audio(audio, "grabacion.wav")
        st.success("¡Grabación exitosa!")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
