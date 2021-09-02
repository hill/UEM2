# Hugging Face Notes

https://huggingface.co/course/

Speeding up inference: https://huggingface.co/blog/accelerated-inference

## Models

### Encoders

### Decoders

### Seq-to-Seq (Encoder/Decoder)

## What happens in the pipeline fn?

1. Tokenizer (raw text to numbers)
   - raw text split into tokens
   - special tokens added
   - tokens translated into IDs
   ```python
   from transformers import AutoTokenizer
   checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
   tokenizer = AutoTokenizer.from_pretrained(checkpoint)
   raw_inputs = ["Hello world", "This is very cool"]
   inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
   ```
2. Model (numbers to logits)

   - `AutoModel` loads a model without pretraining head

   ```py
    from transformers import AutoModel
    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModel.from_pretrained(checkpoint)
    outputs = model(**inputs)
    print(outputs.last_hidden_state.shape) # torch.Size([2, 16, 768]) (batch size, sequence length, hidden size)
   ```

   - Each `AutoModelForXxx` class loads a model suitable for a specific task

   ```py
   from transformers import AutoModelForSequenceClassification

   checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
   model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
   outputs = model(**inputs)
   print(outputs.logits)
   ```

3. Postprocessing (logits to predictions)

   - to go from logits to probabilities we apply a softmax layer

   ```py
   import torch

   predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
   print(predictions)
   # tensor([[3.0e-02, 3.0e-02],
   #         [3.0e-02, 3.0e-02]], grad_fn=<SoftmaxBackwards>)

   model.config.id2label # index to label
   ```
