import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
import sqlite3

# Define file paths for model and vectorizer
MODEL_FILE = "models/sentiment_model.pkl"
VECTORIZER_FILE = "models/tfidf_vectorizer.pkl"

# Create models directory if it doesn’t exist
os.makedirs("models", exist_ok=True)

# Load data from SQLite
conn = sqlite3.connect("imdb_reviews.db")
query = "SELECT cleaned_review, sentiment FROM imdb_reviews"
data = pd.read_sql(query, conn)
conn.close()  # Close database connection after loading data

# Drop missing values (fix for NoneType issue)
data = data.dropna(subset=["cleaned_review"])

# Convert sentiment labels to binary
data["sentiment"] = data["sentiment"].apply(lambda x: 1 if x == "positive" else 0)

# Split data
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(
    data["cleaned_review"], data["sentiment"], test_size=0.2, random_state=42
)

# Drop None values again (if any)
X_train = X_train.dropna()
X_val = X_val.dropna()

# Vectorize text
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Evaluate model
y_pred = model.predict(X_val_tfidf)
print(classification_report(y_val, y_pred))

# Save model and vectorizer safely
with open(MODEL_FILE, "wb") as model_file:
    pickle.dump(model, model_file)
with open(VECTORIZER_FILE, "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print(f"Model training complete. Saved as {MODEL_FILE} and {VECTORIZER_FILE}.")