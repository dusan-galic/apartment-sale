from utils.api_helpers import general


def edit_stan(data, stan_id, query_model, error):
    """
    This method is used for editing apartment data for given params and apartment id
    :param data:
    :param stan_id:
    :param query_model:
    :param error:
    :return:
    """

    return general.edit_object(
        obj_id=stan_id,
        query_model=query_model,
        data=data,
        error=error
    )


def delete_stan(stan_id, query_model, error):
    """
    This method is used for deleting apartment data for given apartment id
    :param stan_id:
    :param query_model:
    :param error:
    :return:
    """

    return general.delete_object(
        obj_id=stan_id,
        query_model=query_model,
        error=error
    )
