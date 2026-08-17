from src.processing.categorizer import FeedbackCategorizer


categorizer = FeedbackCategorizer()

tests = [
    "The app keeps crashing and shows an error",
    "I cannot login with my password",
    "My payment failed and I need a refund",
    "The application is very slow",
    "Please add dark mode",
    "The button design is confusing",
    "I am worried about privacy and security",
    "I love this game",
]


for text in tests:
    result = categorizer.categorize(text)

    print("--------------------------------")
    print("Text:", text)
    print("Category:", result["category"])
    print("Score:", result["category_score"])
    print("Keywords:", result["matched_keywords"])
