from src.intelligence.ml_models import FeedbackMLClassifier


training_data = [
    {
        "text": "The application keeps crashing",
        "category": "bug",
    },
    {
        "text": "The app shows an error every time I open it",
        "category": "bug",
    },
    {
        "text": "I cannot login to my account",
        "category": "login",
    },
    {
        "text": "My password login is not working",
        "category": "login",
    },
    {
        "text": "My payment failed",
        "category": "payment",
    },
    {
        "text": "I need a refund for my transaction",
        "category": "payment",
    },
    {
        "text": "The application is extremely slow",
        "category": "performance",
    },
    {
        "text": "The app takes too long to load",
        "category": "performance",
    },
]


classifier = FeedbackMLClassifier()

training_result = classifier.train(
    training_data
)

print("Training result:")
print(training_result)

test_texts = [
    "The app crashes when I open it",
    "I cannot access my account",
    "My transaction failed",
    "The application is very slow",
]

print("\nPredictions:")

for text in test_texts:
    result = classifier.predict(text)

    print("--------------------------------")
    print("Text:", text)
    print("Category:", result["category"])
    print("Confidence:", result["confidence"])
    print("Probabilities:", result["probabilities"])