from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        default="unknown",
    )

    sentiment: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    sentiment_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sentiment_confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    category_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    category_confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    category_scores: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    priority_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    urgent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    urgent_keywords: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )