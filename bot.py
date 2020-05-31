import datetime
import logging
from db.models import Base
from db.base import engine

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, \
                         ConversationHandler, MessageHandler, Filters

from config import API_KEY, PROXY_PASSWORD, PROXY_URL, PROXY_USERNAME
from utils.handlers import delete_readmanga_start, delete_readmanga_choose, \
                           dontknow, \
                           get_subscribed_manga_ids, get_subscribed_readmanga, \
                           greet_user, \
                           inline_button_pressed, \
                           leave_conversation, \
                           manga_choose, mintmanga_search, \
                           readmanga_search, \
                           readmanga_track, \
                           send_updated_manga, get_last_readmanga_chapter, \
                           talk_to_me, subscribe, unsubscribe

# from utils.periodic_tasks import erase_new_chapters, update_all_active_mangas

logging.basicConfig(filename="bot.log", level=logging.INFO)
PROXY = {"proxy_url": PROXY_URL,
         "urllib3_proxy_kwargs": {
                    "username": PROXY_USERNAME,
                    "password": PROXY_PASSWORD
                    }}


def main():
    mybot = Updater(API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    # mybot.job_queue.run_daily(erase_new_chapters, time=datetime.time(22, 0, 0, 0))
    # mybot.job_queue.run_daily(update_all_active_mangas, time=datetime.time(22, 3, 0, 0))
    # mybot.job_queue.run_daily(send_updated_manga, time=datetime.time(22, 3, 0, 0))

    choose_form = ConversationHandler(
        entry_points=[CommandHandler("choose_manga", manga_choose)],
        states={
            "choose_provider": [
                CallbackQueryHandler(inline_button_pressed)
            ],
            "search_readmanga": [
                CommandHandler('cancel', leave_conversation),
                MessageHandler(Filters.text, readmanga_search)
            ],
            "search_mintmanga": [
                CommandHandler('cancel', leave_conversation),
                MessageHandler(Filters.text, mintmanga_search)
            ],
            "readmanga_track": [
                CommandHandler('cancel', leave_conversation),
                CommandHandler('try_again', manga_choose),
                MessageHandler(Filters.regex(r'/track_\d{1,}'), readmanga_track)
            ],
            "mintmanga_track": [
                CommandHandler('cancel', leave_conversation),
                CommandHandler('try_again', manga_choose),
                MessageHandler(Filters.regex(r'/track_\d{1,}'), readmanga_track)
            ],
            'add_more': [
                CommandHandler("add_more", manga_choose),
                CommandHandler("cancel", leave_conversation)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, dontknow)]
    )

    delete_form = ConversationHandler(
        entry_points=[CommandHandler("delete_manga", delete_readmanga_start)],
        states={
            "choose": [CommandHandler('cancel', leave_conversation)],
            "delete": [
                CommandHandler('cancel', leave_conversation),
                MessageHandler(Filters.regex(r'/delete_\d{1,}'), delete_readmanga_choose)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, dontknow)]
    )

    dp.add_handler(choose_form)
    dp.add_handler(delete_form)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("tracking_manga", get_subscribed_readmanga))
    dp.add_handler(MessageHandler(Filters.regex(r'/last_chapter_\d{1,}'), get_last_readmanga_chapter))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot has been started")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
