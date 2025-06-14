import json
import nltk
from nltk.data import find
from nltk.data import path as nltk_path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
import joblib

# Set the NLTK data path
nltk_path.append('C:/Users/User/AppData/Roaming/nltk_data')

# Ensure the punkt package is available
try:
    find('tokenizers/punkt')
except LookupError:
    print("punkt not found in the specified NLTK data path. Please ensure it is downloaded and placed correctly.")

# Load the custom dataset
with open('miit_dataset_version2.json', 'r') as file:
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
vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english', token_pattern=None)
classifier = LogisticRegression()
model = make_pipeline(vectorizer, classifier)
model.fit(patterns, labels)

# Save the trained model, label encoder, and responses
joblib.dump(model, 'chatbot_model_version2.pkl')
joblib.dump(label_encoder, 'label_encoder_version2.pkl')
with open('responses_version2.json', 'w') as f:
    json.dump(responses, f)
