from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


BUTTONS_PER_PAGE = 5

category_dict = {
    "Automotive": 0,
    "Business": 1,
    "Culture": 2,
    "Education": 3,
    "Entertainment And Recreation": 4,
    "Facilities": 5,
    "Finance": 6,
    "Food And Drink": 7,
    "Government": 8,
    "Health And Wellness": 9,
    "Housing": 10,
    "Lodging": 11,
    "Natural Features": 12,
    "Places Of Worship": 13,
    "Services": 14,
    "Shopping": 15,
    "Sports": 16,
    "Transportation": 17
}

category_names = list(category_dict.keys())


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await show_category_page(update, context, page=page)
    elif data.startswith("category_"):
        # Тут логика для выбора категории
        pass
    else:
        await query.answer("Неизвестная команда")




async def show_category_page(update, context, page=0, PLACE_TYPE: int = 2):

    start = page * BUTTONS_PER_PAGE
    end = start + BUTTONS_PER_PAGE
    page_items = category_names[start:end]

    buttons = [
        [InlineKeyboardButton(name, callback_data=f"category_page{category_dict[name]}")]
        for name in page_items
    ]

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("⏮ Назад", callback_data=f"page_{page - 1}"))
    if end < len(category_names):
        navigation_buttons.append(InlineKeyboardButton("Вперёд ⏭", callback_data=f"page_{page + 1}"))
    if navigation_buttons:
        buttons.append(navigation_buttons)

    reply_markup = InlineKeyboardMarkup(buttons)

    if update.callback_query:
        await update.callback_query.edit_message_text("Выбери тип заведения:", reply_markup=reply_markup)
        await update.callback_query.answer()
    else:
        await update.message.reply_text("Выбери тип заведения:", reply_markup=reply_markup)

    context.user_data["category_page"] = page
    return PLACE_TYPE


async def sendPrompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    return await show_category_page(update, context, page=0)

