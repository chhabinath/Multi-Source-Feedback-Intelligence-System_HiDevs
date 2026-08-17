from src.processing.cleaner import TextCleaner

cleaner = TextCleaner()

text = "  AMAZING APP!!! 😍😍 Visit https://example.com  "

print(cleaner.clean(text))