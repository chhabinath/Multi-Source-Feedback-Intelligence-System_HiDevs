from src.intelligence.trend_detector import TrendDetector


detector = TrendDetector()


feedback = [
    {
        "created_at": "2026-01-01",
        "sentiment": "positive",
        "category": "performance",
    },
    {
        "created_at": "2026-01-02",
        "sentiment": "positive",
        "category": "performance",
    },
    {
        "created_at": "2026-02-01",
        "sentiment": "negative",
        "category": "performance",
    },
    {
        "created_at": "2026-02-02",
        "sentiment": "negative",
        "category": "performance",
    },
]


result = detector.detect_sentiment_trend(
    feedback
)

print("Sentiment trend:")
print(result)


category_result = detector.detect_category_trends(
    feedback
)

print("\nCategory trends:")
print(category_result)


emerging = detector.detect_emerging_issues(
    feedback
)

print("\nEmerging issues:")
print(emerging)