from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, ContextTypes, CommandHandler, MessageHandler, filters
from src import config as cfg
import random

CODE, VIDEO = range(2)
admin_id = random.choice(list(cfg.admin_dic.values()))

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
    cfg.auth_code = random.randint(100000, 999999)
    await update.message.reply_text(f"Registra un video di te stesso mentre leggi il codice sottostante, mantenendo bene in vista un identificativo qualsiasi (carta d'identità, patente, etc.)\nUsa /annulla per annullare l'operazione.\n\n\n{cfg.auth_code}")
    return VIDEO

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    admin_id = random.choice(list(cfg.admin_dic.values()))
    await context.bot.forward_message(admin_id, update.message.chat_id, update.message.message_id)
    await context.bot.send_message(admin_id, f"Codice: {cfg.auth_code}")
    await context.bot.send_message(admin_id, f"Rendi l'utente un venditore con il comando /makeseller {update.message.from_user.id}", 
                                   reply_markup=ReplyKeyboardMarkup([[f"/makeseller {update.message.from_user.id}"]] , 
                                                                    one_time_keyboard=True))
    await update.message.reply_text("Riceverai a breve una notifica di conferma.")
    return ConversationHandler.END
     
conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.ChatType.PRIVATE & filters.COMMAND, seller)],
        states={
            CODE: [MessageHandler(filters.Regex("^(Autenticazione)$"), code), CommandHandler("annulla", cancel)],
            VIDEO: [MessageHandler(filters.VIDEO, video), CommandHandler("annulla", cancel)],
        },
        fallbacks=[CommandHandler("annulla", cancel)],
    )
