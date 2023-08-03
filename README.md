# Language models

This is my repository where I put my experiments - successful or not - about Language Models (a branch of Artificial Neural Networks dedicated to language processing and generation).

## Tokenizers
### Italian Tokenizer
The tokens are unique words taken from [@napolux/paroleitaliane](https://github.com/napolux/paroleitaliane/blob/master/paroleitaliane/60000_parole_italiane.txt). From each word I removed the common prefixes that change the meaning of the verb/noun/adjective and the common suffixes. The common suffixes have also integrated a space ending.  
As result, the total tokens are **14009** with *23 prefixes*, *97x2 suffixes*, *11 conjuctions and prepositions* and *45 special tokens*.

Below the listing of the special tokens:
| ID | usage 
|-|-
| 1 | termination of output
| 2 | sep. topic-data
| 3 | sep. data-answer
| 4 | sep. data-context
| 5 | sep. context-answer
| 6 | uppercase next char
| 7 | out of vocabulary
| 21 | start citation
| 22 | end citation
| 23 | start code (right before language name)
| 24 | end code
| 25 | start different text size (right before lenght)
| 26 | end different text size
| 31 | execute precedent code
| 32 | slide to data output executed code

## Fantastic models (and where to find them)
### Plato Model
Next Token Prediction model aimed to replicate the dialogues and the argumentations of Plato in its style.

*Language: Italian*  
*Tokenizer: Italian Tokenizer by NickP05*  
*Data training: Plato's works on ousia.it*

This is meant to be used on a website where you select the starting character and write a question or the beginning of a phrase that character would say. Optionally can input the work's name. The model is aimed to predict the next words without limits: the challenge will challenge itself to create self-classified resumes.

#### Model overall structure
The overall


256 TOKENS(14009) INPUT  
180 LSTM layer  
EMBEDDING (+ 12 TOKENS(101))  
180 BiLSTM layer  
DROPOUT 15%  
180 Dense layer | 101 Dense categorical_crossentropy OUTPUT  
14009 Dense categorical_crossentropy OUTPUT

#### Training data structure - dialogues
Each training set contains:  
BOOK_NAME + token(2) + CHARACTER_NAME + token(3) + QUESTION + token(4) + TRUNCATED_ANSWER
