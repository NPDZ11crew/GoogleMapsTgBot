from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from .SearchTextHandlerStates import *

SEARCH_TEXT, GET_DETAILS = range(2)


searchTextConvHandler = ConversationHandler(
        entry_points=[CommandHandler("searchText", startSearchByText)],
        states={
                SEARCH_TEXT: [MessageHandler(filters.TEXT,callback=searchByText)],
                GET_DETAILS: [CallbackQueryHandler(getPlaceDetails, pattern=r"^id:.*")]
                },
        fallbacks=[CommandHandler("end", end)]
    )
