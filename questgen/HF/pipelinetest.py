import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModel,
    AutoModelForSequenceClassification,
)

# classifier = pipeline("sentiment-analysis")
# print(classifier(["I can't wait to build this product!", "your face is scaring me"]))

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

raw_inputs = [
    "I've been waiting for a HuggingFace course my whole life.",
    "I hate this so much!",
]
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs)

# input_ids = unique ids for each token
# attention masks = ?
# {
#     "input_ids": tensor(
#         [
#             [
#                 101,
#                 1045,
#                 1005,
#                 2310,
#                 2042,
#                 3403,
#                 2005,
#                 1037,
#                 17662,
#                 12172,
#                 2607,
#                 2026,
#                 2878,
#                 2166,
#                 1012,
#                 102,
#             ],
#             [101, 1045, 5223, 2023, 2061, 2172, 999, 102, 0, 0, 0, 0, 0, 0, 0, 0],
#         ]
#     ),
#     "attention_mask": tensor(
#         [
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#         ]
#     ),
# }

# model = AutoModel.from_pretrained(checkpoint)
# outputs = model(**inputs)
# print(outputs.last_hidden_state.shape)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
outputs = model(**inputs)
print(outputs.logits.shape)
print(outputs.logits)

predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions)
print(model.config.id2label)

for i, pred in enumerate(predictions):
    print(raw_inputs[i])
    result = f"Results ({i}): "
    for idx, label in model.config.id2label.items():
        result += f"{label}: {pred[idx]*100:.2f}%  "
    print(result)
    print()
