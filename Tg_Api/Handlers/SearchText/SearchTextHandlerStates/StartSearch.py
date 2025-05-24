from telegram import Update
from telegram.ext import ContextTypes


async def startSearchByText(update: Update, context: ContextTypes.DEFAULT_TYPE, SEARCH_TEXT=0):
    await context.bot.send_message(chat_id=update.message.chat_id, text="Send me a name of the place you wanna find!")
    return SEARCH_TEXT
