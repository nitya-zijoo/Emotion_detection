import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))

CRISIS_PHRASES = [
    "it is better to die",
    "i hate living",
    "i want to hurt myself",
    "is there no way out",
    "soon this will all be over",
    "things will never get better",
    "you'd be better off without me",
    "people would be happier if i were gone",
    "everyone would be relieved if i died",
    "i'm only making things worse for my family",
    "i don't want to exist",
    "i wish i was dead",
    "i want to disappear forever",
    "no one would miss me",
    "i can't do this anymore"
]

CRISIS_RESPONSE = """
I hear you, and I'm really glad you're talking to me.
Please reach out to someone who can help right now:
- iCall (India): 9152987821
- Vandrevala Foundation: 1860-2662-345 (24/7)
- AASRA: 91-22-27546669
You matter. Please make that call.
"""
def is_crisis(text: str, chat_history: list) -> tuple:
    text_lower = text.lower()
    matched_keyword = None
    
    for phrase in CRISIS_PHRASES:
        if phrase in text_lower:
            matched_keyword = phrase
            break
    
    if not matched_keyword:
        return False, None
    
    prompt = f"""You are a mental health safety checker.
Given this message: {text}
And this conversation history: {chat_history}
The word/phrase '{matched_keyword}' was flagged.
Is the user expressing suicidal tendency or self-harm intent?
Reply with only YES or NO."""

    response = client.chat_completion(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5
    )
    
    answer = response.choices[0].message.content.strip().upper()
    
    if answer == "YES":
        return True, CRISIS_RESPONSE
    return False, None