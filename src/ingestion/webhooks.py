from typing import Dict, Optional


class WebhookReceiver:
    """
    Receives feedback submitted through web forms or external
    webhook integrations.
    """

    def receive(self, payload: Dict) -> Dict:
        """
        Validate and normalize an incoming webhook payload.

        Expected payload:
        {
            "id": "web_001",
            "text": "The application is great",
            "rating": 5,
            "source": "web"
        }

        Returns:
            Normalized feedback record.
        """

        if not isinstance(payload, dict):
            raise ValueError("Webhook payload must be a dictionary.")

        feedback_id = payload.get("id")
        text = payload.get("text")
        rating = payload.get("rating")

        if not feedback_id:
            raise ValueError("Feedback id is required.")

        if not text or not str(text).strip():
            raise ValueError("Feedback text is required.")

        if rating is not None:
            try:
                rating = int(rating)
            except (TypeError, ValueError):
                raise ValueError("Rating must be an integer.")

            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5.")

        return {
            "id": str(feedback_id),
            "text": str(text),
            "rating": rating,
            "source": payload.get("source", "web"),
            "metadata": payload.get("metadata", {}),
        }

    def receive_batch(self, payloads: list) -> list:
        """
        Receive multiple webhook feedback records.
        """

        if not isinstance(payloads, list):
            raise ValueError("Batch payload must be a list.")

        return [
            self.receive(payload)
            for payload in payloads
        ]