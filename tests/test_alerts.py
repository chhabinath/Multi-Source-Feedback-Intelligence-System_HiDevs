from src.actions.alerts import AlertManager


manager = AlertManager()


tests = [
    {
        "id": "feedback_001",
        "text": "The app keeps crashing",
        "priority": "critical",
        "category": "bug",
        "sentiment": "negative",
        "urgent": True,
    },
    {
        "id": "feedback_002",
        "text": "The app is slightly slow",
        "priority": "medium",
        "category": "performance",
        "sentiment": "negative",
        "urgent": False,
    },
    {
        "id": "feedback_003",
        "text": "I love the application",
        "priority": "low",
        "category": "uncategorized",
        "sentiment": "positive",
        "urgent": False,
    },
]


for feedback in tests:

    result = manager.create_alert(
        feedback
    )

    print("--------------------------------")
    print("Feedback:", feedback["text"])
    print("Alert required:", result["alert_required"])

    if result["alert"]:
        print("Alert:", result["alert"])