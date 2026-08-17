from src.intelligence.ai_prompts import FeedbackPromptBuilder


builder = FeedbackPromptBuilder()

feedback = {
    "text": "The application keeps crashing after the update",
    "rating": 1,
    "sentiment": "negative",
    "sentiment_confidence": 0.91,
    "category": "bug",
    "priority": "critical",
}


prompt = builder.build_feedback_analysis_prompt(
    feedback
)

print(prompt)