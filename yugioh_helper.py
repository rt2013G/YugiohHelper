import logging
import os
import json
from telegram.ext import (
    Application,
    MessageHandler,
    filters
)
from dotenv import load_dotenv
from src.handler import handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
bot_token = os.getenv("bot_token")

def main():
    application = Application.builder().token(bot_token).build()
    print("Bot started")
    application.add_handler(MessageHandler(filters.COMMAND, handler.on_command))
    application.add_handler(MessageHandler(filters.TEXT, handler.get_user_id))
    application.run_polling()

if __name__ == "__main__":
    main()
