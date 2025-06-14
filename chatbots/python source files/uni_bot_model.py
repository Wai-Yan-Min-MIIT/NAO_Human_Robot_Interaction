# uni_bot_model.py
import os
import streamlit as st
import json
import random
import joblib
from tts_client import send_message_to_nao  # Import the function
from text_to_speech_pytts import speak_with_spinner
import re

# Load the trained model, vectorizer, label encoder, and responses
model = joblib.load('chatbot_model_version2.pkl')
vectorizer = joblib.load('vectorizer_version2.pkl')
label_encoder = joblib.load('label_encoder_version2.pkl')
with open('responses_version2.json', 'r') as f:
    responses = json.load(f)

# Function to tokenize text into words
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Function to search for user input manually in tags
def manual_search(user_input):
    matching_tags = set()
    user_keywords = set(tokenize(user_input))
    for tag in responses.keys():
        tag_keywords = set(tokenize(tag))
        if user_keywords & tag_keywords:
            matching_tags.add(tag)
    return list(matching_tags)

# Function to get response from the custom dataset chatbot
def get_custom_response(user_input):
    user_input_vectorized = vectorizer.transform([user_input])
    prediction = model.predict(user_input_vectorized)
    tag = label_encoder.inverse_transform(prediction)[0]
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

        # Perform manual search first
        matching_tags = manual_search(university_prompt)
        
        if len(matching_tags) == 1:
            # Single match found, use it
            response = random.choice(responses[matching_tags[0]])
        elif len(matching_tags) > 1:
            # Multiple matches found, use model prediction
            response = get_custom_response(university_prompt)
        else:
            # No matches found, use model prediction
            response = get_custom_response(university_prompt)

        # Replace 'MIIT' with 'M I I T' in the response
        

        st.session_state.university_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        print(f"User: {university_prompt}\nAssistant: {response}")  # Print to terminal

        # Speak the response
        st.spinner(None)  # Close the "Thinking..." spinner before speaking
        #speak_with_spinner(response)

        # Send the response to NAO for TTS
        response = response.replace('MIIT', 'M I I T')
        print(f"NAO {response}")
        send_message_to_nao(response)

if __name__ == "__main__":
    uni_bot_interface()
