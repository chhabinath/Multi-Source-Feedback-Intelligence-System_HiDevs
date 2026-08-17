from typing import Dict, List


class FeedbackAggregator:
    """
    Combines feedback records from multiple ingestion sources
    into one normalized collection.
    """

    def __init__(self):
        self.feedback: List[Dict] = []

    def add(self, feedback: List[Dict]) -> None:
        """
        Add feedback records to the collection.
        """
        if not isinstance(feedback, list):
            raise ValueError("Feedback must be provided as a list.")

        self.feedback.extend(feedback)

    def add_one(self, feedback: Dict) -> None:
        """
        Add a single feedback record.
        """
        if not isinstance(feedback, dict):
            raise ValueError("Feedback must be a dictionary.")

        self.feedback.append(feedback)

    def get_all(self) -> List[Dict]:
        """
        Return all collected feedback.
        """
        return list(self.feedback)

    def get_by_source(self, source: str) -> List[Dict]:
        """
        Return feedback belonging to a specific source.
        """
        return [
            feedback
            for feedback in self.feedback
            if feedback.get("source") == source
        ]

    def count_by_source(self) -> Dict[str, int]:
        """
        Return feedback counts grouped by source.
        """
        counts: Dict[str, int] = {}

        for feedback in self.feedback:
            source = feedback.get("source", "unknown")
            counts[source] = counts.get(source, 0) + 1

        return counts

    def deduplicate(self) -> List[Dict]:
        """
        Remove duplicate feedback records using their IDs.
        """
        unique = {}
        order = []

        for feedback in self.feedback:
            feedback_id = feedback.get("id")

            if feedback_id is None:
                continue

            if feedback_id not in unique:
                unique[feedback_id] = feedback
                order.append(feedback_id)

        self.feedback = [
            unique[feedback_id]
            for feedback_id in order
        ]

        return self.get_all()

    def clear(self) -> None:
        """
        Remove all collected feedback.
        """
        self.feedback.clear()