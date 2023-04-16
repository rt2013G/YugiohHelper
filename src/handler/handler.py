import random
from telegram import Update
from telegram.ext import ContextTypes
from src.card_search import card_search
from src.sentence_generator import sentence_gen
from src.sentence_generator import data_standardization as sen_ds
from src import config as cfg

# This handles all bot commands called with /
async def on_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Card search
    if update.message.text.startswith("/card"):
        await context.bot.send_message(update.message.chat_id, card_search.card_search(
            cfg.remove_tag(update.message.text.replace("/card ", ""))), 
            disable_web_page_preview=True)


    # ADMIN-ONLY COMMANDS
    # Toggle the auto answer feature
    if update.message.text.startswith("/toggle"):
        if str(update.message.from_user.id) not in cfg.admin_dic.values():
            return
        cfg.respond_to_msg = not cfg.respond_to_msg
        await context.bot.send_message(update.message.chat_id, 
                                       f"Messaggi automatici impostato su {str(cfg.respond_to_msg)}")
    
    if update.message.text.startswith("/setautoanswer"):
        if str(update.message.from_user.id) not in cfg.admin_dic.values():
            return
        try:
            new_num = int(cfg.remove_tag(update.message.text.replace("/setautoanswer", "")))
        except:
            print(cfg.remove_tag(update.message.text.replace("/setautoanswer", "")))
            return  
        cfg.msg_threshold = new_num
        await context.bot.send_message(update.message.chat_id, "Quantità di messaggi cambiata")

async def on_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.message.from_user.id)
        user_name = str(update.message.from_user.full_name)
    except:
        user_id = "none"
        user_name = "none"
    print(user_id + " " + user_name) # debug
    if cfg.bot_tag not in update.message.text :
        if (random.randint(0, 20) <= cfg.msg_threshold or not cfg.respond_to_msg):
            return
    
    # clean the message and grab only the last three elements
    text = cfg.remove_tag(sen_ds.cleaner(update.message.text)).split()[-3:]
    text = sentence_gen.sentence_gen(text, random.randint(5, (len(text) + 1) * (len(text) + 1) + 4))
    sentence = " ".join([w for w in text if w is not None])
    await update.message.reply_text(sentence)
