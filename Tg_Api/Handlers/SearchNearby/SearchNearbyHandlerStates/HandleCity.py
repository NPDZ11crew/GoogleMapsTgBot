from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def sendPrompt(update: Update, context: ContextTypes.DEFAULT_TYPE, PLACE_TYPE: int = 2):
    context.user_data['city'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Кафе", callback_data='cafe')],
        [InlineKeyboardButton("Магазин", callback_data='store')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери тип заведения:", reply_markup=reply_markup)

    return PLACE_TYPE
