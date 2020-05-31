import logging
# import pprint

from telegram import error, InlineKeyboardButton, InlineKeyboardMarkup,\
                     ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils.manga import delete_manga, get_manga_title, \
                        get_manga_chapters, get_manga_chapters_value, \
                        search_manga_titles, update_manga
from utils.users import get_or_create_subscriber, toogle_subscription, \
                        get_subscribed_manga_ids, \
                        is_subscribed_to_manga, \
                        subscribe_to_manga, \
                        unsubscribe_from_manga, \
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
        inlinekeyboard = [[
                InlineKeyboardButton("Mintmanga", callback_data='mintmanga'),
                InlineKeyboardButton("Readmanga", callback_data='readmanga'),
                InlineKeyboardButton("Cancel", callback_data='cancel')
        ]]
        kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
        update.message.reply_text("Choose provider", reply_markup=kbd_markup)
        return "choose_provider"
    else:
        update.message.reply_text("You haven't subscribed, press /subscribe for subscribing")
        return ConversationHandler.END


def inline_button_pressed(update, context):
    query = update.callback_query
    text = "Enter any manga title or press /cancel"
    if query.data == "mintmanga":
        context.bot.edit_message_text(
                    text=text,
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id
        )
        print('mintmanga')
        return "search_mintmanga"
    elif query.data == "readmanga":
        context.bot.edit_message_text(
                    text=text,
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id
        )
        return "search_readmanga"
    elif query.data == "cancel":
        context.bot.edit_message_text(
                    text="Goode bye",
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id
        )
        return ConversationHandler.END


def readmanga_search(update, context):
    user_message = update.message.text.strip()
    if len(user_message) <= 3 or user_message.count(" ") >= 4:
        update.message.reply_text("dont'understand you try again or press /cancel")
        return "search_readmanga"
    mangas = search_manga_titles('readmanga', user_message)
    if not mangas:
        update.message.reply_text("Couldn't find any manga, try again or press /cancel if you want to leave conversation")
        return "search_readmanga"
    else:
        text = ""
        for manga in mangas:
            text += f"{manga['title']}\n/track_{manga['id']}\n\n"
            if len(text) > 4000:
                update.message.reply_text(text)
                update.message.reply_text("Press /try_again or press /cancel if you want to leave conversation")
                return "readmanga_track"
        update.message.reply_text(text)
        update.message.reply_text("Press /try_again or press /cancel if you want to leave conversation")
        return "readmanga_track"


def mintmanga_search(update, context):
    user_message = update.message.text.strip()
    if len(user_message) <= 3 or user_message.count(" ") >= 4:
        update.message.reply_text("dont'understand you tyr again or press /cancel")
        return "search_mintmanga"
    mangas = search_manga_titles('mintmanga', user_message)
    if not mangas:
        update.message.reply_text("Couldn't find any manga, try again or press /cancel if you want to leave conversation")
        return "search_mintmanga"
    else:
        text = ""
        for manga in mangas:
            text += f"{manga['title']}\n/track_{manga['id']}\n\n"
            if len(text) > 4000:
                update.message.reply_text(text)
                update.message.reply_text("Press /try_again or press /cancel if you want to leave conversation")
                return "mintmanga_track"
        update.message.reply_text(text)
        update.message.reply_text("Press /try_again or press /cancel if you want to leave conversation")
        return "mintmanga_track"


def readmanga_track(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    try:
        manga_id = int(update.message.text.replace('/track_', ''))
        manga_title = get_manga_title('readmanga', manga_id)
        text = "If you want to add once more manga press /add_more or /cancel for quit"
        if is_subscribed_to_manga('readmanga', user.user_id, manga_id):
            update.message.reply_text(f"{manga_title} is already in your tracikng list")
            update.message.reply_text(text)
            return "add_more"
        else:
            update.message.reply_text("adding...")
            update = update_manga('readmanga', manga_id)
            if not update:
                update.message.reply_text("no chapters in manga")
                delete_manga('readmanga', manga_id)
                update.message.reply_text(text)
                return "add_more"
            subscribe_to_manga('readmanga', user.user_id, manga_id)
            update.message.reply_text(f"{manga_title} added in your tracking list")
            update.message.reply_text(text)
            return "add_more"
    except ValueError:
        update.message.reply_text("don't do this again")
        return ConversationHandler.END


def mintmanga_track(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    try:
        manga_id = int(update.message.text.replace('/track_', ''))
        manga_title = get_manga_title('mintmanga', manga_id)
        text = "If you want to add once more manga press /add_more or /cancel for quit"
        if is_subscribed_to_manga('mintmanga', user.user_id, manga_id):
            update.message.reply_text(f"{manga_title} is already in your tracikng list")
            update.message.reply_text(text)
            return "add_more"
        else:
            update.message.reply_text("adding...")
            update = update_manga('mintmanga', manga_id)
            if not update:
                update.message.reply_text("no chapters in manga")
                delete_manga('mintmanga', manga_id)
                update.message.reply_text(text)
                return "add_more"
            subscribe_to_manga('mintmanga', user.user_id, manga_id)
            update.message.reply_text(f"{manga_title} added in your tracking list")
            update.message.reply_text(text)
            return "add_more"
    except ValueError:
        update.message.reply_text("don't do this again")
        return ConversationHandler.END


def manga_add_more(update, context):
    return "choose_manga"


def leave_conversation(update, context):
    update.message.reply_text("See you later")
    return ConversationHandler.END


def dontknow(update, context):
    update.message.reply_text("Don't understand you, press /cancel for leaving conversation")


#refactor
def get_subscribed_readmanga(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    tracking_manga = get_subscribed_manga_ids('readmanga', user.user_id)
    if tracking_manga is not None:
        text = "Your manga:\n"
        for manga_id in tracking_manga:
            text += f"""
Title: {get_manga_title(manga_id)}
Chapters: {get_manga_chapters_value(manga_id)}
/last_chapter_{manga_id}
"""
        update.message.reply_text(text)
    else:
        update.message.reply_text("you don't have any manga in your tracking list")


def delete_readmanga_start(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    tracking_manga = get_subscribed_manga_ids('readmanga', user.user_id)
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


def delete_readmanga_choose(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    try:
        manga_id = int(update.message.text.replace('/delete_', ''))
        manga_exist = is_subscribed_to_manga(user.user_id, manga_id)
        if manga_exist:
            unsubscribe_from_manga('readmanga', user.user_id, manga_id)
            manga_title = get_manga_title('readmanga', manga_id)
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


def get_last_readmanga_chapter(update, context):
    user = get_or_create_subscriber(update.effective_user, update.message)
    manga_id = int(update.message.text.replace('/last_chapter_', ''))
    if is_subscribed_to_manga('readmanga', user.user_id, manga_id):
        chapters = get_manga_chapters(manga_id)
        text = f'title: {chapters[0]["chapter_name"]}\nurl: {chapters[0]["chapter_url"]}'
        update.message.reply_text(text)
    else:
        update.message.reply_text("don't do this again")