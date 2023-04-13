import requests
import streamlit as st
import openai
import os

openai.api_key = os.getenv("YOUR_API_KEY")

# función para mejorar el texto generado
def mejorar_texto(texto_generado):
    # completar la oración del usuario para obtener un texto coherente
    prompt = "Completa la siguiente oración: \"" + texto_generado + "\" "
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=60,
      n=1,
      stop=None,
      timeout=15,
      )
    # obtener el texto mejorado generado por el modelo de lenguaje
    texto_mejorado = response.choices[0].text.strip()
    return texto_mejorado

# título de la aplicación
st.title('Transcripción y mejora de texto')

# obtener la URL del audio a transcribir
url_audio = st.text_input('Ingrese la URL del audio a transcribir:')

# transcribir el audio utilizando el servicio de reconocimiento de voz de Rev.ai
if st.button('Transcribir'):
    headers = {
        'Authorization': 'Bearer 02l5R8_G98YSnNk_J5iQXhuVMMVo6cKcraDdGz-XrGRKGZUVlSO1PLmst2krtbrprwhZlLSsYhqK4jAhs8XIYQTUShtdY',
        'Content-Type': 'application/json'
    }
    data = {
        'source_config': {
            'url': url_audio
        },
        'metadata': 'Audio de prueba'
    }
    response = requests.post('https://api.rev.ai/speechtotext/v1/jobs', headers=headers, json=data)

    if response.status_code == 200:
        # obtener el resultado de la transcripción del audio
        resultado = response.json()

        # obtener el texto generado por el servicio de reconocimiento de voz
        texto_generado = resultado['transcript']

        # mejorar el texto generado utilizando la función mejorado_texto()
        texto_mejorado = mejorar_texto(texto_generado)

        # mostrar el texto generado y el texto mejorado en la interfaz de usuario
        st.subheader('Texto generado:')
        st.write(texto_generado)
        st.subheader('Texto mejorado:')
        st.write(texto_mejorado)

    else:
        st.error('¡Ocurrió un error al obtener el resultado de la transcripción del audio!') 
