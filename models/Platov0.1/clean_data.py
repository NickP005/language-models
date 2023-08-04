"""
This file is used to clean the data from the raw data file.
1. Delete all the files in data/
2. For each file in raw_data/
    2.1. For each line in the file, if the line starts with 4 or less words which start with uppercase and the next line is a number, delete both lines
    2.2. If the first word of the line isn't all uppercase, to the previous line append a whitespace and the current line
    2.3. if a "(" contains a ")", delete the "(" and the following ")"
    2.4. create a new file in data/ with the same name as the raw file
"""

import os
import re
import shutil

# function to check if a word is all uppercase
def is_all_uppercase(word):
    for letter in word:
        if letter.islower():
            return False
    return True

def clean_file(string):
    # 2.1. For each line in the file, if the line starts with 4 or less words which start with uppercase and the next line is a number, delete both lines
    lines = string.split("\n")
    string = ""
    titles_deleted = 0
    skip_next = False
    for line in lines:
        if len(line) == 0:
            continue
        if skip_next and line[0].isdigit():
            skip_next = False
            continue
        if line[0] == " ":
            line = line[1:]
        words = line.split(" ")
        to_delete = False
        if len(words) == 0:
            to_delete = True
        elif len(words) <= 5:
            upper_words = 0
            for word in words:
                if len(word) == 0:
                    to_delete = True
                    continue
                if word[0].isupper():
                    upper_words += 1
            if upper_words/len(words) > 0.4:    
                to_delete = True
            if words[0] != "Platone": 
                to_delete = False
        if to_delete:
            titles_deleted += 1
            skip_next = True
        else:
            string += line + "\n"
    print("Deleted " + str(titles_deleted) + " titles")

    # 2.2. If the first word of the line isn't all uppercase, to the previous line append a whitespace and the current line
    removed_total_nextline = 0
    removed_nextline = 1
    while removed_nextline > 0:
        removed_nextline = 0
        lines = string.split("\n")
        string = ""
        for line in lines:
            words = line.split(" ")
            if not is_all_uppercase(words[0]) or len(words[0]) == 1 or (not words[0].isalpha()):
                if len(words[0]) > 0 and words[0][-1] != ":":
                    string = string[:-1] + " " + line + "\n"
                    removed_nextline += 1
                elif len(words[0]) > 1 and words[0][0].islower():
                    string = string[:-1] + " " + line + "\n"
                    removed_nextline += 1
                else:
                    string += line + "\n"
            else:
                string += line + "\n"
        removed_total_nextline += removed_nextline

    print("Removed " + str(removed_total_nextline) + " nextlines")

    # 2.3. if a parenthesis contains onl a number, delete the whole parenthesis
    removed_parenthesis = 0
    lines = string.split("\n")
    string = ""
    for line in lines:
        parenthesis = re.findall(r'\(.*?\)', line)
        for p in parenthesis:
            if p[1:-1].isdigit():
                line = line.replace(p, "")
                removed_parenthesis += 1
        string += line + "\n"
    print("Removed " + str(removed_parenthesis) + " parenthesis")

    return string

def clean_data(read_folder, deposit_folder):
    # Delete all files in data/
    for filename in os.listdir(deposit_folder):
        file_path = os.path.join(deposit_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # For each file in raw_data/
    for filename in os.listdir(read_folder):
        file_path = os.path.join(read_folder, filename)
        print("Cleaning " + filename)
        if os.path.isfile(file_path):
            # Open the file
            f = open(file_path, "r", encoding="utf8")
            new_string = clean_file(f.read())
            f.close()
            # Create a new file in data/ with the same name as the raw file
            new_file_path = os.path.join(deposit_folder, filename)
            f = open(new_file_path, "w", encoding="utf8")
            f.write(new_string)
            f.close()
"""
For each file in clean_data/, distinguish if it's a explicit dialogue or a flowing text
To see if it's a dialogue, check if at least 5 lines in the file have the first work that ends with ":".
If it's not a dialogue, implicitly is a flowing text.
Create an info.json file in the same folder as the file with the following structure:
{
    "data": {
        "file_name": {
            "type": "dialogue" or "flowing_text",
            "title": "title of the file",
            "lines": "number of lines in the file",
            "words": "number of words in the file",
            "dialogues": "number of dialogues in the file",
            "partecipants": ["list", "of", "partecipants", "in", "the", "dialogues"]
            }
            }
    }
"""
import json
def catalogue_data(read_folder, deposit_folder):
    # For each file in clean_data/
    infos = {}
    known_partecipants = []
    for filename in os.listdir(read_folder):
        file_path = os.path.join(read_folder, filename)
        print("Cataloguing " + filename)
        if os.path.isfile(file_path):
            # Open the file
            f = open(file_path, "r", encoding="utf8")
            lines = f.read().split("\n")
            f.close()
            # Check if it's a dialogue
            is_dialogue = False
            dialogue_lines = 0
            total_lines = len(lines)
            partecipants = []
            for line in lines:
                words = line.split(" ")
                if len(words) > 0:
                    word = words[0]
                    if len(word) < 2:
                        continue
                    if word[-1] == ":":
                        word = word[:-1]
                    word = word[0].upper() + word[1:].lower()
                    if word not in known_partecipants:
                        known_partecipants.append(word)
                        partecipants.append(word)

                is_dialogue = True
            # Create the info.json file
            info = {
                "type": "dialogue" if is_dialogue else "flowing_text",
                "title": filename,
                "lines": total_lines,
                "words": sum([len(line.split(" ")) for line in lines]),
                "dialogues": dialogue_lines,
                "partecipants": partecipants
            }
            infos[filename] = info

    # Write the deposit file
    f = open(os.path.join(deposit_folder, "info.json"), "w", encoding="utf8")
    f.write(json.dumps(infos, indent=4))


"""
# Delete all files in data/
for filename in os.listdir("data"):
    file_path = os.path.join("clean_data", filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# For each file in raw_data/
for filename in os.listdir("raw_data"):
    file_path = os.path.join("raw_data", filename)
    print("Cleaning " + filename)
    if os.path.isfile(file_path):
        # Open the file
        f = open(file_path, "r", encoding="utf8")
        new_string = clean_file(f.read())
        f.close()
        # Create a new file in data/ with the same name as the raw file
        new_file_path = os.path.join("clean_data", filename)
        f = open(new_file_path, "w", encoding="utf8")
        f.write(new_string)
        f.close()
        """

if __name__ == "__main__":
    clean_data("raw_data", "clean_data")
    catalogue_data("clean_data", "clean_data")