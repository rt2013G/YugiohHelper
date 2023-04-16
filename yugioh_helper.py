import logging
from telegram.ext import (
    Application,
    MessageHandler,
    filters
)
from src.handler import handler
from src import config as cfg

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(cfg.bot_token).build()
    print("Bot started")
    application.add_handler(MessageHandler(filters.COMMAND, handler.on_command))
    application.add_handler(MessageHandler(filters.TEXT, handler.on_user_msg))
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
