from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.card_search import card_search
from src import config as cfg
from datetime import datetime
import time

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = str(update.message.from_user.id)
    try:
        user_tag = str(update.message.from_user.username)
    except:
        user_tag = "N/A"
    if not any(id in d.values() for d in cfg.users_list):
        cfg.add_user_to_list(id, str(update.message.from_user.full_name), user_tag, is_active=True)
    else:
        list(filter(lambda x: x["id"] == id, cfg.users_list))[0]["is_active"] = True
    await context.bot.send_message(update.message.chat_id, cfg.start_msg, 
                                   disable_web_page_preview=True)

# Card search with /card
async def card_search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.message.chat_id, card_search.card_search(
        cfg.remove_tag(update.message.text.replace("/card ", ""))), 
        disable_web_page_preview=True)
    
# Command to approve a seller, usage: /makeseller <user_id>
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
            cfg.add_user_to_list(user_id, "N/A", "N/A", is_seller=True)
            await context.bot.send_message(update.message.chat_id, "Utente approvato come venditore!", 
                                           reply_markup=ReplyKeyboardRemove())
    else:
        return
    
# Command to approve a seller, usage: /removerseller <user_id>
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

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = str(update.message.from_user.id)
    if not cfg.is_superadmin(id):
        return
    new_admin_id = cfg.get_id_from_tag(cfg.remove_tag(update.message.text.replace("/addadmin ", "")))
    if cfg.is_admin(new_admin_id):
        await context.bot.send_message(update.message.chat_id, "Utente già admin!")
        return
    cfg.admin_dic[cfg.get_tag_from_id(new_admin_id)] = new_admin_id
    await context.bot.send_message(update.message.chat_id, "Utente aggiunto come admin!")

# Command to check if user_id is a seller or not, usage: /checkseller @username
async def check_seller(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = cfg.get_id_from_tag(cfg.remove_tag(update.message.text.replace("/checkseller ", "")))
    if cfg.is_seller(user_id):
        await context.bot.send_message(update.message.chat_id, "L'utente è un venditore!")
    else:
        await context.bot.send_message(update.message.chat_id, "L'utente non è un venditore!")

# Command to check if user_id is an scammer or not, usage: /checkscammer @username
async def check_scammer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = cfg.get_id_from_tag(cfg.remove_tag(update.message.text.replace("/checkscammer ", "")))
    if cfg.is_scammer(user_id):
        await context.bot.send_message(update.message.chat_id, "L'utente è uno scammer!")
    else:
        await context.bot.send_message(update.message.chat_id, "L'utente non è attualmente presente nella lista scammer!")

async def check_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = cfg.get_id_from_tag(cfg.remove_tag(update.message.text.replace("/feedback ", "")))
    list = cfg.get_feedback(user_id)
    for feedback in list:
        await context.bot.send_message(update.message.chat_id, f"{feedback}")
    await context.bot.send_message(update.message.chat_id, str(len(list)) + " feedback trovati!")
    
async def market_msg_updater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if time.time() - cfg.last_sync > 300:
        cfg.save_files()
        cfg.last_sync = time.time()

    try:
        user_id = str(update.message.from_user.id)
    except:
        return
    try:
        user_tag = str(update.message.from_user.username)
    except:
        user_tag = "N/A"
    try:
        text = update.message.text
    except:
        text = update.message.caption

    if cfg.is_admin(user_id):
        return

    if not any(user_id in d.values() for d in cfg.users_list) or not cfg.is_active(user_id):
        await update.message.delete()
        return

    if(cfg.is_scammer(user_id)):
        await context.bot.send_message(update.message.chat_id, f"Ho eliminato il messaggio di {update.message.from_user.full_name}, tag: @{user_tag} perche' e' uno scammer!")
        await update.message.delete()
        return

    cfg.update_user(user_id, str(update.message.from_user.full_name), user_tag)

    if cfg.is_feedback(text):
        print(cfg.get_tag_from_text(text))
        if "@" not in text:
            return
        await update.message.forward(cfg.feedback_id)
        cfg.add_feedback(cfg.get_id_from_tag(cfg.get_tag_from_text(text)), text)
        return

    if cfg.is_sell_post(text):
        if not cfg.is_seller(user_id):
            await context.bot.send_message(user_id, "Il tuo messaggio è stato eliminato, non sei un venditore! Usa /seller per poter vendere nel gruppo market.")
            await update.message.delete()
            return
        if str(datetime.now().date()) == cfg.get_date(user_id, is_sell_post=True):
            await context.bot.send_message(user_id, "Il tuo messaggio è stato eliminato, hai già inviato un post di vendo oggi!")
            await update.message.delete()
        cfg.set_date_today(user_id, is_sell_post=True)

    if cfg.is_buy_post(text):
        if str(datetime.now().date()) == cfg.get_date(user_id, is_sell_post=False):
            await context.bot.send_message(user_id, "Il tuo messaggio è stato eliminato, hai già inviato un post di cerco oggi!")
            await update.message.delete()
        cfg.set_date_today(user_id, is_sell_post=False)

# debug
async def on_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if time.time() - cfg.last_sync > 300:
        cfg.save_files()
        cfg.last_sync = time.time()
    try:
        user_id = str(update.message.from_user.id)
        user_name = str(update.message.from_user.full_name)
        user_tag = str(update.message.from_user.username)
        if not any(user_id in d.values() for d in cfg.users_list):
            cfg.add_user_to_list(user_id, user_name, user_tag)
        else:
            cfg.update_user(user_id, user_name, user_tag)
    except:
        return
    print(user_id + " " + user_name)
    print("  group: " + str(update.message.chat_id))

# debug
async def channel_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(str(update.channel_post.chat_id) + " " + str(update.channel_post.chat.title))
