from flask import request
import os
import core
from core import db

from flask_restful import Api

from core.modules import get_module_list, create_routes


module_names = []

pkgpath = os.path.join(os.path.dirname(__file__), "api")

module_names = get_module_list(pkgpath, "api", module_names)

routes = create_routes(module_names)

api = Api()


def create_flask_app():
    app = core.create_app(
        routes,
        name=__name__
    )

    @app.after_request
    def after_request(response):
        if request.method != 'GET':
            db.session.commit()

        return response
    return app
