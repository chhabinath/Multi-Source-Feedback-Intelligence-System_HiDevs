from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.middleware import log_request
from src.database.database import get_db
from src.database.repository import FeedbackRepository
from src.processing.pipeline import FeedbackPipeline


app = FastAPI(
    title="Feedback Intelligence API",
    description="API for collecting and analyzing customer feedback",
    version="1.0.0",
)

app.middleware("http")(log_request)

pipeline = FeedbackPipeline()


# ============================================================
# Request / Response Models
# ============================================================

class FeedbackRequest(BaseModel):
    id: str
    text: str
    rating: int | None = None
    source: str = "api"


class FeedbackResponse(BaseModel):
    id: str
    text: str
    rating: int | None = None
    source: str

    sentiment: str | None = None
    sentiment_score: float | None = None
    sentiment_confidence: float | None = None

    category: str | None = None
    category_score: float | None = None
    category_confidence: float | None = None

    priority: str | None = None
    priority_score: int | None = None

    urgent: bool = False
    urgent_keywords: List[str] = []


# ============================================================
# Health
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "feedback-intelligence-api",
    }


# ============================================================
# Create Feedback
# ============================================================

@app.post(
    "/feedback",
    response_model=FeedbackResponse,
)
def create_feedback(
    feedback: FeedbackRequest,
    db: Session = Depends(get_db),
):
    """
    Receive feedback, analyze it, and store the
    processed result in the database.
    """

    repository = FeedbackRepository(db)

    # Check whether ID already exists.
    existing = repository.get_by_id(feedback.id)

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Feedback with this ID already exists.",
        )

    # Convert request to dictionary.
    raw_feedback = feedback.model_dump()

    # Run the complete processing pipeline.
    processed_feedback = pipeline.process(
        raw_feedback
    )

    # Store in database.
    repository.create(
        processed_feedback
    )

    return processed_feedback


# ============================================================
# Get All Feedback
# ============================================================

@app.get("/feedback")
def get_feedback(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Return processed feedback from the database.
    """

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="offset cannot be negative",
        )

    repository = FeedbackRepository(db)

    records = repository.get_all(
        limit=limit,
        offset=offset,
    )

    return {
        "count": repository.count(),
        "limit": limit,
        "offset": offset,
        "feedback": [
            {
                "id": item.id,
                "text": item.text,
                "rating": item.rating,
                "source": item.source,
                "sentiment": item.sentiment,
                "sentiment_score": item.sentiment_score,
                "sentiment_confidence": item.sentiment_confidence,
                "category": item.category,
                "category_score": item.category_score,
                "category_confidence": item.category_confidence,
                "category_scores": item.category_scores,
                "priority": item.priority,
                "priority_score": item.priority_score,
                "urgent": item.urgent,
                "urgent_keywords": item.urgent_keywords,
                "metadata": item.metadata_json,
                "created_at": item.created_at,
            }
            for item in records
        ],
    }


# ============================================================
# Get Feedback By ID
# ============================================================

@app.get("/feedback/{feedback_id}")
def get_feedback_by_id(
    feedback_id: str,
    db: Session = Depends(get_db),
):
    """
    Return one feedback record from the database.
    """

    repository = FeedbackRepository(db)

    feedback = repository.get_by_id(
        feedback_id
    )

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found",
        )

    return {
        "id": feedback.id,
        "text": feedback.text,
        "rating": feedback.rating,
        "source": feedback.source,
        "sentiment": feedback.sentiment,
        "sentiment_score": feedback.sentiment_score,
        "sentiment_confidence": feedback.sentiment_confidence,
        "category": feedback.category,
        "category_score": feedback.category_score,
        "category_confidence": feedback.category_confidence,
        "category_scores": feedback.category_scores,
        "priority": feedback.priority,
        "priority_score": feedback.priority_score,
        "urgent": feedback.urgent,
        "urgent_keywords": feedback.urgent_keywords,
        "metadata": feedback.metadata_json,
        "created_at": feedback.created_at,
    }