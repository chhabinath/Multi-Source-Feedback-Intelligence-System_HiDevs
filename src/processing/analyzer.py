from typing import Dict, List

from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer,
)


class SentimentAnalyzer:
    """
    Analyzes customer feedback sentiment using VADER.

    Produces:
    - sentiment label
    - sentiment score
    - confidence score
    """

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> Dict:
        """
        Analyze one feedback text.
        """

        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.0,
            }

        scores = self.analyzer.polarity_scores(text)

        compound = scores["compound"]

        sentiment = self._get_sentiment_label(
            compound
        )

        confidence = self._calculate_confidence(
            scores
        )

        return {
            "sentiment": sentiment,
            "score": round(compound, 4),
            "confidence": round(confidence, 4),
        }

    def analyze_feedback(
        self,
        feedback: Dict,
    ) -> Dict:
        """
        Add sentiment results to a feedback record.
        """

        result = feedback.copy()

        sentiment_result = self.analyze(
            feedback.get("text", "")
        )

        result["sentiment"] = (
            sentiment_result["sentiment"]
        )

        result["sentiment_score"] = (
            sentiment_result["score"]
        )

        result["sentiment_confidence"] = (
            sentiment_result["confidence"]
        )

        return result

    def analyze_batch(
        self,
        feedback_list: List[Dict],
    ) -> List[Dict]:
        """
        Analyze multiple feedback records.
        """

        return [
            self.analyze_feedback(feedback)
            for feedback in feedback_list
        ]

    @staticmethod
    def _get_sentiment_label(
        compound_score: float,
    ) -> str:

        if compound_score >= 0.05:
            return "positive"

        if compound_score <= -0.05:
            return "negative"

        return "neutral"

    @staticmethod
    def _calculate_confidence(
        scores: Dict[str, float],
    ) -> float:

        return max(
            scores["pos"],
            scores["neg"],
            scores["neu"],
        )