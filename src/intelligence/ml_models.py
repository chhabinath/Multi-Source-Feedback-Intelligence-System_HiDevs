from typing import Dict, List, Optional

from transformers import pipeline

from src.config.settings import settings


class FeedbackMLModel:
    """
    Pre-trained NLP model used for feedback classification.

    Uses zero-shot classification so feedback can be
    categorized without manually labeling thousands of records.
    """

    DEFAULT_CATEGORIES = [
        "bug",
        "payment",
        "login",
        "performance",
        "user interface",
        "feature request",
        "complaint",
        "praise",
        "other",
    ]

    def __init__(
        self,
        model_name: Optional[str] = None,
    ):
        """
        Initialize the zero-shot classification model.

        If model_name is not explicitly provided, the model
        configured in .env is used.
        """

        self.model_name = (
            model_name
            or settings.ML_MODEL_NAME
        )

        print(
            f"Loading ML model: {self.model_name}"
        )

        self.classifier = pipeline(
            "zero-shot-classification",
            model=self.model_name,
        )

    def classify(
        self,
        text: str,
        categories: Optional[List[str]] = None,
    ) -> Dict:
        """
        Classify one feedback text.
        """

        if not text or not text.strip():
            return {
                "category": "other",
                "confidence": 0.0,
                "scores": {},
            }

        labels = (
            categories
            or self.DEFAULT_CATEGORIES
        )

        result = self.classifier(
            text,
            candidate_labels=labels,
            multi_label=False,
        )

        return self._format_result(result)

    def classify_batch(
        self,
        texts: List[str],
        categories: Optional[List[str]] = None,
        batch_size: int = 16,
    ) -> List[Dict]:
        """
        Classify multiple feedback records.

        The model is loaded once and reused for all records.
        """

        if not texts:
            return []

        labels = (
            categories
            or self.DEFAULT_CATEGORIES
        )

        results = self.classifier(
            texts,
            candidate_labels=labels,
            multi_label=False,
            batch_size=batch_size,
        )

        return [
            self._format_result(result)
            for result in results
        ]

    @staticmethod
    def _format_result(
        result: Dict,
    ) -> Dict:
        """
        Convert Hugging Face output into
        the application's standard format.
        """

        scores = dict(
            zip(
                result["labels"],
                result["scores"],
            )
        )

        return {
            "category": result["labels"][0],
            "confidence": round(
                float(result["scores"][0]),
                4,
            ),
            "scores": {
                label: round(
                    float(score),
                    4,
                )
                for label, score in scores.items()
            },
        }