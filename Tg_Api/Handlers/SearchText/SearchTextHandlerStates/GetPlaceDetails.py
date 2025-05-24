from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes, CallbackContext

from GoogleMapsApi import getDetails


async def getPlaceDetails(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    data = await getDetails(id=update.callback_query.data[3:])
    await update.callback_query.answer("Wait for few seconds!")
    message = f"Name: {data['displayName']} - rating: {data['rating']}\n" \
              f"Ratings count: {data['userRatingsCount']}\n" \
              f"Address: {data['formattedAddress']}\n" \
              f"Open hours: {data['weekdayDescriptions']}\n" \

    # пока так, потом поменять прием фото
    photos = [InputMediaPhoto(i) for i in data["photos"]]
    await context.bot.send_media_group(chat_id=update.effective_chat.id,
                                         media=photos,
                                         caption=message)
