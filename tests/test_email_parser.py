from src.ingestion.email_parser import EmailFeedbackParser


parser = EmailFeedbackParser()

raw_email = """\
From: customer@example.com
Subject: Application keeps crashing - Rating: 1

Hello,

The application keeps crashing whenever I try to open it.
Please fix this issue.

Thanks.
"""

result = parser.parse(raw_email)

print("--------------------------------")
print("ID:", result["id"])
print("Text:", result["text"])
print("Rating:", result["rating"])
print("Source:", result["source"])
print("Metadata:", result["metadata"])