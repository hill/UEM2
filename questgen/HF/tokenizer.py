import torch
from transformers import BertTokenizer

# ===== Word based =====
# split on spaces / punctuation. Each word has an id assigned to it.
# limitations:
# - dog, dogs will assign different ids and the model will learn different embeddings
# - vocab size can be very large, keeping track of words can be difficult
tokens = "Tom Hill went to MacDonald's farm".split()


# ===== Character based =====
# split text into characters, rather than words
# - there are a high number of words in a vocab (>170,000),
#   but a small number of characters (<256) = fewer tokens
# - words unseen during tokenizer training will still be able to be tokenized,
#   because all the characters available in a language have an id
# - intuitively, characters do not hold as much info as a word would
# - word based tokenization seq = [250, 861, 10000, UNK]
# - char based tokenization seq = [12,33,44,22,11,123,34,12,345,234,23,345,34,23,56,78]
# - i.e. char based sequence are much longer -> will have an effect on the **context** a
#   token can carry with it

# ===== Subword based tokenization =====
# find a middle ground b/w words and characters
# avoid:
# - very large vocabs
# - large number of out of vocab tokens
# - loss of meaning across very similar words (dog/dogs)
# - very long sequences
# - less meaning full individual tokens (z,x,y vs dog, cat)
# freq used words should not be split, but rare words should be decomposed into meaningful subwords
# - dog = dog
# - dogs = [dog, s]
# - tokenization = [token, ##ization] (## = BERT wordpiece algorithm start of word)

tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
# tokenizer = AutoTokenizer.from_pretrained("bert-base-cased") # will do the same

inputs = tokenizer("Using a transformer network is simples")
print(inputs["input_ids"])

# Encoding
tokens = tokenizer.tokenize("Let's try to tokenize this baaabyyy!?!")
print(tokens)
input_ids = tokenizer.convert_tokens_to_ids(tokens)
print(input_ids)
print(tokenizer.decode(input_ids))

# Handling multiple sentences
# we pad the shorter sequence to the length of the longest one
from transformers import AutoTokenizer, AutoModelForSequenceClassification

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

sentences = ["Woah this is soooo cool man!", "I'm really sorry."]
tokens = [tokenizer.tokenize(sentence) for sentence in sentences]
ids = [tokenizer.convert_tokens_to_ids(token) for token in tokens]
print(ids[0])
print(ids[1])  # not the same length
print("padding id:", tokenizer.pad_token_id)

# single inference
id1 = torch.tensor([ids[0]])  # model expects a list of sequences
id2 = torch.tensor([ids[1]])
output = model(id1)
print("logits:", output.logits)

output = model(id2)
print("logits:", output.logits)

# batched inference
pad_length = len(ids[0]) - len(ids[1])
batched_ids = torch.tensor([ids[0], ids[1] + [tokenizer.pad_token_id] * pad_length])
output = model(batched_ids)
print("logits:", output.logits)
# note that second bit is not == to output from first id2
# we use attention masks to ensure attention is not shared across batched sequences

attention_mask = [[1] * len(ids[0]), [1] * len(ids[1]) + [0] * pad_length]
outputs = model(batched_ids, attention_mask=torch.tensor(attention_mask))
print("should be the same as top 2:", outputs.logits)

# all together in a high level api:

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

sequences = ["I've been waiting for a HuggingFace course my whole life.", "So have I!"]

model_inputs = tokenizer(sequences, padding="longest")  # pt=pytorch

print(model_inputs["input_ids"])
tokens = tokenizer.tokenize(sequences[0])
ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)
print(tokenizer.decode(model_inputs["input_ids"]))
print(tokenizer.decode(ids))
