import sqlite3
import pandas as pd
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Connect to SQLite database
conn = sqlite3.connect("imdb_reviews.db")
query = "SELECT * FROM imdb_reviews"
data = pd.read_sql(query, conn)

# Data Cleaning Function
def clean_text(text):
    if pd.isna(text):  # Skip None/NaN values
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove punctuation
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

# Remove duplicate reviews
data = data.drop_duplicates(subset=["review_text"])

# Drop missing (NaN) values before cleaning
data = data.dropna(subset=["review_text"])

# Apply cleaning to the data
data["cleaned_review"] = data["review_text"].apply(clean_text)

# Drop rows where cleaning resulted in empty strings
data = data[data["cleaned_review"].str.strip() != ""]

# Save cleaned data back to the database
cursor = conn.cursor()
cursor.execute("ALTER TABLE imdb_reviews ADD COLUMN cleaned_review TEXT")
for idx, row in data.iterrows():
    cursor.execute("UPDATE imdb_reviews SET cleaned_review = ? WHERE id = ?", (row["cleaned_review"], row["id"]))
conn.commit()

# Save cleaned data to CSV for easy access
data.to_csv("cleaned_imdb_reviews.csv", index=False)


print("Data Cleaning Complete")

# Exploratory Data Analysis

# 1. Sentiment Distribution
sentiment_counts = data["sentiment"].value_counts()
print("Sentiment Distribution:\n", sentiment_counts)

# Plot sentiment distribution
plt.figure(figsize=(6, 4))
sns.countplot(x=data["sentiment"], palette="coolwarm")
plt.title("Sentiment Distribution in IMDB Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.savefig("images/sentiment_distribution.png")  # Save the plot
plt.show()

# 2. Review Length Analysis
data["review_length"] = data["cleaned_review"].apply(lambda x: len(x.split()))
avg_length = data.groupby("sentiment")["review_length"].mean()
print("\nAverage Review Length by Sentiment:\n", avg_length)

# Plot Review Length Distribution
plt.figure(figsize=(6, 4))
sns.boxplot(x=data["sentiment"], y=data["review_length"], palette="coolwarm")
plt.title("Review Length Distribution by Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Review Length (words)")
plt.savefig("images/review_length_distribution.png")  # Save the plot
plt.show()

# 3. Word Cloud for Positive Sentiment
positive_reviews = " ".join(data[data["sentiment"] == "positive"]["cleaned_review"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(positive_reviews)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Positive Reviews")
plt.savefig("images/positive_wordcloud.png")  # Save the plot
plt.show()

# 4. Word Cloud for Negative Sentiment
negative_reviews = " ".join(data[data["sentiment"] == "negative"]["cleaned_review"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(negative_reviews)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Negative Reviews")
plt.savefig("images/negative_wordcloud.png")  # Save the plot
plt.show()

print("Data Cleaning & EDA Complete!")