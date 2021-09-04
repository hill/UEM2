# https://huggingface.co/course/chapter3
import torch
from transformers import (
    AdamW,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer,
)
from datasets import load_dataset, load_metric
from rich import print
import numpy as np


raw_datasets = load_dataset("glue", "mrpc")
# print(raw_datasets)
raw_train_dataset = raw_datasets["train"]
# print(raw_train_dataset[0])
# print(raw_train_dataset.features)
# exit()

checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# demo with single item
# tokenized_sentences_1 = tokenizer(raw_datasets["train"][15]["sentence1"])
# tokenized_sentences_2 = tokenizer(raw_datasets["train"][15]["sentence2"])
# print(tokenized_sentences_1)
# print(tokenized_sentences_2)
# inputs = tokenizer(
#     raw_datasets["train"][15]["sentence1"], raw_datasets["train"][15]["sentence2"]
# )
# print(inputs)
# print(tokenizer.convert_ids_to_tokens(inputs["input_ids"]))
# exit()

# this only works if you have enough RAM to store the entire dataset during tokenization
# tokenized_dataset = tokenizer(
#     raw_datasets["train"]["sentence1"],
#     raw_datasets["train"]["sentence2"],
#     padding=True,
#     truncation=True,
# )

# To keep the data as a dataset, we will use the Dataset.map method.
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)


tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


# samples = tokenized_datasets["train"][:8]
# samples = {  # remove string arrays - cannot make into tensors
#     k: v for k, v in samples.items() if k not in ["idx", "sentence1", "sentence2"]
# }
# print([len(x) for x in samples["input_ids"]])  # we see entries of various lengths

# batch = data_collator(samples)
# print({k: v.shape for k, v in batch.items()})  # all the same size

# exit()

training_args = TrainingArguments("test-trainer", evaluation_strategy="epoch")

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)


def compute_metrics(eval_preds):
    metric = load_metric("glue", "mrpc")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()

exit()


sequences = [
    "I've been waiting for a HuggingFace course my whole life.",
    "This course is amazing!",
]
batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")

# This is new
batch["labels"] = torch.tensor([1, 1])

optimizer = AdamW(model.parameters())
loss = model(**batch).loss
loss.backward()
optimizer.step()
