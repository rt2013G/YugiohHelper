import json
import os
import time
import sys
import zlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

admin_dic = {}
with open(os.path.dirname(__file__) + "/data/admin.json") as fp:
    admin_dic = json.load(fp)

groups_dic = {}
with open(os.path.dirname(__file__) + "/data/groups.json") as fp:
    groups_dic = json.load(fp)

users_list = []
with open(os.path.dirname(__file__) + "/data/users.json") as fp:
    users_list = json.load(fp)

scam_list = []
with open(os.path.dirname(__file__) + "/data/scamlist.json") as fp:
    scam_list = json.load(fp)

feedback_list = []
with open(os.path.dirname(__file__) + "/data/feedback.json") as fp:
    feedback_list = json.load(fp)

def save_files():
    with open(os.path.dirname(__file__) + "/data/admin.json", "w") as fp:
        json.dump(admin_dic, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/groups.json", "w") as fp:
        json.dump(groups_dic, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/users.json", "w") as fp:
        json.dump(users_list, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/scamlist.json", "w") as fp:
        json.dump(scam_list, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/feedback.json", "w") as fp:
        json.dump(feedback_list, fp, indent=4)
    print("Files saved at " + str(datetime.now()))

if len(sys.argv) == 2 and sys.argv[1] == "ygodeploy":
    bot_token = os.getenv("bot_token")
    bot_tag = "@yugiohmainbot"
    market_id = int(groups_dic["market"])
    feedback_id = int(groups_dic["feedback"])
    #heroku_port = int(os.environ.get("PORT"))
else:
    bot_token = os.getenv("bot_token_test") 
    bot_tag = "@yugiohhelpertestbot"
    market_id = int(groups_dic["market_beta"])
    feedback_id = int(groups_dic["market_beta"])

main_id = int(groups_dic["main"])
auction_id = int(groups_dic["auction"])
approve_group = int(groups_dic["approve_group"])
log_channel_id = int(groups_dic["log_channel"])
last_sync = time.time()

# Other utilities
def remove_tag(text):
    text = text.replace(bot_tag, "")
    return text

# id: Telegram user id
# name: Telegram full name
# tag: Telegram username
# is_seller: True if user has completed seller auth process, False by default
# is_active: True if user has started a chat with the bot, False by default
# last_sell_post: Date of last sell post
# last_buy_post: Date of last buy post
def add_user_to_list(user_id, user_name, tag, is_seller=False, is_active=False,
                     last_sell_post="2015-01-15", last_buy_post="2015-01-15"):
    users_list.append({"id": str(user_id), "name": str(user_name), "tag": "@" + str(tag),
                       "is_seller": is_seller, "is_active": is_active,
                       "last_sell_post": str(last_sell_post), "last_buy_post": str(last_buy_post)})

def is_active(user_id):
    if not any(user_id in d.values() for d in users_list):
        return False
    return list(filter(lambda x: x["id"] == user_id, users_list))[0]["is_active"]

def is_seller(user_id):
    if not any(user_id in d.values() for d in users_list):
        return False
    return list(filter(lambda x: x["id"] == user_id, users_list))[0]["is_seller"]

def is_scammer(user_id):
    return user_id in scam_list

def is_admin(user_id):
    return user_id in admin_dic.values()

def is_superadmin(user_id):
    return user_id == admin_dic["raffaele"]

def get_id_from_tag(tag):
    return list(filter(lambda x: x["tag"] == tag, users_list))[0]["id"]

def get_tag_from_id(user_id):
    return list(filter(lambda x: x["id"] == user_id, users_list))[0]["tag"]

def get_tag_from_text(text):
    for word in text.replace(",", "").replace(".", "").replace("!", "").split():
        if "@" in word:
            print(word)
            return word
    return ""

def get_code_from_id(user_id):
    code = "%08X" % zlib.adler32(str(user_id).encode())
    return code[:-2]

def get_admin_from_id(user_id):
    index = "%08X" % zlib.adler32(str(user_id).encode())
    index = int(index, 16) % len(admin_dic)
    admin_id = list(admin_dic.values())[index]
    return admin_id

def get_feedback(user_id):
    list_to_return = []
    if not any(user_id in d.values() for d in feedback_list):
        return []
    else:
        for feedback in list(filter(lambda x: x["id"] == user_id, feedback_list))[0]["feedback_list"]:
            list_to_return.append("Feedback di: " + feedback["from_tag"] + " (ID " + feedback["from_id"] + "):\n" + feedback["text"])
        return list_to_return

def add_feedback(user_id, from_user_id, text):
    dic_to_ins = {"from_id": str(from_user_id), "from_tag": get_tag_from_id(from_user_id), "text": text}
    if not any(user_id in d.values() for d in feedback_list):
        feedback_list.append({"id": str(user_id), "feedback_list": [dic_to_ins]})
    else:
        list(filter(lambda x: x["id"] == user_id, feedback_list))[0]["feedback_list"].append(dic_to_ins)

def update_user(user_id, user_name, tag):
    list(filter(lambda x: x["id"] == user_id, users_list))[0]["name"] = user_name
    list(filter(lambda x: x["id"] == user_id, users_list))[0]["tag"] = "@" + tag

def reset_date(user_id):
    if not any(user_id in d.values() for d in users_list):
        return False
    list(filter(lambda x: x["id"] == user_id, users_list))[0]["last_sell_post"] = "2015-01-15"
    list(filter(lambda x: x["id"] == user_id, users_list))[0]["last_buy_post"] = "2015-01-15"
    return True

# ugly, will fix later
def is_sell_post(message):
    text = message.lower()
    return "#vendo" in text or "vendo" in text or "vendere" in text or "vendesi" in text or "vendono" in text

def is_buy_post(message):
    text = message.lower()
    return "#cerco" in text or "cerco" in text or "compro" in text or "cercare" in text or "cercasi" in text or "cercano" in text

def is_feedback(message):
    text = message.lower()
    return "#feedback" in text or "feedback" in text or "feed" in text or "feedb" in text or "feed" in text

def get_date(user_id, is_sell_post):
    if is_sell_post:
        return list(filter(lambda x: x["id"] == user_id, users_list))[0]["last_sell_post"]
    else:
        return list(filter(lambda x: x["id"] == user_id, users_list))[0]["last_buy_post"]

def set_date_today(user_id, is_sell_post):
    if is_sell_post:
        list(filter(lambda x: x["id"] == user_id, users_list))[0]["last_sell_post"] = str(datetime.today().date())
    else:
        list(filter(lambda x: x["id"] == user_id, users_list))[0]["last_buy_post"] = str(datetime.today().date())

start_msg = f"""Benvenuto sul gruppo Yu-Gi-Oh ITA Main.
Per entrare nel gruppo market segui questo link: {groups_dic["market_link"]}.\n
Ricorda di leggere le regole! Solo i venditori approvati possono vendere sul gruppo.
Se vuoi diventare venditore, usa il comando /seller.\n
Ricorda che in ogni caso, puoi effettuare solo 1 post di vendita e 1 post di acquisto al giorno."""

gdpr_msg = f"""Al fine di limitare il numero di truffatori, per autenticarsi come seller è necessario fornire un identificativo.
Se non si vuole vendere sul gruppo, NON è ovviamente obbligatorio autenticarsi.
Il video inviatoci è visibile soltanto agli amministratori del gruppo market, e viene salvato dal bot. Non è condiviso con nessun altro.
Il video non viene utilizzato per nessuno scopo ECCETTO in caso di truffa da parte di un venditore, in quel caso potrebbe essere utilizzato al fine di risalire all'identità del truffatore.
"""
