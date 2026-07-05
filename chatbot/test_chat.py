from chat_handler import get_reply
from crisis_check import is_crisis
history = []
while True:
    user = input("You: ")
    crisis, response = is_crisis(user, history)
    if crisis:
        print(f"Bot: {response}")
        break
    reply = get_reply(user, history)
    print(f"Bot: {reply}")
    history.append({"role": "user", "content": user})
    history.append({"role": "assistant", "content": reply})