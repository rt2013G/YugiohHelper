import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("bot_token") 
# heroku_port = int(os.environ.get("PORT")) # uncomment this line for heroku

bot_tag = "@yugiohmainbot"

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

def save_files():
    with open(os.path.dirname(__file__) + "/data/admin.json", "w") as fp:
        json.dump(admin_dic, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/groups.json", "w") as fp:
        json.dump(groups_dic, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/users.json", "w") as fp:
        json.dump(users_list, fp, indent=4)
    with open(os.path.dirname(__file__) + "/data/scamlist.json", "w") as fp:
        json.dump(scam_list, fp, indent=4)

# Other utilities
def remove_tag(text):
    text = text.replace(bot_tag, "")
    return text

# for now we only need to check the day
def add_user_to_list(user_id, user_name, is_seller=False, 
                     last_sell_post=datetime.now().day-1, last_buy_post=datetime.now().day-1):
    users_list.append({"id": user_id, "name": user_name, "is_seller": is_seller, 
                       "last_sell_post": last_sell_post, "last_buy_post": last_buy_post})

def is_seller(user_id):
    return list(filter(lambda x: x["id"] == user_id, users_list))[0]["is_seller"]

def is_scammer(user_id):
    return user_id in scam_list

def is_admin(user_id):
    return user_id in admin_dic.values()

def is_superadmin(user_id):
    return user_id == admin_dic["raffaele"]

def is_sell_post(message):
    return "#vendo" in message or "vendo" in message or "vendere" in message or "vendesi" in message or "vendono" in message.lower()

def is_buy_post(message):
    return "#compro" in message or "compro" in message or "comprare" in message or "comprasi" in message or "comprano" in message.lower()


# Default messages
start_msg = "Welcome to Yu-Gi-Oh! Main Bot!\n\n"

auth_code = 0
market_id = int(groups_dic["market_beta"])
main_id = int(groups_dic["main"])