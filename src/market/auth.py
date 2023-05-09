from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, ContextTypes, CommandHandler, MessageHandler, filters
from src import config as cfg
import os

CODE, VIDEO = range(2)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    print(f"User {str(user.first_name) + str(user.last_name)} ended auth conversation")
    await update.message.reply_text(
        "Operazione annullata", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
    
async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id)
    user_name = str(update.message.from_user.full_name)
    if not any(user_id in d.values() for d in cfg.users_list):
            cfg.add_user_to_list(user_id, user_name)
    elif cfg.is_seller(user_id):
        await update.message.reply_text("Sei già un venditore.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    
    await update.message.reply_text("Usa /annulla per annullare l'operazione, altrimenti premi su Autenticazione",
            reply_markup=ReplyKeyboardMarkup(
            [["Autenticazione"]], one_time_keyboard=True))
    
    return CODE

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f"Registra un video di te stesso mentre leggi il codice sottostante, mantenendo bene in vista un identificativo qualsiasi (carta d'identità, patente, etc.). Non è necessario inquadrare la faccia.\nUsa /annulla per annullare l'operazione.\n\n\n{cfg.get_code_from_id(update.message.from_user.id)}")
    return VIDEO

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    video = await context.bot.get_file(update.message.video)
    await video.download_to_drive(os.path.dirname(__file__) + f"/../data/auth_files/{update.message.from_user.id}.mp4")
    await context.bot.forward_message(cfg.approve_group, update.message.chat_id, update.message.message_id)
    await context.bot.send_message(cfg.approve_group, f"Codice: {cfg.get_code_from_id(update.message.from_user.id)}")
    await context.bot.send_message(cfg.approve_group, f"/makeseller {update.message.from_user.id}", 
                                   reply_markup=ReplyKeyboardMarkup([[f"/makeseller {update.message.from_user.id}"]] , 
                                                                    one_time_keyboard=True))
    await update.message.reply_text("Riceverai a breve una notifica di conferma.")
    return ConversationHandler.END
     
conv_handler = ConversationHandler(
        entry_points=[CommandHandler("seller", seller, filters.ChatType.PRIVATE)],
        states={
            CODE: [MessageHandler(filters.Regex("^(Autenticazione)$"), code), CommandHandler("annulla", cancel)],
            VIDEO: [MessageHandler(filters.VIDEO, video), CommandHandler("annulla", cancel)],
        },
        fallbacks=[CommandHandler("annulla", cancel)],
    )
