from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_subtype(update: Update, context: ContextTypes.DEFAULT_TYPE,RADIUS=3):
    query = update.callback_query
    await query.answer()
    context.user_data['subtype'] = query.data

    await query.edit_message_text("Укажи радиус поиска (в км):")
    return RADIUS



