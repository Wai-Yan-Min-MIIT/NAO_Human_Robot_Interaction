# ui.py
import streamlit as st
from PIL import Image

def setup_ui():
    # Set page configuration
    st.set_page_config(page_title="🤖💬 Chatbots", initial_sidebar_state="expanded")

    # Sidebar for settings
    with st.sidebar:
        # Center the logo
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            logo = Image.open("miit_logo.png")
            resized_logo = logo.resize((100, 100))  # Adjust the size as needed
            st.image(resized_logo)

        # Centered titles and markdown
        st.markdown("<h1 style='text-align: center;'>Myanmar Institute of Information Technology (MIIT)</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🤖💬 Chatbots</h1>", unsafe_allow_html=True)

        chatbot_choice = st.radio("Choose a chatbot:", ['Llama3 Bot', 'University Chatbot'])

        st.markdown("<p style='text-align: center;'>Developed at MIC (MIIT Infinity Club).</p>", unsafe_allow_html=True)

    return chatbot_choice
