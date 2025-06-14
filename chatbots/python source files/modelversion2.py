import json
import random
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib

# Load the JSON data
with open('miit_dataset_version2.json', 'r') as file:
    data = json.load(file)

# Extract patterns and tags
patterns = []
tags = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])

# Convert to DataFrame
df = pd.DataFrame({'pattern': patterns, 'tag': tags})

# Encode the labels
label_encoder = LabelEncoder()
df['tag'] = label_encoder.fit_transform(df['tag'])

# Vectorize the text data
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(df['pattern'])
y = df['tag']

# Train the SVM model
model = SVC(kernel='linear')
model.fit(X_vectorized, y)

# Save the model, vectorizer, and label encoder
joblib.dump(model, 'chatbot_model_version2.pkl')
joblib.dump(vectorizer, 'vectorizer_version2.pkl')
joblib.dump(label_encoder, 'label_encoder_version2.pkl')

# Save the responses
responses = {}
for intent in data['intents']:
    responses[intent['tag']] = intent['responses']
with open('responses_version2.json', 'w') as f:
    json.dump(responses, f, indent=4)

print("Model, vectorizer, label encoder, and responses have been saved.")
