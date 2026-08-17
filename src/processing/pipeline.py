from typing import Dict, List

from src.processing.cleaner import TextCleaner
from src.processing.analyzer import SentimentAnalyzer
from src.processing.categorizer import FeedbackCategorizer
from src.processing.priority import PriorityScorer


class FeedbackPipeline:
    """
    Runs the complete feedback-processing pipeline.

    Processing order:
        1. Clean text
        2. Analyze sentiment
        3. Categorize feedback
        4. Calculate priority
    """

    def __init__(self):
        self.cleaner = TextCleaner()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.categorizer = FeedbackCategorizer()
        self.priority_scorer = PriorityScorer()

    def process(self, feedback: Dict) -> Dict:
        """
        Process one feedback record through all stages.

        The original feedback dictionary is not modified.
        """

        result = self.cleaner.clean_feedback(feedback)

        result = self.sentiment_analyzer.analyze_feedback(result)

        result = self.categorizer.categorize_feedback(result)

        result = self.priority_scorer.score_feedback(result)

        return result

    def process_batch(
        self,
        feedback_list: List[Dict],
        batch_size: int = 16,
    ) -> List[Dict]:
        """
        Process multiple feedback records efficiently.

        Transformer-based classification is performed in batches.
        """

        if not feedback_list:
            return []

        # 1. Clean
        cleaned = [
            self.cleaner.clean_feedback(feedback)
            for feedback in feedback_list
        ]

        # 2. Sentiment
        analyzed = [
            self.sentiment_analyzer.analyze_feedback(feedback)
            for feedback in cleaned
        ]

        # 3. ML categorization in batches
        categorized = self.categorizer.categorize_batch(
            analyzed,
            batch_size=batch_size,
        )

        # 4. Priority
        processed = [
            self.priority_scorer.score_feedback(feedback)
            for feedback in categorized
        ]

        return processed