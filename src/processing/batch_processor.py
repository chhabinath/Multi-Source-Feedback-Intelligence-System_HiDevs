from pathlib import Path
import json
from typing import Dict, List, Optional

from src.config.settings import settings
from src.ingestion.api_clients import CSVFeedbackImporter
from src.processing.cleaner import TextCleaner
from src.processing.analyzer import SentimentAnalyzer
from src.processing.priority import PriorityScorer
from src.intelligence.ml_models import FeedbackMLModel


class BatchProcessor:
    """
    Process feedback efficiently in batches.

    The expensive Hugging Face zero-shot model is loaded once
    and reused for all batches.
    """

    def __init__(
        self,
        batch_size: Optional[int] = None,
    ):
        self.importer = CSVFeedbackImporter()

        self.batch_size = (
            batch_size
            if batch_size is not None
            else settings.BATCH_SIZE
        )

        self.cleaner = TextCleaner()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.priority_scorer = PriorityScorer()

        # Load Transformer only once.
        self.ml_model = FeedbackMLModel()

    def process_csv(
        self,
        input_path: Optional[str] = None,
        output_path: Optional[str] = None,
        ml_limit: Optional[int] = None,
    ) -> List[Dict]:
        """
        Process the configured CSV dataset.

        Arguments are optional. If omitted, values from
        .env are used.
        """

        input_path = (
            input_path
            or str(settings.INPUT_DATA_PATH)
        )

        output_path = (
            output_path
            or str(settings.PROCESSED_DATA_PATH)
        )

        ml_limit = (
            ml_limit
            if ml_limit is not None
            else settings.ML_LIMIT
        )

        feedback = self.importer.load(
            input_path
        )

        total = len(feedback)

        print(
            f"Loaded {total:,} feedback records"
        )

        print(
            f"ML classification limit: "
            f"{ml_limit:,}"
        )

        limit = min(
            ml_limit,
            total,
        )

        feedback = feedback[:limit]

        processed: List[Dict] = []

        for start in range(
            0,
            limit,
            self.batch_size,
        ):

            end = min(
                start + self.batch_size,
                limit,
            )

            batch = feedback[
                start:end
            ]

            print(
                f"Processing {start + 1:,}-"
                f"{end:,} of {limit:,}"
            )

            # --------------------------------------------------
            # 1. Clean
            # --------------------------------------------------

            cleaned_batch = [
                self.cleaner.clean_feedback(
                    item
                )
                for item in batch
            ]

            # --------------------------------------------------
            # 2. Sentiment
            # --------------------------------------------------

            sentiment_batch = [
                self.sentiment_analyzer.analyze_feedback(
                    item
                )
                for item in cleaned_batch
            ]

            # --------------------------------------------------
            # 3. ML classification
            # --------------------------------------------------

            texts = [
                item.get("text", "")
                for item in sentiment_batch
            ]

            ml_results = (
                self.ml_model.classify_batch(
                    texts,
                    batch_size=self.batch_size,
                )
            )

            # --------------------------------------------------
            # 4. Attach ML results
            # --------------------------------------------------

            category_batch = []

            for item, ml_result in zip(
                sentiment_batch,
                ml_results,
            ):

                result = dict(item)

                result["category"] = (
                    ml_result["category"]
                )

                result["category_score"] = (
                    ml_result["confidence"]
                )

                result["category_confidence"] = (
                    ml_result["confidence"]
                )

                result["category_scores"] = (
                    ml_result["scores"]
                )

                category_batch.append(
                    result
                )

            # --------------------------------------------------
            # 5. Priority
            # --------------------------------------------------

            final_batch = [
                self.priority_scorer.score_feedback(
                    item
                )
                for item in category_batch
            ]

            processed.extend(
                final_batch
            )

            # --------------------------------------------------
            # 6. Checkpoint
            # --------------------------------------------------

            self._save(
                processed,
                output_path,
            )

            print(
                f"Checkpoint saved: "
                f"{len(processed):,} records"
            )

        print()
        print(
            f"Completed: "
            f"{len(processed):,} records"
        )

        print(
            f"Output: {output_path}"
        )

        return processed

    @staticmethod
    def _save(
        data: List[Dict],
        output_path: str,
    ) -> None:
        """
        Save processed data atomically.
        """

        path = Path(
            output_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path = path.with_suffix(
            path.suffix + ".tmp"
        )

        with temporary_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )

        # Atomic replacement.
        temporary_path.replace(
            path
        )

    @staticmethod
    def load_processed(
        path: Optional[str] = None,
    ) -> List[Dict]:
        """
        Load previously processed feedback.
        """

        path = (
            path
            or str(settings.PROCESSED_DATA_PATH)
        )

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Processed data not found: {path}"
            )

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)