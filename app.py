import os
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Model & Vectorizer with Proper Error Handling
model_path = "sentiment_model.pkl"
vectorizer_path = "tfidf_vectorizer.pkl"

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    print("Error: Model or vectorizer not found. Please train the model first.")
    exit(1)

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to Sentiment Analysis API</h1><p>Use /predict to classify text. and please use curl or postman with apropriate json body.</p>"

@app.route("/predict", methods=["POST"])
def predict():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if "review_text" not in data:
        return jsonify({"error": "Missing 'review_text' field"}), 400

    review = data["review_text"]
    review_vectorized = vectorizer.transform([review])
    prediction = model.predict(review_vectorized)[0]
    
    return jsonify({"sentiment_prediction": "positive" if prediction == 1 else "negative"})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)