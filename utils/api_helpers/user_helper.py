from utils.api_helpers import general


def edit_user(data, user_id, query_model, error):
    """
    This method is used for editing user data for given params and user id
    :param data:
    :param user_id:
    :param query_model:
    :param error:
    :return:
    """
    return general.edit_object(
        obj_id=user_id,
        query_model=query_model,
        data=data,
        error=error
    )


def delete_user(user_id, query_model, error):
    """
    This method is used for deleting user data for given user id
    :param user_id:
    :param query_model:
    :param error:
    :return:
    """

    return general.delete_object(
        obj_id=user_id,
        query_model=query_model,
        error=error
    )