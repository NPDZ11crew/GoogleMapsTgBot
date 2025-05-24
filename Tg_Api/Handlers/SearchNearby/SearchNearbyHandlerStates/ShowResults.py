from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Update, InputMedia, InputMediaPhoto
from telegram.ext import ContextTypes
from GoogleMapsApi import SearchNearbyByGeo  # твой модуль


async def handle_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.split("_")[1])
    return await show_results(query, context, page=page)


async def show_results(update_or_query: Update | CallbackQuery,
                       context: ContextTypes.DEFAULT_TYPE,
                       page: int = 1):
    data = context.user_data

    # Получаем места
    if data.get("location"):
        lat = data['location'].latitude
        lng = data['location'].longitude
        results = await SearchNearbyByGeo(
            groupOfFacility=data['type'],
            typesOfFacility=data['sybtype'],
            lat=lat,
            lng=lng,
            rad=data['radius']
        )
    else:
        results = await SearchNearbyByGeo(
            groupOfFacility=data['type'],
            typesOfFacility=data['sybtype'],
            city=data['city']
        )

    if not results:
        msg = "Ничего не найдено."
        if isinstance(update_or_query, CallbackQuery):
            await update_or_query.edit_message_text(msg)
        else:
            await update_or_query.message.reply_text(msg)
        return

    # Пагинация
    per_page = 1
    total_pages = (len(results) - 1) // per_page + 1
    page = max(1, min(page, total_pages))  # защита от выхода за пределы
    start = (page - 1) * per_page
    place = results[start]


    # Извлекаем и форматируем данные
    name = place.get("displayName", {}).get("text", "")
    address = place.get("formattedAddress", "")
    phone = place.get("nationalPhoneNumber", "")
    photos = InputMediaPhoto(place.get("photos")[0])
    rating = place.get("rating")
    maps_url = place.get("googleMapsUri")

    text = f"<b>{name}</b>\n📍 {address}\n📞 {phone}\n🌐 {maps_url}\n Rating: {rating}🌟\n\n<i>Страница {page} из {total_pages}</i>"

    # Кнопки пагинации
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{page - 1}"))
    if page < total_pages:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"page_{page + 1}"))
    buttons.append(InlineKeyboardButton("❌ Завершить", callback_data="cancel_search"))

    markup = InlineKeyboardMarkup([buttons]) if buttons else None

    # Отправка или редактирование сообщения
    if isinstance(update_or_query, CallbackQuery):
        await update_or_query.edit_message_text(text=text, reply_markup=markup, parse_mode="HTML")
        await update_or_query.edit_message_media(media=photos)
    else:
        await update_or_query.message.reply_text(text=text, reply_markup=markup, parse_mode="HTML")

    return len(results)
