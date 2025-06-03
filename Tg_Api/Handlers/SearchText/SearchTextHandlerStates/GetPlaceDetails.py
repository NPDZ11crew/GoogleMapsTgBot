import os

from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes, CallbackContext
import re
from GoogleMapsApi import getDetails


# def extract_photo_reference(url):
#     m = re.search(r'3m2!1s([^!]+)!2e10', url)
#     if m:
#         print(m.group(1))
#         return m.group(1)
#     return None


async def getPlaceDetails(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    id = update.callback_query.data[3:]
    data = await getDetails(id)
    await update.callback_query.answer("Wait for few seconds!")

    # print("Photo URLs:")
    # for url in data["photos"]:
    #     print(url)
    temp = [i.split(':') for i in data['weekdayDescriptions']]
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    cnt = 0
    for i in temp:
        i[0] = days[cnt]
        cnt += 1
    weekdayDescriptions = [":".join(i) for i in temp]

    schedule = '\n'.join(weekdayDescriptions)

    message = f"Назва закладу: {data['displayName']}\n" \
              f"Рейтинг: {data['rating']}\n" \
              f"Кількість оцінок: {data['userRatingsCount']}\n" \
              f"Адреса: {data['formattedAddress']}\n" \
              f"Години роботи:\n{schedule}\n" \

    # пока так, потом поменять прием фото
    photos = []
    for url in data["photos"]:
        photo_ref = url.split('/')[-1]
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_ref}&key={os.getenv('googleApiKey')}"
        photos.append(InputMediaPhoto(photo_url))

    # for i, media in enumerate(photos):
    #     print(f"InputMediaPhoto {i}: {media.media}")

    await context.bot.send_media_group(chat_id=update.effective_chat.id,
                                         media=photos,
                                         caption=message)
