import json
import urllib

id_database = json.load(open("src/data/id_database.json", "r"))
card_database = "https://db.ygorganization.com/data/card/"
ruling_database = "https://db.ygorganization.com/card#"    

def lcs(X, Y, m, n):
    memo = [[None] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                memo[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                memo[i][j] = memo[i - 1][j - 1] + 1
            else:
                memo[i][j] = max(memo[i - 1][j], memo[i][j - 1])
    return memo[m][n]

def card_search(text):
    # Json of the form {Name:[ID]}
    text = str.title(text)
    max_text = text
    if text in id_database.keys():
        card_id = id_database[text]
    else:
        max_so_far = 0
        max = 0
        for key in id_database.keys():
            # print(key) # debug
            max = lcs(text, key, len(text), len(key))
            if max > max_so_far:
                max_so_far = max
                max_text = key
        card_id = id_database[max_text]    
    # Opens the url at https://db.ygorganization.com/data/card/ID
    # which returns a Json containing all the informations regarding the card
    with urllib.request.urlopen(card_database + str(card_id[0])) as card_url:
        card_data = json.loads(card_url.read().decode())
        name = card_data["cardData"]["en"]["name"]
        text = card_data["cardData"]["en"]["effectText"]
        try:
            pendulum_effect = card_data["cardData"]["en"]["pendulumEffectText"]
        except:
            pendulum_effect = None
    if pendulum_effect is not None:
        text = ( name + "\n\n" + text + "\n\n" + "Pendulum effect:" + "\n"
                + pendulum_effect + "\n\n" + "Rulings: " + ruling_database + 
                str(card_id).replace("[", "").replace("]", "")
        )  
    else :
        text = ( name + "\n\n" + text + "\n\n" + "Rulings: " + ruling_database + 
                str(card_id).replace("[", "").replace("]", "")
            )            
    return text
      