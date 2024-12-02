from flask import Flask, request, jsonify
import torch
import joblib
from model import SMSClassifier

app = Flask(__name__)

# -------------------------------
# Load Deep Learning Model
# -------------------------------
# Define model parameters
vocab_size = 128  # ASCII characters
embed_dim = 64
num_classes = 4

# Recreate and load the deep learning model
dl_model = SMSClassifier(vocab_size, embed_dim, num_classes)
dl_model.load_state_dict(torch.load('deep_learning_model.pth'))
dl_model.eval()  # Set to evaluation mode

# -------------------------------
# Load Naive Bayes Model and Vectorizer
# -------------------------------
nb_model = joblib.load('naive_bayes_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# -------------------------------
# Helper Functions
# -------------------------------

def tokenize_text(text, max_len=128):
    """Tokenize text for the deep learning model."""
    tokens = [ord(c) for c in text if ord(c) < 128]
    if len(tokens) > max_len:
        tokens = tokens[:max_len]
    else:
        tokens += [0] * (max_len - len(tokens))
    return torch.tensor(tokens, dtype=torch.long).unsqueeze(0)  # Add batch dimension

def preprocess_text_for_nb(text):
    """Preprocess text for the Naive Bayes model."""
    return vectorizer.transform([text])  # Convert text to TF-IDF features

# -------------------------------
# API Endpoints
# -------------------------------

@app.route('/')
def home():
    return "SMS Classification API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    """Predict using both models."""
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Deep Learning Prediction
    input_tensor = tokenize_text(message)
    dl_output = dl_model(input_tensor)
    _, dl_prediction = torch.max(dl_output, dim=1)

    # Naive Bayes Prediction
    nb_input = preprocess_text_for_nb(message)
    nb_prediction = nb_model.predict(nb_input)[0]

    return jsonify({
        'deep_learning_prediction': int(dl_prediction.item()),
        'naive_bayes_prediction': int(nb_prediction)
    })

# -------------------------------
# Run the Application
# -------------------------------

if __name__ == '__main__':
    app.run(debug=True)
