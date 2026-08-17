# src/intelligence/trend_detector.py

from collections import Counter, defaultdict
from typing import Dict, List


class TrendDetector:
    """
    Analyzes processed feedback and identifies
    important trends and recurring issues.
    """

    def analyze(self, feedback_list: List[Dict]) -> Dict:
        """
        Analyze a collection of processed feedback records.
        """

        if not feedback_list:
            return self._empty_result()

        total = len(feedback_list)

        sentiment_counts = Counter()
        category_counts = Counter()

        rating_sum = 0
        rating_count = 0

        category_sentiment = defaultdict(
            lambda: {
                "total": 0,
                "negative": 0,
            }
        )

        for feedback in feedback_list:
            sentiment = feedback.get("sentiment", "unknown")
            category = feedback.get("category", "uncategorized")
            rating = feedback.get("rating")

            sentiment_counts[sentiment] += 1
            category_counts[category] += 1

            if rating is not None:
                try:
                    rating_sum += float(rating)
                    rating_count += 1
                except (TypeError, ValueError):
                    pass

            category_sentiment[category]["total"] += 1

            if sentiment == "negative":
                category_sentiment[category]["negative"] += 1

        average_rating = (
            round(rating_sum / rating_count, 2)
            if rating_count
            else None
        )

        average_sentiment = self._average_sentiment(
            feedback_list
        )

        top_issues = self._build_top_issues(
            category_sentiment
        )

        return {
            "total_feedback": total,
            "average_rating": average_rating,
            "average_sentiment": average_sentiment,
            "sentiment_distribution": dict(
                sentiment_counts
            ),
            "category_distribution": dict(
                category_counts
            ),
            "top_issues": top_issues,
        }

    @staticmethod
    def _average_sentiment(
        feedback_list: List[Dict],
    ):
        scores = []

        for feedback in feedback_list:
            score = feedback.get("sentiment_score")

            if score is not None:
                try:
                    scores.append(float(score))
                except (TypeError, ValueError):
                    continue

        if not scores:
            return None

        return round(
            sum(scores) / len(scores),
            4,
        )

    @staticmethod
    def _build_top_issues(
        category_sentiment: Dict,
    ) -> List[Dict]:
        issues = []

        for category, data in category_sentiment.items():
            total = data["total"]
            negative = data["negative"]

            negative_rate = (
                negative / total
                if total
                else 0
            )

            issues.append(
                {
                    "category": category,
                    "count": total,
                    "negative_count": negative,
                    "negative_rate": round(
                        negative_rate,
                        4,
                    ),
                }
            )

        issues.sort(
            key=lambda item: (
                item["negative_count"],
                item["negative_rate"],
                item["count"],
            ),
            reverse=True,
        )

        return issues[:10]

    @staticmethod
    def _empty_result() -> Dict:
        return {
            "total_feedback": 0,
            "average_rating": None,
            "average_sentiment": None,
            "sentiment_distribution": {},
            "category_distribution": {},
            "top_issues": [],
        }