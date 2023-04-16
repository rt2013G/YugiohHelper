import json
import os.path
import time
import re

# This file is a standalone script used to parse a json file of a Telegram chat into a .txt file
# The cleaner function is made ad hoc for our group chat
def cleaner(text):
    new_string = text.lower()
    new_string = new_string.replace("benvenuto/a", "benvenuto")
    new_string = new_string.replace("/", " ").replace("\\", " ")
    new_string = re.sub("[^a-zA-Z'àèìòù ]+", "", new_string)
    new_string = new_string.replace("   ", " ").replace("  ", " ")
    new_string = new_string.strip()
    return new_string

def main():
    start = time.time()
    raw_data = json.load(open(os.path.dirname(__file__) +
                           "/model/result_main.json","r", encoding="utf8"))
    i = 0
    with open(os.path.dirname(__file__) + "/model/raw_data.txt", "w") as file:
        for message in raw_data["messages"]:
            sentence = message["text"]
            # If the message contains a @mention, such mention is represented in json as a dictionary
            # and the message becomes a list containing text and dict
            # We iterate through the list and if there's a dictionary we grab only the text part
            try:
                if isinstance(sentence, list):
                    new_sentence = ""
                    for word in sentence:
                        if isinstance(word, dict):
                            new_sentence = new_sentence + " " + word["text"]
                        else:
                            new_sentence = new_sentence + " " + word
                    sentence = new_sentence
            except:
                continue
            sentence = cleaner(sentence)
            if sentence == "" or sentence == " ":
                continue
            file.write(sentence + " ")
            # debug
            print(str(i) + " " + str(sentence))
            i = i+1

    with open(os.path.dirname(__file__) + "/model/raw_data.txt", "r") as file:
        file_text = file.read()
        while "  " in file_text:
            file_text = file_text.replace("  ", " ")
        file = open(os.path.dirname(__file__) + "/model/raw_data.txt", "w")
        file.write(file_text)

    print("TIME IN SECONDS = " + str(time.time() - start))

if __name__ == "__main__":
    main() 
