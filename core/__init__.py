from flask import Flask, request, Response, current_app, make_response, g
from flask_restful import Api, Resource
from flask_redis import FlaskRedis
from core.data_cleaner import DataCleaner

import jsonpickle
import json

import os

from flask_socketio import SocketIO

# FlaskSQLAlchemy = None
# if os.environ.get('FLASK_SQLALCHEMY', False):
#     try:
#         from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
#     except ImportError:
#         FlaskSQLAlchemy = None

from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
db = FlaskSQLAlchemy()
redis_store = FlaskRedis()
api = Api()
data_cleaner = DataCleaner()
socketio = SocketIO()


def create_app(restful_routes, name=__name__, test_config=None):

    app = Flask(name)
    app.config['SECRET_KEY'] = 'asasfadcsavsvrqca'
    app.config.from_pyfile('config.py', silent=True)
    if test_config:
        # load the test config if passed in
        app.config.update(test_config)
    else:
        app.config.from_pyfile('config.py')

        socketio.init_app(
            app,
            logger=app.config.get('SOCKETIO_DEBUG', False),
            engineio_logger=app.config.get('SOCKETIO_DEBUG', False),
            cors_allowed_origins="*",
            message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
            channel=app.config.get('REDIS_SOCKETIO_NAME'),
            async_mode='eventlet',
        )

    if db:
        db.init_app(app)

        # needed in order to jsonpickle can pickle SQLAlchemy models
        def __getstate__(self):
            state = self.__dict__.copy()
            cleaner = data_cleaner.get(self.__class__)
            if cleaner:
                [state.pop(field, False) for field in cleaner]
            del state['_sa_instance_state']

            return state

        def __setstate__(self, state):
            self.__dict__.update(state)

        db.Model.__getstate__ = __getstate__
        db.Model.__setstate__ = __setstate__
    else:
        raise ImportError("flask_sqlalchemy missing")

    redis_store.init_app(app)

    @api.representation("application/json")
    def output_json(data, code, headers=None):
        """Makes a Flask response with a JSON encoded body"""
        if type(data) == str:
            resp = make_response(data, code)
        else:
            resp = make_response(jsonpickle.encode(data, unpicklable=False, max_depth=6), code)
        resp.headers.extend(headers or {})
        data_cleaner.reset()
        return resp

    _register_restful_routes(restful_routes)

    api.init_app(app)

    # socketio.init_app(
    #     app,
    #     logger=app.config.get('SOCKETIO_DEBUG', False),
    #     engineio_logger=app.config.get('SOCKETIO_DEBUG', False),
    #     cors_allowed_origins="*",
    #     message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
    #     channel=app.config.get('REDIS_SOCKETIO_NAME'),
    #     async_mode='eventlet',
    # )

    @app.before_request
    def before_request():
        if '/public/' not in request.path:
            sess_id = request.headers.get('session_id')
            if not sess_id:
                return _build_message("MISSING SESSION ID")
            else:
                user = redis_store.get(sess_id)
                if not user:
                    return _build_message("SESSION NOT VALID", status=401)
                g.current_user = json.loads(user.decode("utf-8"))

    return app


def _register_restful_routes(restful_routes):
    for route in restful_routes:
        if isinstance(route, dict):
            if isinstance(route["url"], list):
                api.add_resource(route["view"], *route["url"])
            else:
                api.add_resource(route["view"], route["url"])
        elif isinstance(route, Resource) and getattr(route, "path"):
            if isinstance(getattr(route, "path"), list):
                api.add_resource(route, *getattr(route, "path"))
            else:
                api.add_resource(route, getattr(route, "path"))


def _build_message(message, message_type='error', status=400):
    return Response(jsonpickle.encode({message_type: message}), status, mimetype="application/json")
