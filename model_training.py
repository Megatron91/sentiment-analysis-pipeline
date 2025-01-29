import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
import sqlite3

# Load data from SQLite
conn = sqlite3.connect("imdb_reviews.db")
query = "SELECT cleaned_review, sentiment FROM imdb_reviews"
data = pd.read_sql(query, conn)

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

# Save model and vectorizer
pickle.dump(model, open("sentiment_model.pkl", "wb"))
pickle.dump(vectorizer, open("tfidf_vectorizer.pkl", "wb"))

print("Model training complete and saved.")