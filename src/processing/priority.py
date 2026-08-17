from typing import Dict


class PriorityScorer:
    """
    Calculates feedback priority.

    Priority is based on:
    - rating
    - sentiment
    - category
    - urgent keywords
    """

    URGENT_KEYWORDS = {
        "urgent",
        "emergency",
        "critical",
        "cannot",
        "can't",
        "unable",
        "blocked",
        "broken",
        "crash",
        "crashes",
        "failure",
        "failing",
    }

    CRITICAL_CATEGORIES = {
        "payment",
        "bug",
        "login",
    }

    def score_feedback(
        self,
        feedback: Dict,
    ) -> Dict:

        result = feedback.copy()

        text = result.get(
            "text",
            "",
        ).lower()

        rating = result.get(
            "rating",
            3,
        )

        sentiment = result.get(
            "sentiment",
            "neutral",
        )

        category = result.get(
            "category",
            "other",
        )

        urgent_keywords = [
            keyword
            for keyword in self.URGENT_KEYWORDS
            if keyword in text
        ]

        score = 0

        # Very low rating
        if rating <= 2:
            score += 5

        # Negative sentiment
        if sentiment == "negative":
            score += 3

        # Critical categories
        if category in self.CRITICAL_CATEGORIES:
            score += 3

        # Urgent language
        if urgent_keywords:
            score += 4

        # Determine priority
        if score >= 10:
            priority = "critical"
        elif score >= 7:
            priority = "high"
        elif score >= 4:
            priority = "medium"
        else:
            priority = "low"

        result["priority"] = priority
        result["priority_score"] = score
        result["urgent"] = bool(urgent_keywords)
        result["urgent_keywords"] = urgent_keywords

        return result