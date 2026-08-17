import os
from pathlib import Path

from dotenv import load_dotenv


# --------------------------------------------------
# Project root
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env from project root
load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Central application configuration.

    All environment-specific configuration is loaded
    from the .env file with sensible defaults.
    """

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Feedback Intelligence System",
    )

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development",
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "false",
    ).lower() == "true"

    # --------------------------------------------------
    # Data
    # --------------------------------------------------

    INPUT_DATA_PATH: Path = BASE_DIR / os.getenv(
        "INPUT_DATA_PATH",
        "data/Updated_App_Details_Reviews_Combined.csv",
    )

    PROCESSED_DATA_PATH: Path = BASE_DIR / os.getenv(
        "PROCESSED_DATA_PATH",
        "data/processed_feedback.json",
    )

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/feedback.db",
    )

    # --------------------------------------------------
    # Processing
    # --------------------------------------------------

    BATCH_SIZE: int = int(
        os.getenv(
            "BATCH_SIZE",
            "32",
        )
    )

    ML_LIMIT: int = int(
        os.getenv(
            "ML_LIMIT",
            "5000",
        )
    )

    # --------------------------------------------------
    # Machine Learning
    # --------------------------------------------------

    ML_MODEL_NAME: str = os.getenv(
        "ML_MODEL_NAME",
        "valhalla/distilbart-mnli-12-3",
    )

    # --------------------------------------------------
    # FastAPI
    # --------------------------------------------------

    API_HOST: str = os.getenv(
        "API_HOST",
        "0.0.0.0",
    )

    API_PORT: int = int(
        os.getenv(
            "API_PORT",
            "8000",
        )
    )

    # --------------------------------------------------
    # Streamlit
    # --------------------------------------------------

    DASHBOARD_PORT: int = int(
        os.getenv(
            "DASHBOARD_PORT",
            "8501",
        )
    )


settings = Settings()