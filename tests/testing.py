from src.ingestion.api_clients import GooglePlayDatasetClient
from src.processing.cleaner import TextCleaner
from src.processing.analyzer import SentimentAnalyzer
from src.processing.categorizer import FeedbackCategorizer

client = GooglePlayDatasetClient()

feedback = client.fetch_feedback(limit=10)

cleaner = TextCleaner()
analyzer = SentimentAnalyzer()
categorizer = FeedbackCategorizer()

feedback = cleaner.clean_batch(feedback)
feedback = analyzer.analyze_batch(feedback)
feedback = categorizer.categorize_batch(feedback)

for item in feedback:
    print("--------------------------------")
    print("ID:", item["id"])
    print("Text:", item["text"])
    print("Rating:", item["rating"])
    print("Sentiment:", item["sentiment"])
    print("Confidence:", item["sentiment_confidence"])
    print("Category:", item["category"])
    print("Category Score:", item["category_score"])