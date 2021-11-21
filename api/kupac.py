import flask_restful
import flask
import model
import errors
from utils.api_helpers import general, kupac_helper
import decorators
from core import db

from schemas import (
    KupacEditSchema,
    KupacCreateSchema,
    KupacSearchSchema
)


class KupacResource(flask_restful.Resource):
    """
    This class will provide api calls for managing basic kupac data.
    """
    path = ['/kupac/<kupac_id>',
            '/kupac']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, kupac_id):
        """
        Get method on this api call returns kupac for given id.
        :param current_user:
        :param kupac_id:
        :return:
        """

        return general.get_object_by_id(
            obj_id=kupac_id,
            query_model=model.Kupac,
            error=errors.ERR_BAD_KUPAC_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def patch(current_user, kupac_id):
        """
        Patch method on this api call should be used for editing kupac data for
        given kupac id.
        :param current_user:
        :param kupac_id:
        :return:
        """

        return kupac_helper.edit_kupac(
            data=KupacEditSchema().check_and_abort(flask.request.json or {}),
            pkupac_id=kupac_id,
            query_model=model.Kupac,
            error=errors.ERR_BAD_KUPAC_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def delete(current_user, kupac_id):
        """
        Delete method on this api call should be used for deleting kupac data for given kupac id.
        :param current_user:
        :param kupac_id:
        :return:
        """

        return kupac_helper.delete_kupac(
            pkupac=kupac_id,
            query_model=model.Kupac,
            error=errors.ERR_BAD_KUPAC_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def post(current_user):
        """
        Post method on this api call should be used for creating kupac data for given params.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = KupacCreateSchema().check_and_abort(flask.request.json or {})

        # add kupac in db
        kupac = model.Kupac.create(**validated_data)
        db.session.add(kupac)
        db.session.flush()

        return kupac


class SearchKupacResource(flask_restful.Resource):
    """
    This resource should be used for getting all kupac or searching kupac.
    """
    path = ['/kupci']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user):
        """
        Get method on this api call should be used for getting and searching kupac.
        Users can filter and sort by all fields and search by first_name and last_name field.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        kwargs = KupacSearchSchema().check_and_abort(flask.request.args or {})

        # Search data
        kupac_count, kupac = model.Kupac.search_kupac(**kwargs)

        return {'kupac_count': kupac_count, 'kupac': kupac}
