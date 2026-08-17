from src.actions.integrations import IntegrationHub


hub = IntegrationHub()


feedback = {
    "id": "feedback_001",
    "text": "The application keeps crashing",
    "rating": 1,
    "sentiment": "negative",
    "category": "bug",
    "priority": "critical",
}


results = hub.process_feedback(
    feedback
)


for result in results:
    print("--------------------------------")
    print("Integration:", result["integration"])
    print("Action:", result["action"])

    if "ticket" in result:
        print("Ticket:", result["ticket"])

    if "data" in result:
        print("CRM data:", result["data"])

    if "message" in result:
        print("Message:", result["message"])