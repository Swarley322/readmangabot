from db.base import s
from db.models import User, Readmanga, Mintmanga


def get_user(user_id):
    user = s.query(User).filter_by(user_id=user_id).first()
    return user


def subscribe_to_manga(manga_site, user_id, manga_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    user_id - telegram user_id from effective_user
    manga_id - integer
    adding readmanga/mintmanga to user supscriptions
    """
    user = get_user(user_id)
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
        user.readmanga.append(manga)
    elif manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()
        user.mintmanga.append(manga)
    s.commit()


def unsubscribe_from_manga(manga_site, user_id, manga_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    user_id - telegram user_id from effective_user
    returns list with readmanga/mintmanga ids
    """
    user = get_user(user_id)
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
        user.readmanga.remove(manga)
    elif manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()
        user.mintmanga.remove(manga)
    s.commit()


def toogle_subscription(user_id):
    user = s.query(User).filter_by(user_id=user_id).first()
    if not user.active:
        user.active = True
    else:
        user.active = False
    s.commit()


def get_or_create_subscriber(effective_user, message):
    subscriber = s.query(User).filter_by(user_id=effective_user.id).first()
    if not subscriber:
        subscriber = User(
            username=effective_user.username,
            user_id=effective_user.id,
            chat_id=message.chat.id,
            active=False
        )
        s.add(subscriber)
        s.commit()
    return subscriber


def get_subscribed_manga_ids(manga_site, user_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    user_id - telegram user_id from effective_user
    returns list with readmanga/mintmanga ids
    """
    user = get_user(user_id)
    if manga_site == "readmanga":
        subscriptions = []
        for manga in user.readmanga:
            subscriptions.append(manga.id)
    elif manga_site == "mintmanga":
        subscriptions = []
        for manga in user.mintmanga:
            subscriptions.append(manga.id)
    return subscriptions


def is_subscribed_to_manga(manga_site, user_id, manga_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    user_id - telegram user_id from effective_user
    manga_id - integer
    returns True if user subscribed on manga else False
    """
    subscriptions = get_subscribed_manga_ids(manga_site, user_id)
    if manga_id in subscriptions:
        return True
    return False


def get_all_active_users():
    users_list = s.query(User).filter_by(active=True).all()
    return users_list



# NEED TO REFACTOR
def get_all_updated_user_manga(user_id):
    user = s.query(User).filter_by(user_id=user_id).first()
    updated_manga = []
    for manga_id in user.tracking_list:
        manga = s.query(Tracking).filter_by(manga_id=manga_id).first()
        if manga.new_chapters:
            updated_manga.append({
                "manga_title": get_manga_title(manga_id),
                "last_chapter": manga.chapters[0]
            })
    if len(updated_manga) > 0:
        text = f"""New chapters available:\n"""
        for manga in updated_manga:
            text += f"""
Title: {manga["manga_title"]}
Chapter: {manga["last_chapter"]["chapter_name"]}
URL: {manga["last_chapter"]["chapter_url"]}
            """
        return text
    return False
