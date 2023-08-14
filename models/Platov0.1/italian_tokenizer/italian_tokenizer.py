import os, json
#numpy array
import numpy as np

# read tokens.json array
file = json.load(open(os.path.join(os.path.dirname(__file__), 'tokens.json'), 'r', encoding='utf-8'))

tokens = file['tokens']
info = file['info']

def tokenize_string(string):
    nuova_stringa = string
    token_list = np.array([], dtype=np.int32)
    is_whitespace = False
    while len(nuova_stringa) > 1:
        found = False
        if nuova_stringa[0].isupper():
            nuova_stringa = nuova_stringa[0].lower() + nuova_stringa[1:]
            token_list = np.append(token_list, 6)
        
        if not is_whitespace:
            examine = tokens[:45] + tokens[66:]
        else:
            examine = tokens
            is_whitespace = False
        for token in examine:   
            if nuova_stringa.startswith(token):
                nuova_stringa = nuova_stringa[len(token):]
                token_list = np.append(token_list, tokens.index(token))
                found = True
                if token == ' ' or (tokens.index(token) > info["suffissi_spaziati"]["start"] and tokens.index(token) < info["prep_cong_spaziati"]["end"]):
                    is_whitespace = True
                break
        if not found:
            nuova_stringa = nuova_stringa[1:]
            token_list = np.append(token_list, 7)
    return token_list

#write a function that using multiprocessing tokenizes a string (using the tokenize_string func) while splitting it into multiple substrings
#then it merges the substrings into a single token list
import multiprocessing, threading
import queue

def tokenize_string_multithread(string, threads=16):
    if threads < 2:
        return tokenize_string(string)
    substrings = []
    for i in range(threads):
        substrings.append(string[i*len(string)//threads:(i+1)*len(string)//threads])
    substrings.append(string[(i+1)*len(string)//threads:])
    thread_queue = queue.Queue()
    threadss = []
    for i in range(threads):
        threadss.append(threading.Thread(target=lambda: thread_queue.put(tokenize_string(substrings[i]))))
        threadss[i].start()
    token_list = np.array([], dtype=np.int32)
    for i in range(threads):
        token_list = np.append(token_list, thread_queue.get())
    return token_list

def tokenize_string_multiprocess(string, processes=4):
    if processes < 2:
        return tokenize_string(string)

    def process_substring(substring, queue):
        queue.put(tokenize_string(substring))

    substrings = []
    for i in range(processes):
        substrings.append(string[i * len(string) // processes:(i + 1) * len(string) // processes])
    substrings.append(string[(i + 1) * len(string) // processes:])

    process_queue = multiprocessing.Queue()
    processesss = []

    for i in range(processes):
        process = multiprocessing.Process(target=process_substring, args=(substrings[i], process_queue))
        process.start()
        processesss.append(process)

    for i in range(processes):
        processesss[i].join()

    token_list = np.array([], dtype=np.int32)
    for i in range(processes):
        token_list = np.append(token_list, process_queue.get())

    return token_list


def detokenize_string(token_list):
    stringa = ''
    to_upper = False
    #convert numpy token list to python list
    token_list = token_list.tolist()
    for token in token_list:
        if token == 6:
            to_upper = True
        else:
            string = tokens[token]
            if to_upper:
                string = string[0].upper() + string[1:]
                to_upper = False
            stringa += string
    return stringa
    