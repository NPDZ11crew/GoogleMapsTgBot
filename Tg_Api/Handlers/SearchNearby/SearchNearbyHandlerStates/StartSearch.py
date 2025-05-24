from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, LOCATION: int = 0):
    # Кнопка для отправки геолокации
    location_button = KeyboardButton(text="📍 Отправить геолокацию", request_location=True)
    manual_button = KeyboardButton(text="🏙 Ввести название города")
    reply_markup = ReplyKeyboardMarkup([[location_button], [manual_button]],
                                       resize_keyboard=True,
                                       one_time_keyboard=True)

    await update.message.reply_text(
        "Выберите способ указания местоположения:",
        reply_markup=reply_markup
    )

    return LOCATION
