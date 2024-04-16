import os
import json
from google.cloud import language_v1
import csv

# Set Google Cloud credentials from environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\service_account_key.json"

# Create a client instance for the Natural Language API
client = language_v1.LanguageServiceClient()

# Specify the full path to the dataset JSON file containing social media posts about suicidal ideation
json_file_path = 'C:\\Analyzing-Mental-Health-Sentiments-on-Social-Media\\combined_suicidal ideation.json'

# Load and iterate through the dataset JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    posts = data['posts']

    content_list = []

    # Iterate over each post in the dataset
    for post in posts:
        content = post['content']

        try:
            # Analyze sentiment for each post
            document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
            response = client.analyze_sentiment(request={'document': document})

            sentiment_score = response.document_sentiment.score

            # Determine if the content indicates suicidal ideation based on sentiment score
            if sentiment_score < -0.7:  # Example threshold for identifying suicidal language
                content_list.append(content)

        except Exception as e:
            # Handle errors during sentiment analysis
            print(f"Error processing content: {content}")
            print(f"Error message: {str(e)}")
            continue

# Export detected suicidal ideation mentions to CSV file
csv_file_path = 'C:\\Analyzing-Mental-Health-Sentiments-on-Social-Media\\suicidal_ideation_mentions.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Content'])

    for content in content_list:
        writer.writerow([content])

print(f'Suicidal ideation mentions exported to {csv_file_path}')
