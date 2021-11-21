import functools
import jsonpickle
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from core import db, redis_store
import flask_restful
import flask
from flask import request
import model
import json
from flask_socketio import ConnectionRefusedError

import errors


def obj_to_json(obj):
    return jsonpickle.encode(obj, max_depth=6, unpicklable=False)


def to_json(func):
    """
    Decorator for transforming result of a function to JSON dictionary
    """
    @functools.wraps(func)
    def decorated(*args, **kwargs):

        res = func(*args, **kwargs)
        # res can be tuple when status code is returned with response
        # return error, 404
        if type(res) == tuple:
            return obj_to_json(res[0]), res[1]
        return obj_to_json(res)

    return decorated


def flask_sqlalchemy_session_decorator(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if "ERR_" in res or (type(res) == tuple and res[1] >= 400):
                db.session.rollback()
                return res
            db.session.commit()
            return res
        except SQLAlchemyError as e:
            try:
                db.session.rollback()
            except Exception as e:
                print("ROLLBACK EXCEPTION: {}".format(e))
            db.session.close()
            if "orig" in e.__dict__:
                msg = getattr(e, "orig")
            elif "msg" in e.__dict__:
                msg = getattr(e, "msg")
            else:
                msg = e
            if type(e) == IntegrityError:
                if "duplicate key" in str(getattr(e, "orig")):
                    return jsonpickle.encode({"error": "ERR_DUPLICATE_ENTRY"}), 400
            return jsonpickle.encode({"error": "{}".format(msg)}, unpicklable=False), 400

    return decorated


def check_user_roles(*permissions, exclude=False):
    """
    This decorator checks the user role.
    :param permissions:
    :param exclude:
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def _decorated(*args, **kwargs):
            try:
                role = flask.g.current_user.get("role")
            except Exception as e:
                flask_restful.abort(403, error=errors.ERR_BAD_USER_ID)
            else:
                if not exclude and role not in permissions:
                    flask_restful.abort(403, error=errors.ERR_FORBIDDEN_FOR_ROLE)
                if exclude and role in permissions:
                    flask_restful.abort(403, error=errors.ERR_FORBIDDEN_FOR_ROLE)
                return func(*args, **kwargs)
        return _decorated
    return decorator


def get_user_and_check_user_validity(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        This decorator is getting current_user and checking if user is not deleted, in
        case user is valid then send current_user to decorated function.
        :param args:
        :param kwargs:
        :return:
        """
        from utils.api_helpers import general
        # Get logged in user
        current_user = general.get_object_by_id(
            obj_id=flask.g.current_user['id'],
            query_model=model.User,
            error=errors.ERR_BAD_USER_ID
        )

        # Check if current user is not deleted
        if current_user:
            current_user.check_if_user_not_deleted()
            return func(current_user=current_user, *args, **kwargs)
        else:
            flask_restful.abort(400, error=errors.ERR_BAD_USER_ID)
    return wrapper


def auth_decorator(func):
    """
    This decorator is used to check user authorization for websocket.
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sess_id = request.headers.get('session_id')
        if not sess_id:
            raise ConnectionRefusedError('missed session id!')
        else:
            user = redis_store.get(sess_id)
            if not user:
                raise ConnectionRefusedError('session is not valid!')
        user = json.loads(user.decode("utf-8"))
        current_user = user
        return func(current_user=current_user, *args, **kwargs)

    return wrapper
