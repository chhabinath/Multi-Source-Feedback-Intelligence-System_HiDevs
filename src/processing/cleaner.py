from typing import Dict


class TextCleaner:
    """
    Cleans and normalizes feedback text.
    """

    def clean(self, text: str) -> str:
        """
        Normalize feedback text.
        """

        if not text:
            return ""

        text = str(text)

        # Normalize whitespace
        text = " ".join(text.split())

        # Lowercase
        text = text.lower().strip()

        return text

    def clean_feedback(self, feedback: Dict) -> Dict:
        """
        Return a cleaned copy of a feedback record.
        """

        result = feedback.copy()

        result["text"] = self.clean(
            feedback.get("text", "")
        )

        return result