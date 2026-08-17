import streamlit as st
import pandas as pd

from src.config.settings import settings
from src.database.database import SessionLocal
from src.database.repository import FeedbackRepository


st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="📊",
    layout="wide",
)


@st.cache_data(ttl=10)
def load_data() -> pd.DataFrame:
    """
    Load feedback directly from SQLite.
    """

    db = SessionLocal()

    try:
        repository = FeedbackRepository(db)

        # Load all records.
        # Increase this if your dataset becomes larger.
        records = repository.get_all(
            limit=10000,
            offset=0,
        )

        if not records:
            return pd.DataFrame()

        data = []

        for feedback in records:
            data.append(
                {
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
            )

        return pd.DataFrame(data)

    finally:
        db.close()


df = load_data()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 Feedback Intelligence System")

st.caption(
    "Multi-source customer feedback analysis and intelligence"
)


# --------------------------------------------------
# Database status
# --------------------------------------------------

if df.empty:

    st.error(
        "No feedback records found in the database."
    )

    st.info(
        f"Database: {settings.DATABASE_URL}"
    )

    st.stop()


st.success(
    f"Loaded {len(df):,} feedback records from SQLite."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Filters")


# Source
sources = sorted(
    df["source"]
    .dropna()
    .unique()
    .tolist()
)

selected_sources = st.sidebar.multiselect(
    "Source",
    sources,
    default=sources,
)


# Sentiment
sentiments = sorted(
    df["sentiment"]
    .dropna()
    .unique()
    .tolist()
)

selected_sentiments = st.sidebar.multiselect(
    "Sentiment",
    sentiments,
    default=sentiments,
)


# Category
categories = sorted(
    df["category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories,
)


# Priority
priorities = sorted(
    df["priority"]
    .dropna()
    .unique()
    .tolist()
)

selected_priorities = st.sidebar.multiselect(
    "Priority",
    priorities,
    default=priorities,
)


# --------------------------------------------------
# Filtering
# --------------------------------------------------

filtered_df = df[
    df["source"].isin(selected_sources)
    & df["sentiment"].isin(selected_sentiments)
    & df["category"].isin(selected_categories)
    & df["priority"].isin(selected_priorities)
].copy()


# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_feedback = len(filtered_df)


if (
    not filtered_df.empty
    and "rating" in filtered_df
):
    average_rating = filtered_df["rating"].mean()
else:
    average_rating = 0


if (
    not filtered_df.empty
    and "sentiment_score" in filtered_df
):
    average_sentiment = (
        filtered_df["sentiment_score"].mean()
    )
else:
    average_sentiment = 0


negative_count = (
    filtered_df["sentiment"] == "negative"
).sum()


critical_count = (
    filtered_df["priority"] == "critical"
).sum()


urgent_count = (
    filtered_df["urgent"] == True
).sum()


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Total Feedback",
    f"{total_feedback:,}",
)


col2.metric(
    "Average Rating",
    f"{average_rating:.2f}",
)


col3.metric(
    "Avg Sentiment",
    f"{average_sentiment:.3f}",
)


col4.metric(
    "Negative Feedback",
    f"{negative_count:,}",
)


col5.metric(
    "Critical Issues",
    f"{critical_count:,}",
)


st.divider()


# --------------------------------------------------
# Sentiment + Category
# --------------------------------------------------

left, right = st.columns(2)


with left:

    st.subheader(
        "Sentiment Distribution"
    )

    sentiment_counts = (
        filtered_df["sentiment"]
        .value_counts()
    )

    st.bar_chart(
        sentiment_counts
    )


with right:

    st.subheader(
        "Category Distribution"
    )

    category_counts = (
        filtered_df["category"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(
        category_counts
    )


# --------------------------------------------------
# Priority
# --------------------------------------------------

st.subheader(
    "Priority Distribution"
)

priority_counts = (
    filtered_df["priority"]
    .value_counts()
)

st.bar_chart(
    priority_counts
)


# --------------------------------------------------
# Top Issues
# --------------------------------------------------

st.subheader(
    "Top Issues"
)


issue_df = (
    filtered_df
    .groupby("category")
    .agg(
        feedback_count=(
            "id",
            "count",
        ),
        negative_count=(
            "sentiment",
            lambda x: (
                x == "negative"
            ).sum(),
        ),
    )
    .reset_index()
)


if not issue_df.empty:

    issue_df["negative_rate"] = (
        issue_df["negative_count"]
        / issue_df["feedback_count"]
    )

    issue_df = issue_df.sort_values(
        "negative_count",
        ascending=False,
    )

    st.dataframe(
        issue_df.head(10),
        use_container_width=True,
    )


# --------------------------------------------------
# Critical Feedback
# --------------------------------------------------

st.subheader(
    "🚨 Critical Feedback"
)


critical_df = filtered_df[
    filtered_df["priority"] == "critical"
]


if critical_df.empty:

    st.info(
        "No critical feedback found."
    )

else:

    display_columns = [
        "id",
        "text",
        "rating",
        "sentiment",
        "category",
        "priority",
        "priority_score",
        "urgent",
    ]

    display_columns = [
        column
        for column in display_columns
        if column in critical_df.columns
    ]

    st.dataframe(
        critical_df[
            display_columns
        ].head(50),
        use_container_width=True,
    )


# --------------------------------------------------
# Recent Feedback
# --------------------------------------------------

st.subheader(
    "📝 Recent Feedback"
)


recent_columns = [
    "id",
    "text",
    "rating",
    "source",
    "sentiment",
    "category",
    "priority",
]


recent_columns = [
    column
    for column in recent_columns
    if column in filtered_df.columns
]


st.dataframe(
    filtered_df[
        recent_columns
    ].head(50),
    use_container_width=True,
)


# --------------------------------------------------
# Database information
# --------------------------------------------------

with st.expander(
    "Database Information"
):

    st.write(
        f"**Database:** "
        f"`{settings.DATABASE_URL}`"
    )

    st.write(
        f"**Records loaded:** "
        f"{len(df):,}"
    )

    st.write(
        f"**Records after filters:** "
        f"{len(filtered_df):,}"
    )

    st.write(
        f"**Model:** "
        f"`{settings.ML_MODEL_NAME}`"
    )

    st.write(
        f"**Environment:** "
        f"`{settings.APP_ENV}`"
    )