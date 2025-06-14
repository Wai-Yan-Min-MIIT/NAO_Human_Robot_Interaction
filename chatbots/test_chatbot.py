import os
from groq import Groq

# Set the API key environment variable
os.environ["GROQ_API_KEY"] = "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"

# Initialize the Groq client with the API key from the environment variable
client = Groq()

# Create a chat completion request
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-70b-8192",
    # model="llama3-8b-8192",
)

# Print the content of the first choice
print(chat_completion.choices[0].message.content)
