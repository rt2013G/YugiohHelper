import logging
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    filters
)
from src.handler import handler
from src import config as cfg
from src.market import auth

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(cfg.bot_token).build()
    print("Bot started")
    application.add_handler(CommandHandler("start", handler.start, filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("card", handler.card_search_cmd))
    application.add_handler(CommandHandler("makeseller", handler.make_seller, filters.ChatType.PRIVATE | filters.Chat(chat_id=cfg.approve_group)))
    application.add_handler(CommandHandler("removeseller", handler.remove_seller, filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("checkseller", handler.check_seller))
    application.add_handler(CommandHandler("checkscammer", handler.check_scammer))
    application.add_handler(CommandHandler("feedback", handler.check_feedback, filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("addadmin", handler.add_admin, filters.ChatType.PRIVATE | filters.Chat(chat_id=cfg.approve_group)))
    application.add_handler(CommandHandler("announce", handler.announce, filters.ChatType.PRIVATE))
    application.add_handler(auth.conv_handler)
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handler.channel_msg_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.Chat(chat_id=cfg.market_id), handler.on_user_msg))
    application.add_handler(MessageHandler(filters.Chat(chat_id=cfg.market_id) & ~filters.COMMAND, handler.market_msg_updater))
    application.run_polling(drop_pending_updates=True)
    cfg.save_files()

if __name__ == "__main__":
    main()
