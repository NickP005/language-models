"""
This file prepares the training data sequences 
"""

import os
import numpy as np
from italian_tokenizer import italian_tokenizer
from keras.preprocessing.sequence import pad_sequences

MAX_TOKENS = 257

"""
This function asks for the file name contained in "clean_data"

"""
def get_sequences_from_dialogue(file_name, part_n=0, total_parts=1):
    f = open(os.path.join("clean_data", file_name), "r", encoding="utf8")
    lines = f.readlines()
    lines = lines[part_n*len(lines)//total_parts:(part_n+1)*len(lines)//total_parts]
    f.close()
    # Get the file name removing .txt
    file_name = file_name[:-4].lower()
    book_ids = italian_tokenizer.tokenize_string(file_name).tolist()
    # For logging
    tokenized_lines = 0
    total_tokenizing_lines = len(lines)
    # We suppose each line is a dialogue
    sequences = []
    previous_sequence = [] # BOOK_NAME + token(2) + CHARACTER_NAME + token(3) + TRUNCATED_ANSWER
    for line in lines:
        sequence = book_ids.copy() + [2]
        person_name = line.split(" ")[0]
        if len(person_name) == 0:
            continue
        if person_name[-1] == ":":
            person_name = person_name[:-1]
        person_name = person_name.lower()
        person_ids = italian_tokenizer.tokenize_string(person_name).tolist()
        sequence += person_ids + [3]
        spoken_string = line[len(person_name)+1:]
        spoken_ids = italian_tokenizer.tokenize_string_multithread(spoken_string).tolist()
        remaining_tokens = MAX_TOKENS - len(sequence)
        
        # start by adding all the sequences from spoken_ids[:1] to spoken_ids[:remaining_tokens]
        start_index = 1
        while(start_index < remaining_tokens and start_index < len(spoken_ids)):
            sequences.append(sequence + spoken_ids[:start_index])
            start_index += 1
        
        if len(spoken_ids) > remaining_tokens:
            # append the remaining as example spoken_ids[:remaining_tokens], spoken_ids[1:remaining_tokens+1], spoken_ids[2:remaining_tokens+2], ...
            start_index = 1
            while(start_index < len(spoken_ids) - remaining_tokens):
                sequences.append(sequence + spoken_ids[start_index:start_index+remaining_tokens])
                start_index += 1        
        # MAX_TOKENS - len(person_ids) - 3 because we need space for the character name, the 2 tokens and the 3 token
        if len(previous_sequence) > 0 and len(previous_sequence) < MAX_TOKENS - (len(person_ids) + 3):
            # add to the previous sentence (BOOK_NAME + token(2) + CHARACTER_NAME + token(3) + ANSWER) 
            # the current sentence (QUESTION + token(2) + CHARACTER_NAME + token(3) + TRUNCATED_ANSWER)
            amout_of_current_sequence = 1
            while(amout_of_current_sequence < len(spoken_ids) and amout_of_current_sequence < MAX_TOKENS - (len(person_ids) + 3) - len(previous_sequence)):
                sequences.append(previous_sequence + [2] + person_ids + [3] + spoken_ids[:amout_of_current_sequence])
                amout_of_current_sequence += 1
            # now if of the current sequence there are still tokens left, we make space removing the previous sequence one token at time
            # TODO AFTER 
            previous_sequence = sequences[-1]
        else:
            previous_sequence = sequence + spoken_ids[:MAX_TOKENS - (len(person_ids) + 3)]
        tokenized_lines += 1
        print("\rTokenizing line {}/{} - sequences: {}".format(tokenized_lines, total_tokenizing_lines, len(sequences)), end="")

    # convert the sequences to 2d numpy array of integers
    # pad the sequences
    sequences = pad_sequences(sequences, maxlen=MAX_TOKENS, padding="pre", truncating="post")
    return sequences


# BOOK_NAME + token(2) + CHARACTER_NAME + token(3) + TRUNCATED_ANSWER
# BOOK_NAME + token(2) + CHARACTER_NAME + token(3) + QUESTION + token(2) + CHARACTER_NAME + token(3) + TRUNCATED_ANSWER

# function that transforms the sequences into X,y training data
def get_training_data(sequences):
    X = sequences[:,:-1]
    y = sequences[:,-1]
    return X,y

TOPICS_NUMBER = 101
MAX_TOPICS = 12
# function to get blank topics arrays (all zero array of lenght MAX_TOPICS)
def get_blank_X_topics(many=1):
    return np.zeros((many, MAX_TOPICS))
# function to get random topics. Ex output for many=2, [[2], [5]]
# [0] occur 50% of the time, the others 50% are distributed uniformly
def get_random_X_topics(many=1):
    topics = np.zeros((many, 1))
    for i in range(many):
        if np.random.randint(0, 2) == 0:
            topics[i] = 0
        else:
            topics[i] = np.random.randint(1, TOPICS_NUMBER)
    return topics

# 
def test_model(book_name, character_name, question):
    book_name = book_name.lower()
    character_name = character_name.lower()
    question = question.lower()
    book_ids = italian_tokenizer.tokenize_string(book_name).tolist()
    character_ids = italian_tokenizer.tokenize_string(character_name).tolist()
    question_ids = italian_tokenizer.tokenize_string_multithread(question).tolist()
    sequence = book_ids + [2] + character_ids + [3] + question_ids
    sequence = pad_sequences([sequence], maxlen=MAX_TOKENS-1, padding="pre", truncating="post")
    return sequence

# create prepared sequences of data numpy array of maximum 32768 sequences per file saved in train_data/
def create_prepared_sequences(file_name, max_sequences=32768):
    sequences = get_sequences_from_dialogue(file_name)
    # split the sequences in 10000 sequences per file
    for i in range(0, len(sequences), max_sequences):
        np.save("train_data/{}_{}.npy".format(file_name[:-4], i/max_sequences), sequences[i:i+max_sequences])
    del sequences # free memory


""" Example of usage

sequences = get_sequences_from_dialogue("Teagete.txt")
X, y = get_training_data(sequences)
del sequences # free memory

"""

# Example of usage
if __name__ == "__main__":
    #create_prepared_sequences("Teagete.txt")
    #create_prepared_sequences("Timeo.txt")
    #create_prepared_sequences("Teeteto.txt")
    #create_prepared_sequences("Simposio.txt")
    #create_prepared_sequences("Politico.txt")
    #create_prepared_sequences("Menone.txt")
    create_prepared_sequences("Menesseno.txt")
    create_prepared_sequences("Lachete.txt")
    create_prepared_sequences("Ippia-minore.txt")
    create_prepared_sequences("Ippia-maggiore.txt")