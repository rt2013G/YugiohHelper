import random
import os
import dill as pickle
from nltk.corpus import stopwords

with open(os.path.dirname(__file__) + "/model/fourgram_model.pickle","rb") as fp:
    fourgram_model = pickle.load(fp)
    print("FOURGRAM LOADED")

with open(os.path.dirname(__file__) + "/model/trigram_model.pickle","rb") as fp:
    trigram_model = pickle.load(fp)
    print("TRIGRAM LOADED")

with open(os.path.dirname(__file__) + "/model/bigram_model.pickle","rb") as fp:
    bigram_model = pickle.load(fp)
    print("BIGRAM LOADED")  

def sentence_gen(input_text, sentence_len):
    text = input_text
    for i in range(sentence_len):
        # for the lack of better ideas:
        threshold = random.random()
        probability = 0.01

        # Let w1 w2 w3 be the last three elements of text, check if w1_w2_w3 is in the fourgram model
        # if it is, iterate all possible next words w4 and keep stacking probabilities
        # until a certain (random) threshold is reached.
        if len(text) >= 3 and fourgram_model.get(tuple(text[-3:])) is not None:
            for word in fourgram_model[tuple(text[-3:])].keys():
                probability += fourgram_model[tuple(text[-3:])][word]
                if probability > threshold:
                    text.append(word)
                    break

        # If the fourgram w1 w2 w3 w4 doesn't exist, check for the trigram w1 w2 w3
        # if that doesn't exist either, check for the bigram w1 w2     
        elif trigram_model.get(tuple(text[-2:])) is not None:
            for word in trigram_model[tuple(text[-2:])].keys():
                probability += trigram_model[tuple(text[-2:])][word]
                if probability > threshold:
                    text.append(word)
                    break
        elif bigram_model.get(text[-1]) is not None:
            for word in bigram_model[text[-1]].keys():
                probability += bigram_model[text[-1]][word]
                if probability > threshold:
                    text.append(word)
                    break
        
        # if all else fails, pick a word w2 from the bigram default_word w2      
        else:
            default_word = random.choice(stopwords.words("italian"))
            for word in bigram_model[default_word].keys():
                probability += bigram_model[default_word][word]
                if probability > threshold:
                    text.append(word)
                    break
    return text[3:]

def main():
    while(True):
        text = input("Insert three words\n")
        text = text.split()
        sentence = sentence_gen(text, 100)
        print(" ".join([w for w in sentence if w is not None]))

if __name__ == "__main__":
    main()
