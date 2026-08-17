import re
from email import message_from_string
from typing import Dict, List


class EmailFeedbackParser:
    """
    Parses customer feedback from email messages.
    """

    def parse(self, raw_email: str) -> Dict:
        """
        Parse a raw email into a normalized feedback record.
        """

        if not raw_email or not raw_email.strip():
            raise ValueError("Email content is required.")

        message = message_from_string(raw_email)

        subject = message.get("Subject", "")
        sender = message.get("From", "")

        body = self._extract_body(message)

        if not body.strip():
            raise ValueError("Email body is empty.")

        rating = self._extract_rating(subject, body)

        return {
            "id": self._generate_id(sender, subject),
            "text": body.strip(),
            "rating": rating,
            "source": "email",
            "metadata": {
                "sender": sender,
                "subject": subject,
            },
        }

    def parse_batch(
        self,
        emails: List[str],
    ) -> List[Dict]:
        """
        Parse multiple raw emails.
        """

        return [
            self.parse(email)
            for email in emails
        ]

    @staticmethod
    def _extract_body(message) -> str:
        """
        Extract plain-text content from an email.
        """

        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    payload = part.get_payload(
                        decode=True
                    )

                    if payload:
                        return payload.decode(
                            "utf-8",
                            errors="replace",
                        )

            return ""

        payload = message.get_payload(
            decode=True
        )

        if isinstance(payload, bytes):
            return payload.decode(
                "utf-8",
                errors="replace",
            )

        return str(payload or "")

    @staticmethod
    def _extract_rating(
        subject: str,
        body: str,
    ):
        """
        Extract a 1-5 rating when explicitly provided.

        Supported examples:
            Rating: 5
            Rating 4
            5/5
        """

        text = f"{subject} {body}"

        patterns = [
            r"rating\s*[:\-]?\s*([1-5])",
            r"\b([1-5])\s*/\s*5\b",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                return int(match.group(1))

        return None

    @staticmethod
    def _generate_id(
        sender: str,
        subject: str,
    ) -> str:
        """
        Generate a deterministic email feedback ID.
        """

        import hashlib

        value = f"{sender}:{subject}"

        digest = hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()[:12]

        return f"email_{digest}"