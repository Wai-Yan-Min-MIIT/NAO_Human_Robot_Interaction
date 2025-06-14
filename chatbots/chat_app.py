import os
import streamlit as st
from groq import Groq
from PIL import Image


# Set page configuration
st.set_page_config(page_title="🤖💬 NAO Chatbot", initial_sidebar_state="expanded")

# Sidebar for settings
with st.sidebar:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        logo_path = os.path.join("C:/Users/L-72/Wai_yan_folder/programming/NAO/miit_logo.png")  # Adjust the path as needed
        logo = Image.open(logo_path)
        resized_logo = logo.resize((100, 100))  # Adjust the size as needed
        st.image(resized_logo)
   

    
    st.title('Myanmar Institute of Information Technology (MIIT)')
    st.title('🤖💬 NAO Chatbot')
    # st.header("Let's talk with NAO.")
    
    st.subheader('Models and parameters')
    model_id = 'llama3-70b-8192'


    temperature = st.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)

    st.markdown('Developed at MIC (MIIT Infinity Club).')

# Set the API key environment variable (hardcoded or retrieved securely)
os.environ["GROQ_API_KEY"] = "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"

# Initialize the Groq client with the API key from the environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Store LLM generated responses
if "messages" not in st.session_state.keys():
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
        temperature=temperature,
        top_p=top_p
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
            response = generate_groq_response(prompt)
            placeholder = st.empty()
            full_response = response
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
