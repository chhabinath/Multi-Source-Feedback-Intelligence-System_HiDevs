from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Feedback


class FeedbackRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: Dict) -> Feedback:
        """
        Insert a feedback record.
        """

        feedback = Feedback(
            id=data["id"],
            text=data["text"],
            rating=data.get("rating"),
            source=data.get("source", "unknown"),

            sentiment=data.get("sentiment"),
            sentiment_score=data.get("sentiment_score"),
            sentiment_confidence=data.get(
                "sentiment_confidence"
            ),

            category=data.get("category"),
            category_score=data.get("category_score"),
            category_confidence=data.get(
                "category_confidence"
            ),
            category_scores=data.get(
                "category_scores"
            ),

            priority=data.get("priority"),
            priority_score=data.get(
                "priority_score"
            ),
            urgent=data.get("urgent", False),
            urgent_keywords=data.get(
                "urgent_keywords"
            ),

            metadata_json=data.get("metadata"),
        )

        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return feedback

    def create_many(
        self,
        records: List[Dict],
    ) -> int:
        """
        Insert multiple feedback records.

        Existing IDs are skipped.
        """

        if not records:
            return 0

        ids = [
            record["id"]
            for record in records
        ]

        existing = set(
            self.db.scalars(
                select(Feedback.id).where(
                    Feedback.id.in_(ids)
                )
            ).all()
        )

        new_records = [
            record
            for record in records
            if record["id"] not in existing
        ]

        if not new_records:
            return 0

        objects = [
            Feedback(
                id=data["id"],
                text=data["text"],
                rating=data.get("rating"),
                source=data.get(
                    "source",
                    "unknown",
                ),

                sentiment=data.get(
                    "sentiment"
                ),
                sentiment_score=data.get(
                    "sentiment_score"
                ),
                sentiment_confidence=data.get(
                    "sentiment_confidence"
                ),

                category=data.get(
                    "category"
                ),
                category_score=data.get(
                    "category_score"
                ),
                category_confidence=data.get(
                    "category_confidence"
                ),
                category_scores=data.get(
                    "category_scores"
                ),

                priority=data.get(
                    "priority"
                ),
                priority_score=data.get(
                    "priority_score"
                ),
                urgent=data.get(
                    "urgent",
                    False,
                ),
                urgent_keywords=data.get(
                    "urgent_keywords"
                ),

                metadata_json=data.get(
                    "metadata"
                ),
            )
            for data in new_records
        ]

        self.db.add_all(objects)
        self.db.commit()

        return len(objects)

    def get_by_id(
        self,
        feedback_id: str,
    ) -> Optional[Feedback]:

        return self.db.get(
            Feedback,
            feedback_id,
        )

    def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Feedback]:

        statement = (
            select(Feedback)
            .order_by(
                Feedback.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def count(self) -> int:
        from sqlalchemy import func

        statement = select(
            func.count(Feedback.id)
        )

        return self.db.scalar(statement) or 0