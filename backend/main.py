import sys
sys.path.append('..')

from chatbot.chat_handler import get_reply
from chatbot.crisis_check import is_crisis
from classifier.predict import classify_message
from backend.database import save_message
from backend.aggregator import get_category_counts
from backend.intervention import get_resources

def main(user_id: str, text: str, chat_history: list) -> dict:
    # Step 1 - Crisis check
    crisis, crisis_response = is_crisis(text, chat_history)
    if crisis:
        return {"reply": crisis_response, "suggestion": None}

    # Step 2 - Chatbot reply
    reply = get_reply(text, chat_history)

    # Step 3 - Classify
    category = classify_message(text)

    # Step 4 - Store
    save_message(user_id, text, category)

    # Step 5+6 - Aggregate + suggest
    counts = get_category_counts(user_id)
    band, dominant, resources = get_resources(counts)

    # Step 7 - Return
    return {
        "reply": reply,
        "suggestion": resources if resources else None
    }