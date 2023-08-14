"""
Test the tpu model in tpu_model.h5
"""

import os
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical
from keras.utils import plot_model
from keras.preprocessing.sequence import pad_sequences
from train_data import test_model
from italian_tokenizer.italian_tokenizer import detokenize_string, tokenize_string
import random as rn

# Load the model
model = load_model('tpu_model (4).h5')

test_book = "Alcibiade"
test_character = "Alcibiade"
test_text = "Io penso che"

sequence = test_model(test_book, test_character, test_text)
print(sequence) # np array [256 tokens]

to_generate = 20


for i in range(to_generate):
    # predict next token
    y_preds = model.predict(sequence)[0]
    # select randomly one of the first 3 most probable tokens, weighted by their probability
    top_3 = np.argsort(y_preds)[-3:]
    sums_probs = np.sum(y_preds[top_3])
    probs = y_preds[top_3] / sums_probs
    y_pred = np.random.choice(top_3, p=probs)
    # print the possible token predictions as
    # word (token_number): probability
    for j in range(3):
        print(detokenize_string(np.array([top_3[j]])), "(", top_3[j], "):", probs[j])
    print("Selected:", detokenize_string(np.array([y_pred])))
    # append to sequence
    sequence = sequence[0].tolist()
    sequence.append(y_pred)

    word = detokenize_string(np.array([y_pred]))
    test_text = test_text + word
    
    # delete the sequence after the first token 3 from the left
    # if after this token 3 there is a token 2, start deleting from the first token 2 from the left up to the token 3
    print(len(sequence))
    if sequence[0] != 0:
        print("sequence[0] != 0")
        for j in range(len(sequence)):
            if sequence[j] == 3:
                if sequence[j+1] == 2:
                    first_2 = 0
                    for k in range(len(sequence)):
                        if sequence[k] == 2:
                            first_2 = k
                            break
                    sequence = sequence[:first_2] + sequence[j+1:]
                    break
                else:
                    sequence = sequence[:j] + sequence[j+2:]
                    print(len(sequence))
                    break
    else:
        sequence = sequence[1:]
    sequence = np.array([sequence])

print(test_text)
print(detokenize_string(sequence[0]))