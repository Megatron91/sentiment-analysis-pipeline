import sqlite3
import pandas as pd
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Connect to SQLite database
conn = sqlite3.connect("imdb_reviews.db")
query = "SELECT * FROM imdb_reviews"
data = pd.read_sql(query, conn)

# Data Cleaning Function
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    return text

# Apply cleaning to the data
data["cleaned_review"] = data["review_text"].apply(clean_text)

# Save cleaned data back to the database (optional)
cursor = conn.cursor()
cursor.execute("ALTER TABLE imdb_reviews ADD COLUMN cleaned_review TEXT")
for idx, row in data.iterrows():
    cursor.execute("UPDATE imdb_reviews SET cleaned_review = ? WHERE id = ?", (row["cleaned_review"], row["id"]))
conn.commit()

# Exploratory Data Analysis
# 1. Sentiment distribution
sentiment_counts = data["sentiment"].value_counts()
print("Sentiment Distribution:\n", sentiment_counts)

# Plot sentiment distribution
sentiment_counts.plot(kind="bar", title="Sentiment Distribution", color=["blue", "orange"])
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.savefig("sentiment_distribution.png")  # Save the plot
plt.show()

# 2. Average review length
data["review_length"] = data["cleaned_review"].apply(len)
avg_length = data.groupby("sentiment")["review_length"].mean()
print("\nAverage Review Length by Sentiment:\n", avg_length)

# 3. Word Cloud for Positive Sentiment
positive_reviews = " ".join(data[data["sentiment"] == "positive"]["cleaned_review"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(positive_reviews)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Positive Reviews")
plt.savefig("positive_wordcloud.png")  # Save the plot
plt.show()

# Word Cloud for Negative Sentiment (Optional)
negative_reviews = " ".join(data[data["sentiment"] == "negative"]["cleaned_review"])
wordcloud_neg = WordCloud(width=800, height=400, background_color="black").generate(negative_reviews)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_neg, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Negative Reviews")
plt.savefig("negative_wordcloud.png")  # Save the plot
plt.show()

print("Data Cleaning and EDA completed.")
