# uni_bot_model.py
import os
import streamlit as st
import json
import random
import joblib
from tts_client import send_message_to_nao  # Import the function
from text_to_speech_pytts import speak_with_spinner

# Load the trained model, vectorizer, label encoder, and responses
model = joblib.load('chatbot_model_version2.pkl')
vectorizer = joblib.load('vectorizer_version2.pkl')
label_encoder = joblib.load('label_encoder_version2.pkl')
with open('responses_version2.json', 'r') as f:
    responses = json.load(f)

# Function to get response from the custom dataset chatbot
def get_custom_response(user_input):
    user_input_vectorized = vectorizer.transform([user_input])
    print(f"user_input_vectorized: {user_input_vectorized}")
    prediction = model.predict(user_input_vectorized)
    print(f"prediction: {prediction}")
    tag = label_encoder.inverse_transform(prediction)[0]
    print(f"tag: {tag}")
    response = random.choice(responses[tag])
    return response

# Function to handle University Chatbot interface
def uni_bot_interface():
    st.title("University Chat Application")

    # Initialize session state for messages
    if "university_messages" not in st.session_state:
        st.session_state.university_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display chat messages
    for message in st.session_state.university_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_university_chat_history():
        st.session_state.university_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear University Chat History', on_click=clear_university_chat_history)

    # User-provided prompt for University Chatbot
    if university_prompt := st.chat_input("Type your question here..."):
        st.session_state.university_messages.append({"role": "user", "content": university_prompt})
        with st.chat_message("user"):
            st.write(university_prompt)
        answer = get_custom_response(university_prompt)
        st.session_state.university_messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
        print(f"User: {university_prompt}\nAssistant: {answer}")  # Print to terminal

        # Speak the response
        st.spinner(None)  # Close the "Thinking..." spinner before speaking
        #speak_with_spinner(answer)

        # Send the response to NAO for TTS
        
        send_message_to_nao(answer)

if __name__ == "__main__":
    uni_bot_interface()
