from flask import Flask, request, jsonify
import torch
import joblib

app = Flask(__name__)

# Load models
model = torch.load('deep_learning_model.pth')
model.eval()
vectorizer = joblib.load('tfidf_vectorizer.pkl')
naive_bayes_model = joblib.load('naive_bayes_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Preprocess
    features = vectorizer.transform([message])
    
    # Predictions
    deep_prediction = model(features).argmax().item()
    nb_prediction = naive_bayes_model.predict(features)[0]

    return jsonify({
        'deep_learning_prediction': deep_prediction,
        'naive_bayes_prediction': nb_prediction
    })

if __name__ == '__main__':
    app.run(debug=True)
