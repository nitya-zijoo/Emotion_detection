from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "saved_model")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

def classify_message(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_id = torch.argmax(outputs.logits, dim=1).item()
    return model.config.id2label[predicted_id]