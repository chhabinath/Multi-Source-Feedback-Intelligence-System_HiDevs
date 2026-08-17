import csv
from typing import Dict, List


class CSVFeedbackImporter:
    """
    Imports feedback from CSV files.

    Supports the project's real app-review dataset as well as
    the simpler sample CSV format.
    """

    def load(self, filepath: str) -> List[Dict]:
        feedback = []

        with open(filepath, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV file has no header.")

            fields = set(reader.fieldnames)

            # Real project dataset
            if {
                "rev_app_id",
                "CleanedStop_review_body1",
                "current_rating",
            }.issubset(fields):
                return self._load_project_dataset(reader)

            # Generic/sample dataset
            if {"id", "text"}.issubset(fields):
                return self._load_generic_dataset(reader)

            raise ValueError(
                "Unsupported CSV format. Required columns were not found."
            )

    def _load_project_dataset(self, reader) -> List[Dict]:
        feedback = []

        for row_number, row in enumerate(reader, start=2):
            text = (row.get("CleanedStop_review_body1") or "").strip()

            if not text:
                continue

            try:
                rating = int(float(row["current_rating"]))
            except (TypeError, ValueError):
                rating = None

            feedback.append({
                "id": f"review_{row_number}",
                "text": text,
                "rating": rating,
                "source": "app_store_dataset",
                "metadata": {
                    "app_id": row.get("rev_app_id"),
                    "dataset_category": row.get(
                        "Main_Category_UniqueVal"
                    ),
                    "required_android_version": row.get(
                        "required_android_version"
                    ),
                    "total_reviews": row.get("TotNumRev"),
                    "installs": row.get("Installs"),
                    "app_average_rating": row.get(
                        "TotalAverageRating"
                    ),
                    "row": row_number,
                },
            })

        return feedback

    def _load_generic_dataset(self, reader) -> List[Dict]:
        feedback = []

        for row_number, row in enumerate(reader, start=2):
            text = (row.get("text") or "").strip()

            if not text:
                continue

            rating = row.get("rating")

            try:
                rating = int(float(rating)) if rating else None
            except (TypeError, ValueError):
                rating = None

            feedback.append({
                "id": row.get("id") or f"csv_{row_number}",
                "text": text,
                "rating": rating,
                "source": row.get("source") or "csv",
                "metadata": {
                    "row": row_number,
                },
            })

        return feedback