import flask_restful
import errors
import model
from utils.api_helpers import general
from core import db


def edit_kupac(data, pkupac_id, query_model, error, current_user=None):
    """
    This method is used for editing potencijalnikupac or kupac data for given params and potencijalnikupac id
    Prodavac can not edit or add broj_ugovora, datum_ugovore and is_validated.
    :param current_user:
    :param data:
    :param pkupac_id:
    :param query_model:
    :param error:
    :return:
    """
    if current_user:
        finansije_list_fields = ['broj_ugovora', 'datum_ugovora', 'is_validated']
        for key, value in data.items():
            if key in finansije_list_fields and current_user.role == 'prodavac':
                flask_restful.abort(400, error=errors.ERR_FORBIDDEN_FOR_ROLE)

    return general.edit_object(
        obj_id=pkupac_id,
        query_model=query_model,
        data=data,
        error=error
    )


def delete_kupac(pkupac, query_model, error):
    """
    This method is used for deleting pkupac data for given pkupac id
    :param pkupac:
    :param query_model:
    :param error:
    :return:
    """

    return general.delete_object(
        obj_id=pkupac,
        query_model=query_model,
        error=error
    )


def edit_status_of_stan(stan, status):
    """
    This method is used fot editing status of apartment
    :param stan:
    :param status:
    :return:
    """
    if status == "potencijalni":
        stan.edit(status="dostupan")
    elif status == "rezervisao":
        stan.edit(status="rezervisan")
    elif status == "kupio":
        stan.edit(status="prodat")
    db.session.add(stan)


def check_status_of_stan(pkupac_status, stan_status):
    """
    This method is checking status of stan.
    :param pkupac_status:
    :param stan_status:
    :return:
    """
    # ToDo write this better

    if pkupac_status in ("rezervisao", "potencijalni") and stan_status in ("rezervisan", "prodat") or \
        pkupac_status == "kupio" and stan_status == "prodat":
        flask_restful.abort(400, error=errors.ERR_BAD_STATUS)


def check_price(validated_data, cena):
    """
    This method is used for checking price.
    :param validated_data:
    :param cena:
    :return:
    """
    # if price of apartment is not equal to price of buyer
    # than status of buyer should be "potencijalni"
    validated_data['status'] = 'potencijalni' \
        if validated_data.get('cena_za_kupca') != cena else 'rezervisao'
    return validated_data


def get_pkupac(stan_id, kupac_id):
    """
    This method is used for checking if kupac already has apartment.
    :param stan_id:
    :param kupac_id:
    :return:
    """
    # get pkupac for pkupac id and apartment id
    pkupac = model.PotencijalniKupac.get_pkupac_by_stan_id_and_pkupac_id(
        stan_id=stan_id,
        kupac_id=kupac_id
    )

    # if pkupac exists, return error
    if pkupac:
        flask_restful.abort(400, errors=errors.ERR_DUPLICATED_PKUPAC)
