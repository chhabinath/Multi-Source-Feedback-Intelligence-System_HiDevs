from src.ingestion.webhooks import WebhookReceiver


receiver = WebhookReceiver()

payload = {
    "id": "web_001",
    "text": "The application keeps crashing",
    "rating": 1,
    "source": "web",
}

result = receiver.receive(payload)

print("Webhook result:")
print(result)