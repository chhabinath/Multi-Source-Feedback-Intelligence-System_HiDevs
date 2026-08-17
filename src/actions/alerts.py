from typing import Dict, List


class AlertManager:
    """
    Determines whether feedback requires an alert
    and creates structured alert information.
    """

    ALERT_PRIORITY_LEVELS = {
        "high",
        "critical",
    }

    def should_alert(self, feedback: Dict) -> bool:
        """
        Determine whether a feedback item requires an alert.
        """

        priority = feedback.get(
            "priority",
            "low",
        )

        urgent = feedback.get(
            "urgent",
            False,
        )

        sentiment = feedback.get(
            "sentiment",
            "neutral",
        )

        if priority in self.ALERT_PRIORITY_LEVELS:
            return True

        if urgent and sentiment == "negative":
            return True

        return False

    def create_alert(
        self,
        feedback: Dict,
    ) -> Dict:
        """
        Create a structured alert from feedback.
        """

        if not self.should_alert(feedback):
            return {
                "alert_required": False,
                "alert": None,
            }

        alert = {
            "alert_required": True,
            "alert": {
                "feedback_id": feedback.get("id"),
                "priority": feedback.get(
                    "priority",
                    "unknown",
                ),
                "category": feedback.get(
                    "category",
                    "uncategorized",
                ),
                "sentiment": feedback.get(
                    "sentiment",
                    "unknown",
                ),
                "message": self._build_message(
                    feedback
                ),
            },
        }

        return alert

    def create_alerts(
        self,
        feedback_list: List[Dict],
    ) -> List[Dict]:
        """
        Create alerts for multiple feedback records.

        Only feedback requiring alerts is returned.
        """

        alerts = []

        for feedback in feedback_list:

            result = self.create_alert(
                feedback
            )

            if result["alert_required"]:
                alerts.append(
                    result["alert"]
                )

        return alerts

    @staticmethod
    def _build_message(
        feedback: Dict,
    ) -> str:
        """
        Build a human-readable alert message.
        """

        priority = feedback.get(
            "priority",
            "unknown",
        )

        category = feedback.get(
            "category",
            "uncategorized",
        )

        text = feedback.get(
            "text",
            "",
        )

        return (
            f"{priority.upper()} priority feedback "
            f"detected in category '{category}': "
            f"{text}"
        )