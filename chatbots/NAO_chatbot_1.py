import json
import random
import nltk
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder

# Download NLTK resources
nltk.download('punkt')

# Load the dataset
with open(r'NAO\miit_dataset.json') as file:
    data = json.load(file)

# Extract patterns and tags
patterns = []
tags = []
responses = {}

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

# Encode tags
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(tags)

# Vectorize patterns and train a model
vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
classifier = LogisticRegression()
model = make_pipeline(vectorizer, classifier)
model.fit(patterns, labels)

# Function to get response from the chatbot
def get_response(user_input):
    user_input = [user_input]
    prediction = model.predict(user_input)
    tag = label_encoder.inverse_transform(prediction)[0]
    response = random.choice(responses[tag])
    return response

# Streamlit app
st.set_page_config(page_title="🤖💬 MIIT Chatbot", initial_sidebar_state="expanded")

# Sidebar for settings
with st.sidebar:
    st.title('Myanmar Institute of Information Technology (MIIT)')
    st.title('🤖💬 MIIT Chatbot')
    st.subheader('Settings')
    temperature = st.slider('Temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    st.markdown('Developed at MIC (MIIT Infinity Club).')

# Chatbot interface
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate response
    response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

# Clear chat history button
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
