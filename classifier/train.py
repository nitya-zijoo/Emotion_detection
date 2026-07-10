import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import torch
import numpy as np
from sklearn.metrics import f1_score

# Load data
df = pd.read_csv("../data/train.csv")

# Encode labels
label2id = {"depressed_mood": 0, "concentration": 1, "worthlessness": 2}
id2label = {v: k for k, v in label2id.items()}
df["label"] = df["label"].map(label2id)

# Split
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Convert to HF Dataset
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Load tokenizer and model
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3,
    id2label=id2label,
    label2id=label2id
)

# Tokenize
def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

# Metrics
def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)
    return {"f1": f1_score(labels, preds, average="weighted")}

# Training args
args = TrainingArguments(
    output_dir="../classifier/saved_model",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    logging_dir="../classifier/logs"
)


# Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.save_model("../classifier/saved_model")
tokenizer.save_pretrained("../classifier/saved_model")
print("Training complete.")