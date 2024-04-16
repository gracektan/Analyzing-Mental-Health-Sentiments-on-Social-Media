import os
import json
from google.cloud import language_v1
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# Set Google Cloud credentials from environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\service_account_key.json"

# Create a client instance for the Natural Language API
client = language_v1.LanguageServiceClient()

# Specify the full path to your dataset JSON file
json_file_path = 'C:\\Analyzing-Mental-Health-Sentiments-on-Social-Media\\combined_anxiety.json'

# Load and iterate through the dataset JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    posts = data['posts']

    sentiment_scores = []
    sentiment_magnitudes = []
    content_list = []

    # Iterate over each post in the dataset
    for post in posts:
        content = post['content']

        try:
            # Analyze sentiment for each post
            document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
            response = client.analyze_sentiment(request={'document': document})

            sentiment_score = response.document_sentiment.score
            sentiment_magnitude = response.document_sentiment.magnitude

            # Store sentiment scores, magnitudes, and content
            sentiment_scores.append(sentiment_score)
            sentiment_magnitudes.append(sentiment_magnitude)
            content_list.append(content)

            # Print sentiment analysis results for each post
            print(f"Content: {content}")
            print(f"Sentiment Score: {sentiment_score}")
            print(f"Sentiment Magnitude: {sentiment_magnitude}")
            print("----")

        except Exception as e:
            # Handle errors during sentiment analysis
            print(f"Error processing content: {content}")
            print(f"Error message: {str(e)}")
            continue

# Plotting sentiment scores and magnitudes using matplotlib and seaborn
plt.figure(figsize=(12, 6))

# Sentiment Score Distribution
plt.subplot(1, 2, 1)
sns.histplot(sentiment_scores, bins=10, kde=True, color='skyblue')
plt.title('Distribution of Sentiment Scores')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')

# Sentiment Magnitude Distribution
plt.subplot(1, 2, 2)
sns.histplot(sentiment_magnitudes, bins=10, kde=True, color='salmon')
plt.title('Distribution of Sentiment Magnitudes')
plt.xlabel('Sentiment Magnitude')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Print messages before writing to CSV file
print("Finished sentiment analysis for all posts. Writing to CSV file...")

# Specify the full path for CSV export
csv_file_path = 'C:\\Analyzing-Mental-Health-Sentiments-on-Social-Media\\sentiment_analysis_results.csv'

# Export sentiment analysis results to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Content', 'Sentiment Score', 'Sentiment Magnitude'])

    # Write sentiment analysis results to CSV file
    for content, score, magnitude in zip(content_list, sentiment_scores, sentiment_magnitudes):
        writer.writerow([content, score, magnitude])

print(f'Sentiment analysis results exported to {csv_file_path}')

# Print link to CSV file
print(f'CSV file location: {csv_file_path}')
