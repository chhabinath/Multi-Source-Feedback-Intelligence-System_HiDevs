from typing import Dict

from src.intelligence.ml_models import FeedbackMLModel


class FeedbackCategorizer:
    """
    Categorizes feedback using a pre-trained NLP model.
    """

    def __init__(
        self,
        model: FeedbackMLModel = None,
    ):
        self.model = model or FeedbackMLModel()

    def categorize_feedback(
        self,
        feedback: Dict,
    ) -> Dict:

        text = feedback.get("text", "")

        result = self.model.classify(text)

        output = feedback.copy()

        output["category"] = result["category"]

        output["category_score"] = (
            result["confidence"]
        )

        output["category_confidence"] = (
            result["confidence"]
        )

        output["category_scores"] = (
            result["scores"]
        )

        return output