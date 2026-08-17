
# 📊 Multi-Source Feedback Intelligence System

An end-to-end customer feedback intelligence platform that collects, processes, analyzes, stores, and visualizes customer feedback from multiple sources.

The system combines **FastAPI**, **Streamlit**, **SQLite**, **SQLAlchemy**, **VADER Sentiment Analysis**, and a **Hugging Face zero-shot classification model** to transform raw customer feedback into actionable insights.

---

## 🚀 Overview

Customer feedback is often distributed across application reviews, surveys, APIs, and other sources. Manually analyzing thousands of reviews is slow, inconsistent, and difficult to scale.

This project provides an automated pipeline that:

- Imports customer feedback from CSV files
- Cleans and normalizes feedback text
- Performs sentiment analysis
- Automatically categorizes feedback using zero-shot NLP classification
- Calculates feedback priority
- Detects urgent feedback
- Stores processed feedback in SQLite
- Provides REST APIs through FastAPI
- Provides an interactive analytics dashboard through Streamlit
- Supports configurable processing through environment variables
- Provides reusable database repositories
- Supports batch processing for large datasets



# 🏗️ Architecture

```text
                    ┌──────────────────────────────┐
                    │        Feedback Sources      │
                    │                              │
                    │  CSV / API / Survey / etc.  │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       CSV Importer           │
                    │   CSVFeedbackImporter         │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       Batch Processor         │
                    │                              │
                    │  • Text Cleaning             │
                    │  • Sentiment Analysis        │
                    │  • ML Classification         │
                    │  • Priority Scoring          │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │           SQLite             │
                    │        feedback.db           │
                    │                              │
                    │       SQLAlchemy ORM         │
                    └──────────────┬───────────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
            ┌─────────────────┐        ┌─────────────────┐
            │    FastAPI      │        │   Streamlit     │
            │                 │        │                 │
            │ REST API        │        │ Analytics       │
            │ Data ingestion  │        │ Dashboard       │
            │ Query feedback  │        │ Filtering       │
            └─────────────────┘        └─────────────────┘
````

SQLite acts as the shared persistence layer.

Both FastAPI and Streamlit operate on the same processed feedback database.

---

# ✨ Key Features

## 1. Multi-Source Feedback Ingestion

The ingestion layer supports structured customer feedback from CSV datasets.

The project currently supports:

* Application review datasets
* Generic feedback CSV files
* API-submitted feedback

The CSV importer automatically detects supported CSV formats.

---

## 2. Text Cleaning

Raw feedback is cleaned before analysis.

The processing pipeline handles:

* Empty feedback
* Text normalization
* Whitespace cleanup
* Basic text preprocessing

This ensures downstream NLP components receive consistent input.

---

## 3. Sentiment Analysis

The system uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** for sentiment analysis.

Each feedback record receives:

```text
sentiment
sentiment_score
sentiment_confidence
```

Possible sentiment labels:

```text
positive
negative
neutral
```

The VADER compound score is used to determine the overall sentiment.

---

## 4. Automatic Feedback Categorization

The project uses a Hugging Face zero-shot classification model:

```text
valhalla/distilbart-mnli-12-3
```

No manually labeled training dataset is required.

The default categories include:

```text
bug
payment
login
performance
user interface
feature request
complaint
praise
other
```

Each prediction includes:

```text
category
category_score
category_confidence
category_scores
```

The model can be changed through `.env` without modifying application code.

---

## 5. Priority Scoring

Feedback is analyzed for business impact and urgency.

Each record can contain:

```text
priority
priority_score
urgent
urgent_keywords
```

This allows the system to identify feedback that may require immediate attention.

---

## 6. Batch Processing

Large datasets are processed in configurable batches.

Example:

```text
BATCH_SIZE=32
ML_LIMIT=5000
```

The batch processor:

1. Loads feedback
2. Processes records in batches
3. Cleans text
4. Performs sentiment analysis
5. Performs ML classification
6. Calculates priority
7. Stores results
8. Creates checkpoints during processing

Checkpointing prevents the entire processing output from being lost if processing is interrupted.

---

# 🗄️ Database

The system uses:

```text
SQLite
```

with:

```text
SQLAlchemy
```

as the ORM.

Database file:

```text
data/feedback.db
```

The main database model is:

```text
Feedback
```

Stored information includes:

* ID
* Feedback text
* Rating
* Source
* Sentiment
* Sentiment score
* Sentiment confidence
* Category
* Category score
* Category confidence
* Category scores
* Priority
* Priority score
* Urgent flag
* Urgent keywords
* Metadata
* Creation timestamp

---

# 🔌 FastAPI

FastAPI provides the backend REST API.

## Start the API

From the project root:

```bash
uvicorn src.api.endpoints:app --reload
```

The API will run on:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Checks whether the API is running.

Example response:

```json
{
  "status": "healthy",
  "service": "feedback-intelligence-api"
}
```

---

### Create Feedback

```http
POST /feedback
```

Receives new feedback, processes it, and stores it in the database.

Example request:

```json
{
  "id": "api_test_002",
  "text": "payment keeps failing when i try to buy something",
  "rating": 2
}
```

The system analyzes the feedback and returns fields such as:

```json
{
  "id": "api_test_002",
  "text": "payment keeps failing when i try to buy something",
  "rating": 2,
  "sentiment": "negative",
  "sentiment_score": -0.5106,
  "category": "complaint",
  "priority": "critical",
  "priority_score": 12,
  "urgent": true
}
```

---

### Get Feedback

```http
GET /feedback
```

Returns stored feedback records.

---

### Get Feedback by ID

```http
GET /feedback/{feedback_id}
```

Returns a specific feedback record.

Example:

```text
GET /feedback/api_test_002
```

---

# 📈 Streamlit Dashboard

The Streamlit dashboard provides an interactive interface for exploring processed feedback.

The dashboard reads from the SQLite database.

## Start Streamlit

From the project root:

```bash
PYTHONPATH=. streamlit run src/dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

