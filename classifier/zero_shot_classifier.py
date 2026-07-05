import os
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))

with open("../data/phq9_categories.json", "r") as f:
    data = json.load(f)
    CATEGORIES = [cat["id"] for cat in data["categories"]]

def zero_shot(text: str) -> str:
    prompt = f"""You are a mental health classifier.
Given this message: {text}
Classify it into exactly one of these categories: {CATEGORIES}
If it does not match any category, return: none
Reply with only the category name, nothing else."""

    response = client.chat_completion(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()