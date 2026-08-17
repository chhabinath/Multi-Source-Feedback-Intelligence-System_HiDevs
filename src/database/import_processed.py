from src.database.database import SessionLocal, init_db
from src.database.repository import FeedbackRepository
from src.processing.batch_processor import BatchProcessor


def main():
    print("Initializing database...")
    init_db()

    print("Loading processed feedback...")
    records = BatchProcessor.load_processed()

    print(f"Loaded {len(records):,} processed records")

    db = SessionLocal()

    try:
        repository = FeedbackRepository(db)

        inserted = repository.create_many(records)

        print(f"Inserted: {inserted:,} records")
        print(f"Total in database: {repository.count():,}")

    finally:
        db.close()


if __name__ == "__main__":
    main()