# HF models deepdive

import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModel,
    AutoModelForSequenceClassification,
)

from transformers import BertConfig, BertModel

config = BertConfig()
print(config)

# build model from config
model = BertModel(config)  # model is randomly initiailized (untrained)

# we could train from scratch but that is expensive,
# instead re-use models that have already been trained
model = BertModel.from_pretrained("bert-base-cased")

# We can replace BertModel with AutoModel as it will find the BertModel class and apply it automatically
# model weights are stored in ~/.cache/huggingface/transformers
# and can be customized by setting the HF_HOME env var

# save model
model.save_pretrained(".")


# doing inference
sequences = ["Hello!", "Cool.", "Nice!"]
# tokenizer converts these to vocabulary indices which are typically called input IDs.
encoded_sequences = [
    [101, 7592, 999, 102],
    [101, 4658, 1012, 102],
    [101, 3835, 999, 102],
]

model_inputs = torch.tensor(encoded_sequences)
output = model(model_inputs)
print(output)
