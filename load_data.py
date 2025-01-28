import sqlite3
import pandas as pd
from datasets import load_dataset

# Load the IMDB dataset
dataset = load_dataset("imdb")
train_data = pd.DataFrame(dataset["train"])
test_data = pd.DataFrame(dataset["test"])

# Connect to SQLite
conn = sqlite3.connect("imdb_reviews.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS imdb_reviews (
    id INTEGER PRIMARY KEY,
    review_text TEXT,
    sentiment TEXT
)
""")

# Insert data
for idx, row in train_data.iterrows():
    cursor.execute("INSERT INTO imdb_reviews (id, review_text, sentiment) VALUES (?, ?, ?)",
                   (idx, row["text"], "positive" if row["label"] == 1 else "negative"))

conn.commit()
conn.close()
print("Database setup complete.")
