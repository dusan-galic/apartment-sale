from core import socketio, redis_store
from flask_socketio import send, emit, join_room, ConnectionRefusedError
import json
import decorators


@socketio.on("connect")
@decorators.auth_decorator
def on_connect(current_user):
    """
    This method is used for connecting users on web socket. Only users with role "finansije" can connect.
    :param current_user:
    :return:
    """
    # current user can connected if has role "finansije"
    if current_user.get('role', '') == 'finansije':
        # set user data to redis
        value = {
            "id": f'{current_user.get("id")}',
            "room": f'user_{current_user.get("id")}'
        }
        redis_store.hset("notification-f", key=f'user_s_{current_user.get("id")}', value=json.dumps(value))
        user_room = f'user_{current_user.get("id")}'
        # add user to group
        join_room(user_room)
        # send signal
        send(f'connect to room {user_room}')
    else:
        send(f'user can not connect to room')
        raise ConnectionRefusedError('unauthorized!')


@socketio.on("disconnect")
@decorators.auth_decorator
def on_disconnect(current_user):
    """
    This method is used for disconnecting users
    :param current_user:
    :return:
    """
    # delete user from redis
    redis_store.hdel("notification-f", f'user_s_{current_user.get("id")}')


@socketio.on('message')
@decorators.auth_decorator
def handle_message(current_user, message):
    """

    :param current_user:
    :param message:
    :return:
    """
    send(message, broadcast=True)


@socketio.on('notification-f')
def ps_notification_f(pkupac, kupac):
    """
    This method is used for sending signal for users with role "finansije"
    :param data:
    :return:
    """
    pkupac_data = {
        "id": pkupac.id,
        "stan_id": pkupac.stan_id,
        "kupac_id": pkupac.kupac_id,
        "cena_za_kupca": pkupac.cena_za_kupca,
        "napomena": pkupac.napomena,
        "status": pkupac.status,
        "first_name": kupac.first_name,
        "last_name": kupac.last_name
    }
    emit('notification-f', pkupac_data, broadcast=True, namespace='/')
