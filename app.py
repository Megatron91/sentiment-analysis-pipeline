from flask import Flask, request, jsonify
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and vectorizer
try:
    model = pickle.load(open("models/sentiment_model.pkl", "rb"))
    vectorizer = pickle.load(open("models/tfidf_vectorizer.pkl", "rb"))
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Home route for the root URL
@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to the Sentiment Analysis API</h1><p>Use the /predict endpoint to classify text.</p>"

# Favicon route to handle browser requests
@app.route("/favicon.ico")
def favicon():
    return "", 204

# Predict endpoint
@app.route("/predict", methods=["POST"])
def predict():
    # Check if the request has JSON content
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    # Parse JSON data
    data = request.get_json()
    if not data or "review_text" not in data:
        return jsonify({"error": "Invalid input. 'review_text' key is required."}), 400

    # Process review and predict sentiment
    review_text = data["review_text"]
    review_vectorized = vectorizer.transform([review_text])
    sentiment = model.predict(review_vectorized)[0]
    sentiment_label = "positive" if sentiment == 1 else "negative"

    return jsonify({"sentiment_prediction": sentiment_label})


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)