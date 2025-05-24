from telegram import Update
from telegram.ext import ContextTypes

from Tg_Api.Handlers.SearchNearby.SearchNearbyHandlerStates.ShowResults import show_results


async def handle_radius(update: Update, context: ContextTypes.DEFAULT_TYPE):
    radius_km = update.message.text
    #Сделать адекватное сохранение радиуса и проверку
    context.user_data['radius'] = int(radius_km)

    # Показать первую страницу
    return await show_results(update, context, page=1)