## Dashboard Features

The dashboard provides:

### KPI Metrics

* Total feedback
* Average rating
* Average sentiment
* Negative feedback count
* Critical issue count

### Visualizations

* Sentiment distribution
* Category distribution
* Priority distribution

### Filtering

Users can filter feedback by:

* Source
* Sentiment
* Category
* Priority

### Issue Analysis

The dashboard identifies:

* Most common feedback categories
* Negative feedback counts
* Negative feedback rates

### Critical Feedback

Critical feedback is displayed separately for quick investigation.

### Recent Feedback

Recent processed feedback can be inspected directly from the dashboard.

---

# ⚙️ Configuration

Application configuration is centralized using environment variables.

Configuration is loaded from:

```text
.env
```

Example:

```env
APP_NAME=Feedback Intelligence System
APP_ENV=development
DEBUG=true

INPUT_DATA_PATH=data/Updated_App_Details_Reviews_Combined.csv
PROCESSED_DATA_PATH=data/processed_feedback.json

BATCH_SIZE=32
ML_LIMIT=5000

ML_MODEL_NAME=valhalla/distilbart-mnli-12-3

DATABASE_URL=sqlite:///./data/feedback.db

API_HOST=0.0.0.0
API_PORT=8000

DASHBOARD_PORT=8501
```

---

# 🔐 Environment Variables

| Variable              | Description                       | Example                                         |
| --------------------- | --------------------------------- | ----------------------------------------------- |
| `APP_NAME`            | Application name                  | `Feedback Intelligence System`                  |
| `APP_ENV`             | Application environment           | `development`                                   |
| `DEBUG`               | Enable debug mode                 | `true`                                          |
| `INPUT_DATA_PATH`     | Input CSV location                | `data/Updated_App_Details_Reviews_Combined.csv` |
| `PROCESSED_DATA_PATH` | Optional JSON export path         | `data/processed_feedback.json`                  |
| `BATCH_SIZE`          | Processing batch size             | `32`                                            |
| `ML_LIMIT`            | Maximum records for ML processing | `5000`                                          |
| `ML_MODEL_NAME`       | Hugging Face model                | `valhalla/distilbart-mnli-12-3`                 |
| `DATABASE_URL`        | Database connection URL           | `sqlite:///./data/feedback.db`                  |
| `API_HOST`            | FastAPI host                      | `0.0.0.0`                                       |
| `API_PORT`            | FastAPI port                      | `8000`                                          |
| `DASHBOARD_PORT`      | Streamlit port                    | `8501`                                          |

---

# 📁 Project Structure

