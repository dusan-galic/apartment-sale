import hashlib
from datetime import datetime
from core import redis_store
import jsonpickle


def obj_to_json(obj):
    return jsonpickle.encode(obj, max_depth=6, unpicklable=False)


def refresh_user_in_session(user, session_key):
    """
    method refresh user in session.
    :param user:
    :param session_key:
    :return:
    """

    # define data
    redis_data = dict()
    redis_data['id'] = user.id
    redis_data['store_time'] = datetime.utcnow()
    redis_data['role'] = user.role

    # set session to redis
    redis_store.set(session_key, obj_to_json(redis_data))


def generate_and_update_user_session_key(user):
    """
    method update user session for given user
    :param user:
    :return:
    """
    # hash user session key
    user_session_key = hashlib.sha512(
        "{}/{}".format(user.id, datetime.utcnow()).encode("UTF-8")
    ).hexdigest()

    # generate session key
    session_key = "{}:{}:{}".format("session", user.id, user_session_key)
    # refresh user session
    refresh_user_in_session(user=user, session_key=session_key)

    return user, session_key


def delete_user_session_from_redis(user_sessions):
    """
    method delete user session for given session
    :param user_sessions:
    :return:
    """
    # delete all given sessions
    for user_session in user_sessions:
        redis_store.delete(user_session.session_token)
