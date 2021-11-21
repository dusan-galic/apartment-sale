import flask_restful
from core import db


def get_object_by_id(obj_id, query_model, error):
    """
    This method is getting object by id.
    :param obj_id: Id of object
    :param query_model: model which need to be queried example(model.User, model.Stan)
    :param error: which error will be returned if object is not found
    :return:ERR_BAD_{model name}_ID: If object does not exist for given object_id
            object: for given object_id
    """
    # Return object if exist otherwise return error
    return query_model.get_by_id(obj_id) or flask_restful.abort(400, error=error)


def edit_object(obj_id, query_model, data, error):
    """
    This method is editing object for given id and params.
    :param obj_id: Id of object
    :param query_model: model which need to be queried example(model.User, model.Stan)
    :param data: data for editing
    :param error: which error will be returned if object is not found
    :return:ERR_BAD_{model name}_ID: If photo does not exist for given object_id
            object: for given photo_id
    """
    object_model = get_object_by_id(
        obj_id=obj_id,
        query_model=query_model,
        error=error
    )

    object_model.edit(**data)
    db.session.add(object_model)

    return object_model


def delete_object(obj_id, query_model, error):
    """
    This method is deleting object for given id.
    :param obj_id: Id of object
    :param query_model: model which need to be queried example(model.User, model.Stan)
    :param error: which error will be returned if object is not found
    :return:ERR_BAD_{model name}_ID: If photo does not exist for given object_id
            object: for given photo_id
    """
    object_model = get_object_by_id(
        obj_id=obj_id,
        query_model=query_model,
        error=error
    )

    object_model.edit(deleted=True)
    db.session.add(object_model)

    return {}
