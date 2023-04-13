from telegram import Update
from telegram.ext import ContextTypes
from src.card_search import card_search

# This handles all bot commands called with /
async def on_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Card search
    if update.message.text.startswith("/card"):
        await context.bot.send_message(update.message.chat_id, card_search.card_search(
            update.message.text.replace("/card ", "").replace("@yugiohmainbot", "")), 
            disable_web_page_preview=True)

# debug
async def get_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.message.from_user.id)
        user_name = str(update.message.from_user.full_name)
    except:
        user_id = "none"
        user_name = "none"
    print(user_id + " " + user_name)
    return
