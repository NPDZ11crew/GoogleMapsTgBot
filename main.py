import logging

import dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
import os
from Tg_Api.Handlers import *

SEARCH_TEXT = 0

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")




if __name__ == '__main__':
    dotenv.load_dotenv()  # загружаем данные,что-то похожее на appsettings.json но в другом формате - файл .env,
                          # Его надо загрузить 1 раз в главном файле программы, чтобы использовать данные из него



    application = ApplicationBuilder().token(os.getenv("tgApiKey")).build()

    application.add_handler(searchTextConvHandler)
    application.add_handler(nearbySearchHandler)
    application.run_polling()
