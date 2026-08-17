from collections import Counter
from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class ReportGenerator:
    """
    Generates feedback intelligence reports
    and PDF summaries.
    """

    def generate_summary(
        self,
        feedback_list: List[Dict],
    ) -> Dict:
        """
        Generate summary statistics from feedback.
        """

        total = len(feedback_list)

        if total == 0:
            return {
                "total_feedback": 0,
                "average_rating": 0,
                "sentiment_distribution": {},
                "category_distribution": {},
                "priority_distribution": {},
                "top_issues": [],
            }

        ratings = [
            feedback["rating"]
            for feedback in feedback_list
            if isinstance(
                feedback.get("rating"),
                (int, float),
            )
        ]

        average_rating = (
            sum(ratings) / len(ratings)
            if ratings
            else 0
        )

        sentiments = Counter(
            feedback.get(
                "sentiment",
                "unknown",
            )
            for feedback in feedback_list
        )

        categories = Counter(
            feedback.get(
                "category",
                "uncategorized",
            )
            for feedback in feedback_list
        )

        priorities = Counter(
            feedback.get(
                "priority",
                "unknown",
            )
            for feedback in feedback_list
        )

        top_issues = [
            {
                "category": category,
                "count": count,
            }
            for category, count in categories.most_common(5)
        ]

        return {
            "total_feedback": total,
            "average_rating": round(
                average_rating,
                2,
            ),
            "sentiment_distribution": dict(
                sentiments
            ),
            "category_distribution": dict(
                categories
            ),
            "priority_distribution": dict(
                priorities
            ),
            "top_issues": top_issues,
        }

    def generate_pdf(
        self,
        feedback_list: List[Dict],
        output_path: str,
        title: str = "Feedback Intelligence Report",
    ) -> str:
        """
        Generate a PDF report containing:
        - Summary metrics
        - Sentiment distribution
        - Category distribution
        - Top issues
        """

        summary = self.generate_summary(
            feedback_list
        )

        chart_path = self._create_sentiment_chart(
            summary["sentiment_distribution"]
        )

        document = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                title,
                styles["Title"],
            )
        )

        elements.append(
            Spacer(1, 0.2 * inch)
        )

        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                styles["Normal"],
            )
        )

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        summary_table = Table(
            [
                ["Metric", "Value"],
                [
                    "Total Feedback",
                    summary["total_feedback"],
                ],
                [
                    "Average Rating",
                    summary["average_rating"],
                ],
            ],
            colWidths=[3 * inch, 2 * inch],
        )

        summary_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (-1, -1),
                        "CENTER",
                    ),
                ]
            )
        )

        elements.append(summary_table)

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        elements.append(
            Paragraph(
                "Sentiment Distribution",
                styles["Heading2"],
            )
        )

        elements.append(
            Image(
                chart_path,
                width=5.5 * inch,
                height=3.5 * inch,
            )
        )

        elements.append(
            Spacer(1, 0.2 * inch)
        )

        elements.append(
            Paragraph(
                "Top Issues",
                styles["Heading2"],
            )
        )

        issue_rows = [
            ["Category", "Count"]
        ]

        for issue in summary["top_issues"]:
            issue_rows.append(
                [
                    issue["category"],
                    issue["count"],
                ]
            )

        issue_table = Table(
            issue_rows,
            colWidths=[3 * inch, 2 * inch],
        )

        issue_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                ]
            )
        )

        elements.append(issue_table)

        document.build(elements)

        return output_path

    @staticmethod
    def _create_sentiment_chart(
        sentiment_distribution: Dict[str, int],
    ) -> str:
        """
        Create a sentiment distribution chart.
        """

        chart_path = "/tmp/sentiment_distribution.png"

        labels = list(
            sentiment_distribution.keys()
        )

        values = list(
            sentiment_distribution.values()
        )

        plt.figure(figsize=(7, 4))

        plt.bar(
            labels,
            values,
        )

        plt.title(
            "Feedback Sentiment Distribution"
        )

        plt.xlabel("Sentiment")
        plt.ylabel("Number of Feedback Items")

        plt.tight_layout()

        plt.savefig(
            chart_path,
            dpi=150,
        )

        plt.close()

        return chart_path