```text
Multi-Source-Feedback-Intelligence-System/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── data/
│   ├── Updated_App_Details_Reviews_Combined.csv
│   ├── feedback.db
│   └── processed_feedback.json
│
├── docs/
│
├── deployment/
│
├── docker/
│
├── tests/
│   ├── cleaner-test.py
│   ├── test_ai_prompts.py
│   ├── test_alerts.py
│   ├── test_categorizer_manual.py
│   ├── test_email_parser.py
│   ├── test_integrations.py
│   ├── test_ml_models.py
│   ├── test_priority_manual.py
│   ├── test_reports.py
│   ├── test_trend_detector.py
│   ├── test_webhooks.py
│   └── testing.py
│
└── src/
    │
    ├── __init__.py
    ├── dashboard.py
    ├── process_dataset.py
    │
    ├── actions/
    │   ├── alerts.py
    │   ├── integrations.py
    │   └── reports.py
    │
    ├── api/
    │   ├── endpoints.py
    │   └── middleware.py
    │
    ├── config/
    │   └── settings.py
    │
    ├── database/
    │   ├── database.py
    │   ├── init_db.py
    │   ├── models.py
    │   └── repository.py
    │
    ├── ingestion/
    │   ├── aggregator.py
    │   ├── api_clients.py
    │   ├── email_parser.py
    │   └── webhooks.py
    │
    ├── intelligence/
    │   ├── ai_prompts.py
    │   ├── ml_models.py
    │   └── trend_detector.py
    │
    └── processing/
        ├── analyzer.py
        ├── batch_processor.py
        ├── cleaner.py
        ├── categorizer.py
        ├── pipeline.py
        └── priority.py
```

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd Multi-Source-Feedback-Intelligence-System
```

---

## 2. Create a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create:

```text
.env
```

or copy the example:

```bash
cp .env.example .env
```

Update the values as required.

---

# 🗃️ Initialize the Database

Run:

```bash
python -m src.database.init_db
```

Expected output:

```text
Database initialized successfully.
```

The database will be created at:

```text
data/feedback.db
```

---

# 🔄 Process the Dataset

The main input dataset is:

```text
data/Updated_App_Details_Reviews_Combined.csv
```

Run:

```bash
python -m src.process_dataset
```

The batch processor will:

```text
Load CSV
   ↓
Clean feedback
   ↓
Analyze sentiment
   ↓
Classify feedback
   ↓
Calculate priority
   ↓
Store processed records
```

Processing parameters can be changed through `.env`.

For example:

```env
BATCH_SIZE=64
ML_LIMIT=1000
```

No Python source code changes are required.

---

# 🧪 Verify the Database

Check the number of stored records:

```bash
python -c "from src.database.database import SessionLocal; from src.database.repository import FeedbackRepository; db=SessionLocal(); print('Records:', FeedbackRepository(db).count()); db.close()"
```

Inspect a few records:

```bash
python -c "from src.database.database import SessionLocal; from src.database.repository import FeedbackRepository; db=SessionLocal(); rows=FeedbackRepository(db).get_all(limit=5); [(print(r.id, '|', r.category, '|', r.sentiment, '|', r.priority)) for r in rows]; db.close()"
```

---

# ▶️ Running the Complete Application

The application has two main interfaces.

## Terminal 1 — FastAPI

```bash
uvicorn src.api.endpoints:app --reload
```

API:

```text
http://localhost:8000
```

Documentation:

```text
http://localhost:8000/docs
```

---

## Terminal 2 — Streamlit

```bash
PYTHONPATH=. streamlit run src/dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

# 🔁 End-to-End Workflow

A typical workflow is:

```text
1. Raw CSV Dataset
        │
        ▼
2. CSVFeedbackImporter
        │
        ▼
3. BatchProcessor
        │
        ├── TextCleaner
        │
        ├── SentimentAnalyzer
        │
        ├── FeedbackMLModel
        │
        └── PriorityScorer
        │
        ▼
4. SQLite Database
        │
        ├───────────────┐
        ▼               ▼
5. FastAPI        6. Streamlit
        │               │
        ▼               ▼
   REST API       Analytics Dashboard
```

---

# 🧠 Technology Stack

| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| Python                    | Core application language       |
| FastAPI                   | REST API backend                |
| Streamlit                 | Interactive analytics dashboard |
| SQLite                    | Persistent database             |
| SQLAlchemy                | ORM/database abstraction        |
| Pandas                    | Data processing and analysis    |
| VADER                     | Sentiment analysis              |
| Hugging Face Transformers | Zero-shot classification        |
| PyTorch                   | ML model execution              |
| Pydantic                  | API request/response validation |
| python-dotenv             | Environment configuration       |
| Pytest                    | Testing                         |

---

# 📊 Example Use Case

A customer submits:

```text
"Payment keeps failing when I try to buy something."
```

The system can transform it into structured intelligence:

```json
{
  "sentiment": "negative",
  "sentiment_score": -0.5106,
  "category": "complaint",
  "category_score": 0.3575,
  "priority": "critical",
  "priority_score": 12,
  "urgent": true
}
```

This allows a business team to quickly identify:

* What customers are complaining about
* Whether feedback is positive or negative
* Which areas require attention
* Which issues are potentially critical
* Which categories generate the most negative feedback

---

# 🧪 Testing

Run the test suite:

```bash
pytest
```

Individual tests can also be executed:

```bash
pytest tests/test_ml_models.py
```

```bash
pytest tests/test_trend_detector.py
```

```bash
pytest tests/test_alerts.py
```

---

# 🔍 Health Check

Once FastAPI is running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "feedback-intelligence-api"
}
```

---

# 📌 Design Principles

The project follows several architectural principles:

### Separation of Concerns

Different responsibilities are separated into:

```text
ingestion
processing
intelligence
database
api
dashboard
actions
configuration
```

### Configuration Driven

Runtime configuration is controlled through `.env`.

### Reusable Components

Processing components such as sentiment analysis, categorization, cleaning, and priority scoring are implemented independently.

### Database Abstraction

Database operations are handled through a repository layer rather than directly throughout the application.

### Batch Processing

Large datasets are processed in batches to control memory and ML inference workload.

### Shared Persistence

FastAPI and Streamlit use the same SQLite database rather than maintaining separate application data stores.

---

# ⚠️ Performance Considerations

The zero-shot classification model is computationally expensive when executed on CPU.

For large datasets:

* Use an appropriate `BATCH_SIZE`
* Limit ML processing with `ML_LIMIT`
* Use checkpointing
* Prefer GPU acceleration when available
* Avoid loading the Transformer model repeatedly

The model is loaded once and reused by the batch processor.

For example:

```env
BATCH_SIZE=32
ML_LIMIT=5000
```

---

# 🔒 Security

Do not commit sensitive environment variables.

The `.env` file should be excluded from Git:

```text
.env
```

Use:

```text
.env.example
```

for safe configuration examples.

Never place:

* API keys
* passwords
* tokens
* production credentials

inside source code or committed configuration files.

---

# 🚧 Future Improvements

Potential future enhancements include:

* PostgreSQL support for production deployments
* Redis caching
* Background task processing
* Celery/RQ-based asynchronous ML processing
* Authentication and authorization
* Role-based dashboard access
* Real-time feedback ingestion
* Email and webhook integrations
* Advanced trend detection
* Automated alerting
* LLM-powered feedback summarization
* Topic clustering
* Product-level analytics
* Deployment using Docker
* Cloud deployment
* GPU-based inference

---

# 👨‍💻 Development

The project is designed to allow individual components to be developed and tested independently.

For example:

```python
from src.processing.analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

result = analyzer.analyze(
    "The application is excellent."
)

print(result)
```

Similarly, the database repository can be used independently:

```python
from src.database.database import SessionLocal
from src.database.repository import FeedbackRepository

db = SessionLocal()

repository = FeedbackRepository(db)

print(repository.count())

db.close()
```

---

# 📜 License

This project is intended for educational, demonstration, and internship/project evaluation purposes.

---

# 👤 Author

**Chhabinath**

AI/ML Engineer | Java Backend Developer

---

# ⭐ Project Summary

The **Multi-Source Feedback Intelligence System** converts unstructured customer feedback into structured business intelligence.

It combines:

```text
Data Ingestion
      +
NLP Sentiment Analysis
      +
Zero-Shot ML Classification
      +
Priority Detection
      +
Persistent Database
      +
REST API
      +
Interactive Dashboard
```

The result is an end-to-end feedback intelligence platform capable of processing large volumes of customer feedback and presenting the results in a form that can be consumed by both applications and business users.


