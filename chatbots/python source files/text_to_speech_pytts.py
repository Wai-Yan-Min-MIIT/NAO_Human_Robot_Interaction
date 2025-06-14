# text_to_speech.py
import pyttsx3
import streamlit as st

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    
    engine.say(text)
    engine.runAndWait()

def speak_with_spinner(text):
    #st.spinner(None)  # Close the "Thinking..." spinner
    with st.spinner("Speaking..."):
        speak_text(text)
