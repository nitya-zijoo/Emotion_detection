import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))

def get_reply(user_message: str, chat_history: list) -> str:
    with open(os.path.join(os.path.dirname(__file__), "system_prompt.txt"), "r") as f:
        system_prompt = f.read()

    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history
    messages.append({"role": "user", "content": user_message})

    response = client.chat_completion(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message.content