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

def build_category_keyboard(selected: set, page: int = 0):
    start = page * BUTTONS_PER_PAGE
    end = start + BUTTONS_PER_PAGE
    page_items = category_names[start:end]
    buttons = []

    for name in page_items:
        checked = "✅" if name in selected else ""
        buttons.append([
            InlineKeyboardButton(f"{checked}{name}", callback_data=f"cat_{category_dict[name]}")
        ])

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("⏮ Назад", callback_data=f"page_{page-1}"))
    if end < len(category_names):
        navigation_buttons.append(InlineKeyboardButton("Вперёд ⏭", callback_data=f"page_{page+1}"))

    navigation_buttons.append(InlineKeyboardButton("Готово", callback_data="done_selecting"))

    if navigation_buttons:
        buttons.append(navigation_buttons)
    return InlineKeyboardMarkup(buttons)



async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, PLACE_TYPE:int=2, SUBTYPE:int = 3):
    data = update.callback_query.data
    selected = context.user_data.get("selected_categories", set())

    if data.startswith("cat_"):
        idx = int(data.split("_")[1])
        name = category_names[idx]
        # Переключаем выбор
        if name in selected:
            selected.remove(name)
        else:
            selected.add(name)
        context.user_data["selected_categories"] = selected
        # Перерисовываем клавиатуру на той же странице
        page = context.user_data.get("category_page", 0)
        await update.callback_query.edit_message_text(
            "Выбери типы заведений (можно несколько):",
            reply_markup=build_category_keyboard(selected, page)
        )
        await update.callback_query.answer()

    elif data.startswith("page_"):
        page = int(data.split("_")[1])
        context.user_data["category_page"] = page
        await update.callback_query.edit_message_text(
            "Выбери типы заведений (можно несколько):",
            reply_markup=build_category_keyboard(selected, page)
        )
        await update.callback_query.answer()

    elif data == "done_selecting":
        # Список выбранных категорий
        selected_list = list(selected)
        # Переходим к следующему состоянию и обрабатываем выбранные категории
        await update.callback_query.edit_message_text(
            f"Ты выбрал: {', '.join(selected_list)}"
        )
        await update.callback_query.answer()
        # Переход к следующему шагу
        return SUBTYPE

    return PLACE_TYPE  # Остаёмся в этом состоянии, пока не нажали "Готово"



# async def show_category_page(update, context, page=0, PLACE_TYPE: int = 2):
#     start = page * BUTTONS_PER_PAGE
#     end = start + BUTTONS_PER_PAGE
#     page_items = category_names[start:end]
#
#     buttons = [
#         [InlineKeyboardButton(name, callback_data=f"category_{category_dict[name]}")]
#         for name in page_items
#     ]
#
#     navigation_buttons = []
#     if page > 0:
#         navigation_buttons.append(InlineKeyboardButton("⏮ Назад", callback_data=f"page_{page - 1}"))
#     if end < len(category_names):
#         navigation_buttons.append(InlineKeyboardButton("Вперёд ⏭", callback_data=f"page_{page + 1}"))
#     if navigation_buttons:
#         buttons.append(navigation_buttons)
#
#     reply_markup = InlineKeyboardMarkup(buttons)
#
#     if update.callback_query:
#         # Получаем текущий reply_markup
#         current_markup = update.callback_query.message.reply_markup
#         if current_markup and current_markup.to_dict() == reply_markup.to_dict():
#             # Клавиатура не изменилась — ничего не делаем
#             await update.callback_query.answer()
#         else:
#             await update.callback_query.edit_message_text(
#                 "Выбери тип заведения:",
#                 reply_markup=reply_markup
#             )
#             await update.callback_query.answer()
#     else:
#         await update.message.reply_text("Выбери тип заведения:", reply_markup=reply_markup)
#
#     return PLACE_TYPE


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE, HANDLE_CITY: int = 1):
    if update.message.location:
        context.user_data['location'] = update.message.location
        return await show_category_page(update, context, page=0)
    else:
        await update.message.reply_text("Напиши город вручную без ошибок!)")
        return HANDLE_CITY


async def handle_category_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    # data = "page_1", "page_2" и т.д.
    page = int(data.split('_')[1])
    await show_category_page(update, context, page=page)

    # Кнопки выбора типа
