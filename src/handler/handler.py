from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.card_search import card_search
from src import config as cfg
from datetime import datetime

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.message.chat_id, cfg.start_msg)

# Card search with /card
async def card_search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.message.chat_id, card_search.card_search(
        cfg.remove_tag(update.message.text.replace("/card ", ""))), 
        disable_web_page_preview=True)
    
# Command to approve a seller, usage: /makeseller <user_id>, will be changed in the future
async def make_seller(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if cfg.is_admin(str(update.message.from_user.id)):
        user_id = cfg.remove_tag(update.message.text.replace("/makeseller ", ""))
        if any(user_id in d.values() for d in cfg.users_list):
            list(filter(lambda x: x["id"] == user_id, cfg.users_list))[0]["is_seller"] = True
            await context.bot.send_message(user_id, "Sei stato approvato come venditore, ora puoi vendere nel gruppo market!", 
                                           reply_markup=ReplyKeyboardRemove())
            await context.bot.send_message(update.message.chat_id, "Utente approvato come venditore!", 
                                           reply_markup=ReplyKeyboardRemove())
        else:
            await context.bot.send_message(update.message.chat_id, "Utente non trovato!", 
                                           reply_markup=ReplyKeyboardRemove())
    else:
        return
    
# Command to approve a seller, usage: /removerseller <user_id>, will be changed in the future
async def remove_seller(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if cfg.is_admin(str(update.message.from_user.id)):
        user_id = cfg.remove_tag(update.message.text.replace("/removeseller ", ""))
        if any(user_id in d.values() for d in cfg.users_list):
            list(filter(lambda x: x["id"] == user_id, cfg.users_list))[0]["is_seller"] = False
            await context.bot.send_message(user_id, "Non sei più un venditore, non puoi più vendere nel gruppo market!", 
                                           reply_markup=ReplyKeyboardRemove())
            await context.bot.send_message(update.message.chat_id, "Utente rimosso dai venditori!", 
                                           reply_markup=ReplyKeyboardRemove())
        else:
            await context.bot.send_message(update.message.chat_id, "Utente non trovato!", 
                                           reply_markup=ReplyKeyboardRemove())
    else:
        return
    
async def market_msg_updater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # debug
    try:
        user_id = str(update.message.from_user.id)  
    except:
        return
    
    try:
        text = update.message.text
    except:
        text = update.message.caption

    if cfg.is_sell_post(text):
        if datetime.now().day - list(filter(lambda x: x["id"] == user_id, cfg.users_list))[0]["last_sell_post"] == 0:
            await context.bot.send_message(user_id, "Hai già inviato un post di vendo oggi!")
            await update.message.delete()
        list(filter(lambda x: x["id"] == user_id, cfg.users_list))[0]["last_sell_post"] = datetime.now().day

    if cfg.is_buy_post(text):
        if datetime.now().day - list(filter(lambda x: x["id"] == user_id, cfg.users_list))[0]["last_buy_post"] == 0:
            await context.bot.send_message(user_id, "Hai già inviato un post di cerco oggi!")
            await update.message.delete()
        list(filter(lambda x: x["id"] == user_id, cfg.users_list))[0]["last_buy_post"] = datetime.now().day


# debug
async def on_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.message.from_user.id)
        user_name = str(update.message.from_user.full_name)
        if not any(user_id in d.values() for d in cfg.users_list):
            cfg.add_user_to_list(user_id, user_name)
    except:
        return
    print(user_id + " " + user_name)
    print("  group: " + str(update.message.chat_id))
