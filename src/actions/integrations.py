from typing import Dict, List


class IntegrationHub:
    """
    Central integration layer for connecting the
    feedback intelligence system with external
    business systems.
    """

    def create_support_ticket(
        self,
        feedback: Dict,
    ) -> Dict:
        """
        Prepare a support ticket from feedback.

        This method currently returns the ticket payload.
        A real support-system API can be connected later.
        """

        return {
            "success": True,
            "integration": "support",
            "action": "create_ticket",
            "ticket": {
                "feedback_id": feedback.get("id"),
                "title": self._build_ticket_title(
                    feedback
                ),
                "description": feedback.get(
                    "text",
                    "",
                ),
                "category": feedback.get(
                    "category",
                    "uncategorized",
                ),
                "priority": feedback.get(
                    "priority",
                    "low",
                ),
            },
        }

    def update_crm(
        self,
        feedback: Dict,
    ) -> Dict:
        """
        Prepare CRM information from feedback.
        """

        return {
            "success": True,
            "integration": "crm",
            "action": "update_customer",
            "data": {
                "feedback_id": feedback.get("id"),
                "sentiment": feedback.get(
                    "sentiment",
                    "unknown",
                ),
                "category": feedback.get(
                    "category",
                    "uncategorized",
                ),
                "rating": feedback.get(
                    "rating",
                ),
            },
        }

    def send_notification(
        self,
        message: str,
        channel: str = "team",
    ) -> Dict:
        """
        Prepare a team notification.

        Actual delivery can later be connected to
        Slack, email, Teams, etc.
        """

        return {
            "success": True,
            "integration": "notification",
            "action": "send_notification",
            "channel": channel,
            "message": message,
        }

    def process_feedback(
        self,
        feedback: Dict,
    ) -> List[Dict]:
        """
        Decide which integrations should receive
        the feedback.
        """

        results = []

        priority = feedback.get(
            "priority",
            "low",
        )

        category = feedback.get(
            "category",
            "uncategorized",
        )

        if priority in {
            "high",
            "critical",
        }:
            results.append(
                self.create_support_ticket(
                    feedback
                )
            )

        results.append(
            self.update_crm(
                feedback
            )
        )

        if priority == "critical":
            results.append(
                self.send_notification(
                    message=(
                        "Critical feedback detected: "
                        f"{feedback.get('text', '')}"
                    ),
                    channel="critical-alerts",
                )
            )

        return results

    @staticmethod
    def _build_ticket_title(
        feedback: Dict,
    ) -> str:
        category = feedback.get(
            "category",
            "Feedback",
        )

        return (
            f"{category.title()} issue reported"
        )