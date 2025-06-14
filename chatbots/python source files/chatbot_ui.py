# chatbot_ui.py (Python 3.12.2)
from tts_client import send_message_to_nao

def handle_chat_response(response):
    # Process chatbot response
    print("Chatbot response:", response)

    # Send the response to Nao
    send_message_to_nao(response)

# Example usage in your chatbot UI
if __name__ == "__main__":
    chat_response = "Hello from the chatbot!"
    handle_chat_response(chat_response)
