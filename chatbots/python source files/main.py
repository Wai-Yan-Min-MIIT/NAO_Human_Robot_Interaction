# main.py
import ui
import llama3_bot
#import uni_bot_model_model
import uni_bot_model
# Setup UI and get user choice for chatbot
chatbot_choice = ui.setup_ui()

# Render the appropriate chatbot interface based on user selection
if chatbot_choice == 'Llama3 Bot':
    llama3_bot.llama3_bot_interface()
elif chatbot_choice == 'University Chatbot':
    #uni_bot_model_model.uni_bot_interface()
    uni_bot_model.uni_bot_interface()
