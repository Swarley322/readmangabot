import logging
import os
import pprint


from telegram import error, InlineKeyboardButton, InlineKeyboardMarkup,\
                     ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils.manga import search_manga_titles, check_manga_in_tracking, \
                        insert_manga_in_tracking, get_manga_title, \
                        get_manga_chapters_value
from utils.users import get_or_create_subscriber, toogle_subscription, \
                        get_users_tracking_manga, add_manga_to_users_tracking_list
from utils.utils import get_keyboard

pp = pprint.PrettyPrinter(indent=4)


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
        update.message.reply_text("Try again or press /cancel if you want to leave conversation")
        return "search"
    else:
        text = ""
        for manga in mangas:
            text += f"{manga['title']}\n/track_{manga['id']}\n\n"
        update.message.reply_text(text)
        update.message.reply_text("for leaving conversation press /cancel")
        return "track"


def manga_track(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    try:
        manga_id = int(update.message.text.replace('/track_', ''))
        update.message.reply_text("downloading...")
        manga_title = get_manga_title(manga_id)
        manga_exists = add_manga_to_users_tracking_list(user.user_id, manga_id)
        if manga_exists:
            update.message.reply_text(f"{manga_title} added in your tracking list")
        else:
            update.message.reply_text(f"{manga_title} is already in your tracikng list")
        if not check_manga_in_tracking(manga_id):
            insert_manga_in_tracking(manga_id)
        text = "If you want to add once more manga press /add_more or /cancel for quit"
        update.message.reply_text(text)
        return "add_more"
    except ValueError:
        update.message.reply_text("don't do this again")
        return ConversationHandler.END


def manga_add_more(update, context):
    return "choose"


def manga_leave_conversation(update, context):
    update.message.reply_text("See you later")
    return ConversationHandler.END


def dontknow(update, context):
    update.message.reply_text("Don't understand you, press /cancel for leaving conversation")


def get_tracking_manga(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    if user.active:
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
    else:
        update.message.reply_text("You haven't subscribed, press /subscribe for subscribing")
