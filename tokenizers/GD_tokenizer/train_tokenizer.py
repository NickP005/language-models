"""
Using the tokenizer from HuggingFace, we train a tokenizer on the GD corpus.

"""
from pathlib import Path
from tokenizers import ByteLevelBPETokenizer

paths = [str(x) for x in Path(".").glob("clean_data/*.txt")]

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=paths, vocab_size=4_000, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

# Save files to disk
tokenizer.save_model("data/GD_tokenizer")

# print statistics
print("Number of tokens: " + str(len(tokenizer.get_vocab())))
print("Number of special tokens: " + str(len(tokenizer.get_vocab()) - 4000))

# take a random file from the corpus and print both the words size and the token size, then the ratio
import random

file = "clean_data/Liside.txt"

with open(file, "r") as f:
    string = f.read()
    words = string.split(" ")
    tokens = tokenizer.encode(string).tokens
    print("File: " + file)
    print("Words: " + str(len(words)))
    print("Tokens: " + str(len(tokens)))
    print("Ratio: " + str(len(tokens) / len(words)))
"""
tokenizer = ByteLevelBPETokenizer()

tokenizer.train(files=paths, vocab_size=16_000, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])
with open(file, "r") as f:
    string = f.read()
    words = string.split(" ")
    tokens = tokenizer.encode(string).tokens
    print("File: " + file)
    print("Words: " + str(len(words)))
    print("Tokens: " + str(len(tokens)))
    print("Ratio: " + str(len(tokens) / len(words)))
"""