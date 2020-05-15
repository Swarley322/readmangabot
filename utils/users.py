from crud import session
from models import Subscribers

s = session()


def add_manga_to_users_tracking_list(user_id, manga_id):
    """Function returns False if manga is already tracking
       or adds manga_id in users tracking_list and returns True"""
    user = s.query(Subscribers).filter_by(user_id=user_id).first()
    if user.tracking_list is not None and manga_id in user.tracking_list:
        s.close()
        return False
    elif user.tracking_list is None:
        user.tracking_list = [manga_id]
        s.commit()
        s.close()
        return True
    else:
        user.tracking_list = user.tracking_list + [manga_id]
        s.commit()
        s.close()
        return True


def toogle_subscription(user_id):
    user = s.query(Subscribers).filter_by(user_id=user_id).first()
    if not user.active:
        user.active = True
    else:
        user.active = False
    s.commit()
    s.close()


def get_or_create_subscriber(effective_user, message):
    subscriber = s.query(Subscribers).filter_by(user_id=effective_user.id).first()
    if not subscriber:
        subscriber = Subscribers(
            username=effective_user.username,
            user_id=effective_user.id,
            chat_id=message.chat.id,
            tracking_list=[],
            active=False
        )
        s.add(subscriber)
        s.commit()
    s.close()
    return subscriber


def get_users_tracking_manga(user_id):
    user = s.query(Subscribers).filter_by(user_id=user_id).first()
    s.close()
    return user.tracking_list


def check_manga_in_users_tacking_list(user_id, manga_id):
    """returns True if manga_id in users tracking_list else returns False

       user_id - integer
       manga_id - integer"""
    users_tracking_manga = get_users_tracking_manga(user_id)
    if users_tracking_manga is not None and manga_id in users_tracking_manga:
        return True
    else:
        return False


def delete_manga_from_tracking_list(user_id, manga_id):
    user = s.query(Subscribers).filter_by(user_id=user_id).first()
    new_tracking_list = user.tracking_list[:]
    new_tracking_list.remove(manga_id)
    user.tracking_list = new_tracking_list
    s.commit()
    s.close()