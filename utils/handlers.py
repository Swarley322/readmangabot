import logging
# import pprint


from telegram import error, InlineKeyboardButton, InlineKeyboardMarkup,\
                     ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils.manga import search_manga_titles, check_manga_in_tracking, \
                        add_manga_in_tracking, get_manga_title, \
                        get_manga_chapters_value, update_manga_in_tracking
from utils.users import get_or_create_subscriber, toogle_subscription, \
                        get_users_tracking_manga, add_manga_to_users_tracking_list, \
                        delete_manga_from_tracking_list, check_manga_in_users_tacking_list, \
                        get_all_active_users, get_all_updated_user_manga
from utils.utils import get_keyboard

# pp = pprint.PrettyPrinter(indent=4)


def greet_user(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    text = f"Hello {user.user_id}"
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    text = "Hello {}, you said {}".format(
                                user.user_id,
                                update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s",
                 user.user_id,
                 user.chat_id,
                 update.message.text
                 )
    update.message.reply_text(text, reply_markup=get_keyboard())


def subscribe(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    if not user.active:
        toogle_subscription(user.user_id)
        update.message.reply_text("You have subscribed")
    else:
        update.message.reply_text("You have already subscribed")


def unsubscribe(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    if user.active:
        toogle_subscription(user.user_id)
        update.message.reply_text("You have unsubscribed")
    else:
        update.message.reply_text("You haven't subscribed, press /subscribe for subscribing")


def manga_choose(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    if user.active:
        update.message.reply_text("please enter any manga title or press /cancel if you want to leave conversation")
        return "search"
    else:
        update.message.reply_text("You haven't subscribed, press /subscribe for subscribing")
        return ConversationHandler.END


def manga_search(update, context):
    mangas = search_manga_titles(update.message.text)
    if not mangas:
        update.message.reply_text(" Coudn't find any manga, press /try_again or press /cancel if you want to leave conversation")
        return "search"
    else:
        text = ""
        for manga in mangas:
            text += f"{manga['title']}\n/track_{manga['id']}\n\n"
        update.message.reply_text(text)
        update.message.reply_text("Press /try_again or press /cancel if you want to leave conversation")
        return "track"


def manga_track(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    try:
        manga_id = int(update.message.text.replace('/track_', ''))
        manga_title = get_manga_title(manga_id)
        manga_exists = add_manga_to_users_tracking_list(user.user_id, manga_id)
        if manga_exists:
            update.message.reply_text(f"{manga_title} added in your tracking list")
        else:
            update.message.reply_text(f"{manga_title} is already in your tracikng list")
        manga_exist = check_manga_in_tracking(manga_id)
        if not manga_exist:
            update.message.reply_text("downloading...")
            add_manga_in_tracking(manga_id)
        elif manga_exist == "not up to date":
            update.message.reply_text("downloading...")
            update_manga_in_tracking(manga_id)
        text = "If you want to add once more manga press /add_more or /cancel for quit"
        update.message.reply_text(text)
        return "add_more"
    except ValueError:
        update.message.reply_text("don't do this again")
        return ConversationHandler.END


def manga_add_more(update, context):
    return "choose"


def leave_conversation(update, context):
    update.message.reply_text("See you later")
    return ConversationHandler.END


def dontknow(update, context):
    update.message.reply_text("Don't understand you, press /cancel for leaving conversation")


def get_tracking_manga(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    tracking_manga = get_users_tracking_manga(user.user_id)
    if tracking_manga is not None:
        text = "Your manga:\n"
        for manga_id in tracking_manga:
            text += f"""
Title: {get_manga_title(manga_id)}
Chapters: {get_manga_chapters_value(manga_id)}
"""
        update.message.reply_text(text)
    else:
        update.message.reply_text("you don't have any manga in your tracking list")


def delete_manga_start(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    tracking_manga = get_users_tracking_manga(user.user_id)
    if tracking_manga is not None:
        text = "Choose manga:\n"
        for manga_id in tracking_manga:
            text += f"""
Title: {get_manga_title(manga_id)}
/delete_{manga_id}
"""
        update.message.reply_text(text)
        update.message.reply_text("press /cancel for leaving conversation")
        return "delete"
    else:
        update.message.reply_text("you don't have tracking manga")
        return ConversationHandler.END


def delete_manga_choose(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    try:
        manga_id = int(update.message.text.replace('/delete_', ''))
        manga_exist = check_manga_in_users_tacking_list(user.user_id, manga_id)
        if manga_exist:
            delete_manga_from_tracking_list(user.user_id, manga_id)
            manga_title = get_manga_title(manga_id)
            update.message.reply_text(f"{manga_title} deleted from your tracking list")
        else:
            update.message.reply_text("don't do this again")
    except ValueError:
        update.message.reply_text("don't do this again")
    finally:
        return ConversationHandler.END


def send_updated_manga(context):
    all_active_users = get_all_active_users()
    # print(all_active_users)
    if all_active_users is not None:
        for user in all_active_users:
            try:
                text = get_all_updated_user_manga(user.user_id)
                if text:
                    context.bot.send_message(chat_id=user.chat_id, text=text)
                else:
                    text = "No new Manga"
                    context.bot.send_message(chat_id=user.chat_id, text=text)
            except error.BadRequest:
                print("Chat {} not found".format(user.chat_id))
                toogle_subscription(user.user_id)
