from telegram import ReplyKeyboardMarkup


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
                                        ['/start', '/subscribe', '/unsubscribe'],
                                        ['/tracking_manga'],
                                        ['/choose_manga', '/delete_manga']
                                       ], resize_keyboard=True
                                      )
    return my_keyboard
