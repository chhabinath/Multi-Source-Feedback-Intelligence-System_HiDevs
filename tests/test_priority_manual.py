from src.processing.priority import PriorityScorer


scorer = PriorityScorer()


tests = [
    {
        "text": "The app keeps crashing and I cannot use it",
        "rating": 1,
        "sentiment": "negative",
        "sentiment_confidence": 0.90,
        "category": "bug",
    },
    {
        "text": "My payment failed and I need a refund",
        "rating": 2,
        "sentiment": "negative",
        "sentiment_confidence": 0.80,
        "category": "payment",
    },
    {
        "text": "The app is a little slow",
        "rating": 3,
        "sentiment": "negative",
        "sentiment_confidence": 0.55,
        "category": "performance",
    },
    {
        "text": "I love this game",
        "rating": 5,
        "sentiment": "positive",
        "sentiment_confidence": 0.90,
        "category": "uncategorized",
    },
]


for feedback in tests:
    result = scorer.calculate(feedback)

    print("--------------------------------")
    print("Text:", feedback["text"])
    print("Priority:", result["priority"])
    print("Score:", result["priority_score"])
    print("Urgent:", result["urgent"])
    print("Urgent keywords:", result["urgent_keywords"])