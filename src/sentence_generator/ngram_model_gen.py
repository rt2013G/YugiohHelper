import dill as pickle
from collections import defaultdict
from nltk import ngrams

# This file is a standalone script used to generate ngrams of a txt file
# Those ngrams will then be stored into a pickle file and used to generate sentences
def main():
    raw_data_txt = open("/model/raw_data.txt", "r")
    text = raw_data_txt.read().split()
    
    model = defaultdict(lambda: defaultdict(lambda: 0))
    for w1, w2, w3, w4 in ngrams(text, 4, pad_right=True, pad_left=True):
        model[(w1, w2, w3)][w4] += 1
    
    for w1_w2_w3 in model:
        total_count = float(sum(model[w1_w2_w3].values()))
        for w4 in model[w1_w2_w3]:
            model[w1_w2_w3][w4] /= total_count

    with open("/model/fourgram_model.pickle", "wb") as fp:
        pickle.dump(model, fp)
        print("FILE SAVED")

if __name__ == "__main__":
    main()
