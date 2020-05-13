import logging
import re

from telegram.ext import Updater, CallbackQueryHandler, CommandHandler,\
                         ConversationHandler, MessageHandler, Filters

from config import API_KEY, PROXY_PASSWORD, PROXY_URL, PROXY_USERNAME
from utils.handlers import greet_user, talk_to_me, subscribe, unsubscribe, \
                           get_tracking_manga, manga_choose, manga_search, \
                           manga_track, dontknow, manga_leave_conversation

logging.basicConfig(filename="bot.log", level=logging.INFO)
PROXY = {"proxy_url": PROXY_URL,
         "urllib3_proxy_kwargs": {"username": PROXY_USERNAME, "password": PROXY_PASSWORD}}


def main():
    mybot = Updater(API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    choose_form = ConversationHandler(
        entry_points=[CommandHandler("choose_manga", manga_choose)],
        states={
            "search": [
                CommandHandler('cancel', manga_leave_conversation),
                MessageHandler(Filters.text, manga_search)
            ],
            "track": [
                CommandHandler('cancel', manga_leave_conversation),
                MessageHandler(Filters.regex(r'/track_\d{1,}'), manga_track)
            ],
            'add_more': [
                CommandHandler("add_more", manga_choose),
                CommandHandler("cancel", manga_leave_conversation)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, dontknow)]
    )

    dp.add_handler(choose_form)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("tracking_manga", get_tracking_manga))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot has been started")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
