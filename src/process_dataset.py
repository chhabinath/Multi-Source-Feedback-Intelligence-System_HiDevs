from src.processing.batch_processor import BatchProcessor


def main():
    processor = BatchProcessor()

    processor.process_csv()


if __name__ == "__main__":
    main()