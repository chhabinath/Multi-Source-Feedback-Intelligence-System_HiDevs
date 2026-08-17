from typing import Dict, List


class FeedbackPromptBuilder:
    """
    Builds structured prompts for AI-based feedback analysis.

    This component prepares the information that can be sent
    to an AI model for deeper insight generation.
    """

    def build_feedback_analysis_prompt(
        self,
        feedback: Dict,
    ) -> str:
        """
        Build a prompt for analyzing one feedback item.
        """

        return f"""
Analyze the following customer feedback.

Feedback:
{feedback.get("text", "")}

Rating:
{feedback.get("rating", "unknown")}

Sentiment:
{feedback.get("sentiment", "unknown")}

Sentiment confidence:
{feedback.get("sentiment_confidence", 0.0)}

Category:
{feedback.get("category", "unknown")}

Priority:
{feedback.get("priority", "unknown")}

Return the analysis using these sections:

1. Main issue
2. Customer intent
3. Business impact
4. Recommended action
5. Severity
""".strip()

    def build_batch_insight_prompt(
        self,
        feedback_list: List[Dict],
    ) -> str:
        """
        Build a prompt for identifying patterns across
        multiple feedback records.
        """

        feedback_text = []

        for feedback in feedback_list:
            feedback_text.append(
                {
                    "text": feedback.get("text", ""),
                    "rating": feedback.get("rating"),
                    "sentiment": feedback.get(
                        "sentiment",
                        "unknown",
                    ),
                    "category": feedback.get(
                        "category",
                        "unknown",
                    ),
                    "priority": feedback.get(
                        "priority",
                        "unknown",
                    ),
                }
            )

        return f"""
Analyze the following collection of customer feedback.

Feedback records:
{feedback_text}

Identify:

1. Top recurring issues
2. Most common categories
3. Major negative themes
4. Positive themes
5. High-priority issues
6. Possible emerging problems
7. Recommended business actions

Focus on patterns that appear across multiple feedback
records rather than isolated comments.
""".strip()