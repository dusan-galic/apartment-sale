"""Flask configuration."""

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://fww:fww2020@localhost/prodaja_stanova?charset=utf8mb4&use_unicode=1"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

SOCKETIO_MESSAGE_QUEUE = "redis://localhost:6379/5"
REDIS_SOCKETIO_NAME = '5'
SOCKETIO_DEBUG = True

API_URL = "http://0.0.0.0:7777"
