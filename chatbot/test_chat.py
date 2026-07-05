from chat_handler import get_reply

history = []
while True:
    user = input("You: ")
    reply = get_reply(user, history)
    print(f"Bot: {reply}")
    history.append({"role": "user", "content": user})
    history.append({"role": "assistant", "content": reply})