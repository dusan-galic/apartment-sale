import flask_restful
import flask
import model
import errors
from utils.api_helpers import general, kupac_helper
import decorators
from core import db
from utils.template import populate_template

from events import ps_notification_f

from schemas import (
    PKupacEditSchema,
    PKupacCreateSchema,
    PKupacValidationSchema
)


class PKupacResource(flask_restful.Resource):
    """
    This class will provide api calls for managing basic potencijalnikupac data.
    """
    path = ['/pkupac/<pkupac_id>',
            '/pkupac']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, pkupac_id):
        """
        Get method on this api call returns potencijalnikupac for given id.
        :param current_user:
        :param pkupac_id:
        :return:
        """
        return model.PotencijalniKupac.get_pkupac_by_id(obj_id=pkupac_id)

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def patch(current_user, pkupac_id):
        """
        Patch method on this api call should be used for editing potencijalnikupac data for
        given potencijalnikupac id.
        :param current_user:
        :param pkupac_id:
        :return:
        """
        # Validate schema parameters
        validated_data = PKupacEditSchema().check_and_abort(flask.request.json or {})

        # get pkupac
        pkupac = general.get_object_by_id(
            obj_id=pkupac_id,
            query_model=model.PotencijalniKupac,
            error=errors.ERR_BAD_PKUPAC_ID
        )

        # get stan
        stan = general.get_object_by_id(
            obj_id=pkupac.stan_id,
            query_model=model.Stan,
            error=errors.ERR_BAD_STAN_ID
        )

        # check if stan can change status.
        pkupac_status = validated_data.get("status")
        if pkupac_status:
            kupac_helper.check_status_of_stan(pkupac_status=pkupac_status, stan_status=stan.status)

            # edit status of stan.
            kupac_helper.edit_status_of_stan(stan=stan, status=pkupac.status)

        return kupac_helper.edit_kupac(
            current_user=current_user,
            data=PKupacEditSchema().check_and_abort(flask.request.json or {}),
            pkupac_id=pkupac_id,
            query_model=model.PotencijalniKupac,
            error=errors.ERR_BAD_PKUPAC_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def delete(current_user, pkupac_id):
        """
        Delete method on this api call should be used for deleting pkupac data for given pkupac id.
        :param current_user:
        :param pkupac_id:
        :return:
        """

        # get pkupac
        pkupac = general.get_object_by_id(
            obj_id=pkupac_id,
            query_model=model.PotencijalniKupac,
            error=errors.ERR_BAD_PKUPAC_ID
        )

        # If status in "rezervisao" or "kupio", than change status of stan to "dostupan"
        if pkupac.status in ("rezervisao", "kupio"):
            stan = general.get_object_by_id(
                obj_id=pkupac.stan_id,
                query_model=model.Stan,
                error=errors.ERR_BAD_STAN_ID
            )
            stan.edit(status="dostupan")
            db.session.add(stan)

        return kupac_helper.delete_kupac(
            pkupac=pkupac_id,
            query_model=model.PotencijalniKupac,
            error=errors.ERR_BAD_PKUPAC_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def post(current_user):
        """
        Post method on this api call should be used for creating pkupac data for given params.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = PKupacCreateSchema().check_and_abort(flask.request.json or {})

        # check stan for stan_id
        stan = general.get_object_by_id(
            obj_id=validated_data.get('stan_id'),
            query_model=model.Stan,
            error=errors.ERR_BAD_STAN_ID
        )

        # check kupac for kupac_id
        kupac = model.Kupac.get_kupac_by_id(
            kupac_id=validated_data.get('kupac_id'),
        )
        # if kupac does not exist, return error
        if not kupac:
            flask_restful.abort(400, error=errors.ERR_BAD_USER_ID)

        # if kupac already has this apartment, return error
        kupac_helper.get_pkupac(stan_id=stan.id, kupac_id=kupac.id)

        # check price
        validated_data = kupac_helper.check_price(
            validated_data=validated_data, cena=stan.cena
        )

        # check if apartment can change status
        pkupac_status = validated_data.get("status")
        if pkupac_status:
            kupac_helper.check_status_of_stan(pkupac_status=pkupac_status, stan_status=stan.status)

            # edit status of stan.
            kupac_helper.edit_status_of_stan(stan=stan, status=pkupac_status)

        # add pkupac in db
        pkupac = model.PotencijalniKupac.create(**validated_data)
        db.session.add(pkupac)
        db.session.flush()

        # set attributes
        setattr(pkupac, "stan", stan)
        setattr(pkupac, "kupac", kupac)

        # if status "potencijalni" sends signal via web socket
        if pkupac.status == 'potencijalni':
            ps_notification_f(pkupac=pkupac, kupac=kupac)

        # if status of pkupac "rezervisao" than populate template
        if pkupac.status == 'rezervisao':
            file_stream = populate_template.create_template_ugovor(data=pkupac)

            return flask.send_file(
                file_stream,
                as_attachment=True,
                attachment_filename=f'{pkupac.kupac.first_name}_{pkupac.kupac.last_name}.docx'
            )

        return pkupac


class ValidatePriceResource(flask_restful.Resource):
    """
    This class will provide api calls for managing validation price for apartment sales.
    """
    path = ['/pkupac/validation/<pkupac_id>']

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    @decorators.check_user_roles(model.User.FINANSIJE)
    def patch(current_user, pkupac_id):
        """
        Patch method on this api call should be used for editing is_validated field for given params.
        Only finansije can confirm the price
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = PKupacValidationSchema().check_and_abort(flask.request.json or {})

        # get pkuoac
        pkupac = general.get_object_by_id(
            obj_id=pkupac_id,
            query_model=model.PotencijalniKupac,
            error=errors.ERR_BAD_PKUPAC_ID
        )

        # if deleted true, return error
        if pkupac.deleted:
            flask_restful.abort(400, error=errors.ERR_OBJECT_IS_DELETED)

        # get stan
        stan = general.get_object_by_id(
            obj_id=pkupac.stan_id,
            query_model=model.Stan,
            error=errors.ERR_BAD_STAN_ID
        )

        # check if stan can change status.
        pkupac_status = 'rezervisao'
        if pkupac_status:
            kupac_helper.check_status_of_stan(pkupac_status=pkupac_status, stan_status=stan.status)

            # edit status of stan.
            kupac_helper.edit_status_of_stan(stan=stan, status=pkupac_status)

        # edit pkupac
        pkupac.edit(
            is_validated=validated_data.get('is_validated'),
            validated_by=current_user.id,
            status='rezervisao'
        )
        db.session.add(pkupac)
        db.session.flush()

        return pkupac


class StanPKupacResource(flask_restful.Resource):
    """
    This method is used for getting potencijalnikupac for given stan id
    """

    path = ['/pkupac/stan/<stan_id>']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, stan_id):
        """
        Get all data by stan id.
        :param current_user:
        :param stan_id:
        :return:
        """
        return model.PotencijalniKupac.get_by_stan_id(stan_id=stan_id)
