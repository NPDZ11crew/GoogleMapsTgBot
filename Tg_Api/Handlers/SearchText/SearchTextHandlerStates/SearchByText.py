from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from GoogleMapsApi import SearchByTextAsync
from Tg_Api.KeyBoards.InlineKeyboards import CreateDetailsButton


async def searchByText(update: Update, context: ContextTypes.DEFAULT_TYPE, GET_DETAILS=1):
    data = await SearchByTextAsync(update.message.text)
    print(repr(data))
    name = data['displayName']
    if isinstance(name, dict):
        name = name.get('text', '')

    message = f"Name: {name} - rating: {data['rating']}\n" \
              f"Phone number: {data['nationalPhoneNumber']}\n" \
              f"Website: {data['googleMapsUri']}\n"

    detailsMarkup = InlineKeyboardMarkup([CreateDetailsButton(data["id"])])

    await context.bot.send_photo(chat_id=update.message.chat_id,
                                 photo=data["photos"][0]["googleMapsUri"],
                                 caption=message,
                                 reply_markup=detailsMarkup)
    return GET_DETAILS