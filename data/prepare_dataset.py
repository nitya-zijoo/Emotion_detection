from datasets import load_dataset
dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
print(dataset)
print(dataset["train"][0])
print(dataset["train"].features["labels"])