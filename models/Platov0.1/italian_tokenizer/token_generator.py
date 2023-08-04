# tokens massimi tollerabili 50000
# primi 45 tokens sono riservati
# 1: TERMINATION
# 2: SEPARATION QUESTION-DATA
# 3: SEPARATION DATA-ANSWER 
# 4: SEPARATION DATA-CONTEXT
# 5: SEPARATION CONTEXT-ANSWER
# 6: MARK UPPERCASE NEXT
# 7: OOV
# 8-10: UNKNOWN
# 11: RICHIESTA DI PULIZIA DATI
# 12: RICHIESTA DI CONTINUAZIONE DATI
# 13: RICHIESTA DI RISPOSTA DATI
# 14-20: UNKNOWN
# 21: INIZIO CITAZIONE
# 22: FINE CITAZIONE
# 23: INIZIO CODICE
# 24: FINE CODICE
# 25: INIZIO TITOLO
# 26: FINE TITOLO
# 27-30: UNKNOWN
# 31: ESEGUE CODICE PRECEDENTE (contenuto fra 23 e 24)
# 32: RICHIEDE OUTPUT CODICE ESEGUITO (che è rimasto in cache)
# 33-40: UNKNOWN

# le seguenti "sillabe" sono molto frequenti, comprendono prefissi e suffissi cosicche il modello di linguaggio riconosca
# la radice e ne associ prefissi e suffissi come ragiona una persona italiana normalente

prefissi = [
    "de", "ab", "con", "co", "im", "in", "iper", "ipo", "di", "da", "su", "per", "tra", "fra", "pro", "ri", "sovra", "sopra", "sus"
]

suffissi = [
    "are", "ere", "ire", "arsi", "ersi", "orsi", "irsi", "arci", "erci", "irci", "arvi", "ervi", "irvi", "arsela", "sela", "arsele",
    "avo", "avi", "ava", "avamo", "avate", "avano", 
    "issimo", "issima", "issimi", "issime",
    "ersele", "irsele", "arsene", "ersene", "iamo", "ate", "ano", "ete", "ono", "ite", "iscano", "iscano", "iamo", "iate", "isca", "iscono",
    "erò", "erai", "erà", "eremo", "erete", "eranno",
    "ando", "assi", "asse", "assimo", "aste", "assero", "essero", "ebbero", "arono", "erono", "irono", "irono", "eremo", "erete", "eranno",
    "ino", "ina", "ini", "oni",
    "erei", "eresti", "erebbe", "eremo", "ereste", "erebbero",
    "ebbero", "essi", "esse", "emo", "este", "eranno", "azione", "azioni", "atore", "atori", "azione", "azioni", "atore", "atori",
    "ei", "esti", "emmo", "este", "erono",
    "evamo", "evate", "evano", "evi", "eva", "evamo", "evate", "evano",
        "ai", "asti", "ammo", "aste", "arono",
        "ando", "endo",
        "ato", "etto", "ette", "ati", "ate",
        "abile", "mente",
    "o", "a", "e", "i", "ò", "à"
]

special_chars = [
    "!", "%", "&", "(", ")", "*", "+", ", ", ",", "-", ". ", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "€", "£", "§", "°", "ç", "é", "è", "à", "ù", "ì", "ò", "\n", "\t", "\r", "\b", "\\",
    "«", "»", "“", "”", "‘", "’", "„", "‟", "‹", "›", 
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
]

prep_e_congiunzioni = [
    "ma ", "però ", "perché ", "purché ", "che ",
    "li ", "le ", "gli ", "i ", "la ", "di "
    "è ", "ho ",
    "ne ",
]

#order suffissi from the longest to the shortest
suffissi.sort(key=len, reverse=True)

import json, os
tokens = []

raw_data = []

with open(os.path.join(os.path.dirname(__file__), "raw_data.json"), "r", encoding="utf-8") as f:
    for line in f:
        raw_data.append(line.strip())


# check if contains a prefix, and remove it. The same applies for suffixes
def remove_prefix_suffix(word):
    for prefisso in prefissi:
        if word.startswith(prefisso):
            word = word[len(prefisso):]
            break
    for suffisso in suffissi:
        if word.endswith(suffisso):
            word = word[:-len(suffisso)]
            break
    return word

for word in raw_data:
    word = remove_prefix_suffix(word)
    word = word
    if word not in tokens:
        tokens.append(word)

#sort tokens from the longest to the shortest
tokens.sort(key=len, reverse=True)
tokens_cache = tokens.copy()
tokens = []
#put 45 void tokens
info = {}
info["reserved"] = {"start": len(tokens)}
for i in range(45):
    tokens.append("<!$RESERVED-" + str(i) + "$!>")
info["reserved"]["end"] = len(tokens) - 1

info["suffissi_spaziati"] = {"start": len(tokens)}
for word in suffissi:
    word = word + " "
    if word not in tokens:
        tokens.append(word)
info["suffissi_spaziati"]["end"] = len(tokens) - 1

info["prep_cong_spaziati"] = {"start": len(tokens)}
for word in prep_e_congiunzioni:
    word = word
    if word not in tokens:
        tokens.append(word)
info["prep_cong_spaziati"]["end"] = len(tokens) - 1

info["prefissi"] = {"start": len(tokens)}
for word in prefissi:
    word = word
    if word not in tokens:
        tokens.append(word)
info["prefissi"]["end"] = len(tokens) - 1

for word in tokens_cache:
    word = word
    if word not in tokens:
        tokens.append(word)

for word in suffissi:
    word = word
    if word not in tokens:
        tokens.append(word)

for word in special_chars:
    word = word
    if word not in tokens:
        tokens.append(word)

#remove "" and " "
tokens.remove("")
tokens.append(" ")

info["total"] = len(tokens)

file = {"info": info, "tokens": tokens}

# save tokens in tokens.json
with open(os.path.join(os.path.dirname(__file__), "tokens.json"), "w", encoding="utf-8") as f:
    json.dump(file, f, ensure_ascii=False, indent=4)

"""
from transformers import PreTrainedTokenizer

custom_tokenizer = PreTrainedTokenizer.from_pretrained(tokens)

custom_tokenizer.save_pretrained("italian_13871_tokenizer")

encoded_text = custom_tokenizer.encode("Oggi è proprio una bella giornata, non credi?", add_special_tokens=True)

print(encoded_text)

decoded_text = custom_tokenizer.decode(encoded_text)

print(decoded_text)"""