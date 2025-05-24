from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE, HANDLE_CITY:int = 1, PLACE_TYPE: int = 2):
    if update.message.location:
        context.user_data['location'] = update.message.location
        keyboard = [
            [InlineKeyboardButton("Кафе", callback_data='cafe')],
            [InlineKeyboardButton("Магазин", callback_data='store')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выбери тип заведения:", reply_markup=reply_markup)
        return PLACE_TYPE
    else:
        await context.bot.send_message(update.message.chat_id, text="Напиши город вручную без ошибок!)")
        return HANDLE_CITY
    # Кнопки выбора типа

