from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id, text="end")
    return ConversationHandler.END
