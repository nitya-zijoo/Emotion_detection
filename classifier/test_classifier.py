from zero_shot_classifier import zero_shot

test_messages = [
    "I feel so empty and sad all the time",
    "I can't sleep at night",
    "I have no energy to do anything",
    "I feel worthless",
    "I can't concentrate on anything"
]

for msg in test_messages:
    result = zero_shot(msg)
    print(f"Message: {msg}\nCategory: {result}\n")