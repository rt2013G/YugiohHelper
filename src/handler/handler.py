from telegram import Update
from telegram.ext import ContextTypes
from src.card_search import card_search
from src import config as cfg

# This handles all bot commands called with /
async def on_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Card search
    if update.message.text.startswith("/card"):
        await context.bot.send_message(update.message.chat_id, card_search.card_search(
            cfg.remove_tag(update.message.text.replace("/card ", ""))), 
            disable_web_page_preview=True)

    # ADMIN-ONLY COMMANDS GO HERE
    # Toggle the auto answer feature


# debug
async def on_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.message.from_user.id)
        user_name = str(update.message.from_user.full_name)
    except:
        user_id = "none"
        user_name = "none"
    print(user_id + " " + user_name)
