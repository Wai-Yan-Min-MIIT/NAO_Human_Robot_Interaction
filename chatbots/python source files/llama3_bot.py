# llama3_bot.py
import os
import streamlit as st
from groq import Groq
from tts_client import send_message_to_nao  # Import the function
from text_to_speech_pytts import speak_with_spinner

# Initialize the Groq client
def initialize_groq_client():
    os.environ["GROQ_API_KEY"] = ""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return client

client = initialize_groq_client()

# Function to truncate response to a maximum of 3 sentences and 50 words
def truncate_response(response):
    sentences = response.split('. ')
    truncated_response = '. '.join(sentences[:3])  # Take the first 3 sentences

    # Ensure it ends with a full stop
    if not truncated_response.endswith('.'):
        truncated_response += '.'

    words = truncated_response.split()
    if len(words) > 50:
        # Find the position of the last full stop before exceeding 50 words
        truncated_response = ' '.join(words[:50])
        if '.' in truncated_response:
            truncated_response = truncated_response[:truncated_response.rfind('.')] + '.'
        else:
            truncated_response += '...'
    return truncated_response

# Function for generating Groq response for Llama3 Bot
def generate_groq_response(prompt_input, model_id, temperature, top_p, max_tokens):
    messages = [{"role": "user", "content": prompt_input}]
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )
        full_response = response.choices[0].message.content
        truncated_response = truncate_response(full_response)
        return truncated_response
    except Exception as e:
        st.error(f"Error generating Groq response: {e}")
        print(f"Error generating Groq response: {e}")  # Print error to terminal
        return "Sorry, I couldn't generate a response. Please try again later."

# Function to handle Llama3 Bot interface
def llama3_bot_interface():
    st.title("NAO Bot Application")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Let's talk with NAO. How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "Let's talk with Llama3. How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_groq_response(prompt, 'llama3-70b-8192', 0.10, 0.90, 100)
                placeholder = st.empty()
                placeholder.markdown(response)
                print(f"User: {prompt}\nAssistant: {response}")  # Debugging output
        st.spinner(None)  # Close the "Thinking..." spinner before speaking
        # speak_with_spinner(response)
        send_message_to_nao(response)  # Send the response to NAO for TTS
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    llama3_bot_interface()
