from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters
from Tg_Api.Handlers.SearchNearby.SearchNearbyHandlerStates import *

(
    LOCATION,
    HANDLE_CITY,
    PLACE_TYPE,
    SUBTYPE,
    RADIUS,
    SHOW_RESULTS,
) = range(6)

nearbySearchHandler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOCATION: [MessageHandler(filters.TEXT | filters.LOCATION, handle_location)],
        HANDLE_CITY: [MessageHandler(filters.TEXT, sendPrompt)],
        PLACE_TYPE: [
            CallbackQueryHandler(handle_category_selection, pattern=r"^(cat_|page_|done_selecting)"),
        ],
        SUBTYPE: [CallbackQueryHandler(handle_subtype)],
        RADIUS: [MessageHandler(filters.TEXT & filters.Regex(r'^\d+$'), handle_radius)],
        SHOW_RESULTS: [CallbackQueryHandler(handle_pagination, pattern=r'^page_\d+$')],
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        CallbackQueryHandler(cancel, pattern="^cancel_search$")
    ],
)
