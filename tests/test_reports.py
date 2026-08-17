from src.actions.reports import ReportGenerator


feedback = [
    {
        "id": "1",
        "text": "The app keeps crashing",
        "rating": 1,
        "sentiment": "negative",
        "category": "bug",
        "priority": "critical",
    },
    {
        "id": "2",
        "text": "The application is very slow",
        "rating": 2,
        "sentiment": "negative",
        "category": "performance",
        "priority": "high",
    },
    {
        "id": "3",
        "text": "I love the application",
        "rating": 5,
        "sentiment": "positive",
        "category": "uncategorized",
        "priority": "low",
    },
    {
        "id": "4",
        "text": "Please add dark mode",
        "rating": 4,
        "sentiment": "positive",
        "category": "feature_request",
        "priority": "low",
    },
]


generator = ReportGenerator()

summary = generator.generate_summary(
    feedback
)

print("Summary:")
print(summary)

output = generator.generate_pdf(
    feedback,
    "feedback_report.pdf",
)

print("PDF generated:")
print(output)