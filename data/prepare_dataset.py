from datasets import load_dataset
dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
LABEL_MAP = {
    25: "depressed_mood",
    16: "depressed_mood",
    9: "depressed_mood",
    24: "worthlessness",
    12: "worthlessness",
    14: "concentration",
    19: "concentration",
    6: "concentration"
}

def map_labels(example):
    mapped = [LABEL_MAP[l] for l in example["labels"] if l in LABEL_MAP]
    return {"text": example["text"], "phq9_label": mapped[0] if mapped else None}

mapped_dataset = dataset["train"].map(map_labels)
filtered = mapped_dataset.filter(lambda x: x["phq9_label"] is not None)
import pandas as pd

df = pd.DataFrame({"text": filtered["text"], "label": filtered["phq9_label"]})
df.to_csv("data/train.csv", index=False)
print(df["label"].value_counts())