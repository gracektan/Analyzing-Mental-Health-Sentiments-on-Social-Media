import json
from google.cloud import language_v1

# Create a client instance for the Natural Language API
client = language_v1.LanguageServiceClient()

# Load and iterate through your dataset JSON file
with open('C:\\Analyzing-Mental-Health-Sentiments-on-Social-Media\\combined_anxiety.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    posts = data['posts']

    for post in posts:
        content = post['content']

        # Analyze sentiment for each post
        document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})

        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude

        print(f"Content: {content}")
        print(f"Sentiment Score: {sentiment_score}")
        print(f"Sentiment Magnitude: {sentiment_magnitude}")
        print("----")
