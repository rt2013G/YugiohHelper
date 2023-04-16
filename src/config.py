import json
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("bot_token")

admin_dic = {}
with open(os.path.dirname(__file__) + "/data/admin.json") as fp:
    admin_dic = json.load(fp)

bot_tag = "@kekocirankbot"

# enable or disable the auto-answer function
respond_to_msg = True
# -1 = every message is auto-answered, 20 or more = no auto-answers
msg_threshold = 18

def remove_tag(text):
    text = text.replace(bot_tag, "").replace("@yugiohmainbot", "")
    return text
