import os
import streamlit as st
from groq import Groq
from PIL import Image
import json
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder

# Download NLTK resources
nltk.download('punkt')

# Load the custom dataset
with open('NAO\\miit_dataset.json', 'r') as file:
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

# Function to get response from the custom dataset chatbot
def get_custom_response(user_input):
    user_input = [user_input]
    prediction = model.predict(user_input)
    tag = label_encoder.inverse_transform(prediction)[0]
    response = random.choice(responses[tag])
    return response

# Set up Streamlit
st.set_page_config(page_title="🤖💬 NAO Chatbot", initial_sidebar_state="expanded")

# Sidebar for settings
with st.sidebar:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        logo_path = os.path.join("NAO/miit_logo.png")  # Adjust the path as needed
        logo = Image.open(logo_path)
        resized_logo = logo.resize((100, 100))  # Adjust the size as needed
        st.image(resized_logo)
    
    st.title('Myanmar Institute of Information Technology (MIIT)')
    st.title('🤖💬 NAO Chatbot')
    
    # Option to choose between "Ask about miit" and "General questions"
    st.subheader('Choose an option:')
    option = st.selectbox('Select Mode', ['Ask about miit', 'General questions'])
    
    # Settings for "General questions"
    if option == 'General questions':
        if 'temperature' not in st.session_state:
            st.session_state.temperature = 0.1
        if 'top_p' not in st.session_state:
            st.session_state.top_p = 0.9
        
        st.session_state.temperature = st.slider('Temperature', min_value=0.01, max_value=2.0, value=st.session_state.temperature, step=0.01)
        st.session_state.top_p = st.slider('Top_p', min_value=0.01, max_value=1.0, value=st.session_state.top_p, step=0.01)

    st.markdown('Developed at MIC (MIIT Infinity Club).')

# Set the API key environment variable (hardcoded or retrieved securely)
os.environ["GROQ_API_KEY"] = ""

# Initialize the Groq client with the API key from the environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define model_id for the Groq API
model_id = 'llama3-70b-8192'

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's talk with NAO. How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Let's talk with NAO. How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating Groq response
def generate_groq_response(prompt_input):
    messages = [{"role": "user", "content": prompt_input}]
    response = client.chat.completions.create(
        messages=messages,
        model=model_id,
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p
    )
    return response.choices[0].message.content

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if option == 'Ask about miit':
                response = get_custom_response(prompt)
            else:
                response = generate_groq_response(prompt)
            placeholder = st.empty()
            full_response = response
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
