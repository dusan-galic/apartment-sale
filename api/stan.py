import flask_restful
import flask
import model
import errors
from utils.api_helpers import general, stan_helper
import decorators
from core import db

from schemas import (
    StanSchema,
    StanCreateSchema,
    StanSearchSchema
)


class StanResource(flask_restful.Resource):
    """
    This class will provide api calls for managing basic apartments data.
    """
    path = ['/stan/<stan_id>',
            '/stan']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, stan_id):
        """
        Get method on this api call returns apartment for given id.
        :param current_user:
        :param stan_id:
        :return:
        """

        return general.get_object_by_id(
            obj_id=stan_id,
            query_model=model.Stan,
            error=errors.ERR_BAD_STAN_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    @decorators.check_user_roles(model.User.ADMINISTRATOR)
    def patch(current_user, stan_id):
        """
        Patch method on this api call should be used for editing apartment data for given apartment id.
        Only users with administrator role can edit data.
        :param current_user:
        :param stan_id:
        :return:
        """

        return stan_helper.edit_stan(
            data=StanSchema().check_and_abort(flask.request.json or {}),
            stan_id=stan_id,
            query_model=model.Stan,
            error=errors.ERR_BAD_STAN_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    @decorators.check_user_roles(model.User.ADMINISTRATOR)
    def delete(current_user, stan_id):
        """
        Delete method on this api call should be used for deleting apartment data for given apartment id.
        Only users with administrator role can edit data.
        :param current_user:
        :param stan_id:
        :return:
        """

        return stan_helper.delete_stan(
            stan_id=stan_id,
            query_model=model.Stan,
            error=errors.ERR_BAD_STAN_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    @decorators.check_user_roles(model.User.ADMINISTRATOR)
    def post(current_user):
        """
        Post method on this api call should be used for creating apartment data for given params.
        Only users with administrator role can edit data.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = StanCreateSchema().check_and_abort(flask.request.json or {})

        # add current user id
        validated_data['user_id'] = current_user.id

        # add stan in db
        stan = model.Stan.create(**validated_data)
        db.session.add(stan)
        db.session.flush()

        return stan


class FilterStanResource(flask_restful.Resource):
    """
    This resource should be used for getting all apartments or filtering apartments.
    """
    path = ['/stanovi']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user):
        """
        Get method on this api call should be used for getting apartments.
        Apartments can filter and sort by all fields.
        :param current_user:
        :return:
        """
        kwargs = StanSearchSchema().check_and_abort(flask.request.args or {})

        stan_count, stan = model.Stan.filter_stan(**kwargs)

        return {'stan_count': stan_count, 'stan': stan}
