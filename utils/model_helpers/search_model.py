import model
from core import db

fields = ['id', 'role', 'tip', 'status', 'orjentisanost']


def add_filters_to_query(cls_model, search_query, **kwargs):
    """
    This method add filters for all kwargs parameters if they exist in cls_model
    :param cls_model:
    :param search_query:
    :param kwargs:
    :return:
    """
    # Add filters to search
    for attr, value in kwargs.items():
        if getattr(cls_model, attr, None) and value is not None:
            if attr in fields or isinstance(value, bool):
                search_query = search_query.filter(getattr(cls_model, attr) == value)
            else:
                search_query = search_query.filter(getattr(cls_model, attr).like("%{}%".format(value)))
        elif '_to' in attr or '_from' in attr:
            # Get field name without _to or _from keyword
            model_attr = attr.rsplit('_', 1)[0]
            if getattr(cls_model, model_attr, None) and value:
                if '_to' in attr:
                    search_query = search_query.filter(getattr(cls_model, model_attr) <= value)
                else:
                    search_query = search_query.filter(getattr(cls_model, model_attr) >= value)
    return search_query


def sort_query(cls_model, search_query, default_order=None, sort_model=None, **kwargs):
    """
    This method is used for sorting query for given sort_by and sort_desc parameters, if not given default sort is
    by first and last name.
    :param cls_model:
    :param search_query:
    :param kwargs:
    :param default_order:
    :param sort_model:
    :return:
    """
    from model import User
    # Get sorting if it is send, else sort by first_name and last_name

    # Split sort_by by . if send in param, backoffice is sending template.price, user.first_name
    sort_by = kwargs.get('sort_by', '').split('.')[1] if '.' in kwargs.get('sort_by', '') else kwargs.get('sort_by', '')

    # Get sorting if it is send, else sort by first_name and last_name
    if sort_model and getattr(sort_model, sort_by, None):
        if kwargs.get('sort_desc') == 'true':
            search_query = search_query.order_by(getattr(sort_model, sort_by).desc())
        else:
            search_query = search_query.order_by(getattr(sort_model, sort_by))
    elif getattr(cls_model, sort_by, None):
        if kwargs.get('sort_desc') == 'true':
            search_query = search_query.order_by(getattr(cls_model, sort_by).desc())
        else:
            search_query = search_query.order_by(getattr(cls_model, sort_by))
    elif default_order == 'user':
        search_query = search_query.order_by(cls_model.first_name, cls_model.last_name)
    elif getattr(User, sort_by, None):
        if kwargs.get('sort_desc') == 'true':
            search_query = search_query.order_by(getattr(User, sort_by).desc())
        else:
            search_query = search_query.order_by(getattr(User, sort_by))
    else:
        search_query = search_query.order_by(cls_model.date_of_creation.desc())
    return search_query


def sort_query_and_add_filters(cls_model, search_query, default_order=None, sort_model=None, **kwargs):
    """
    This method is used for calling methods for sorting and filtering query for given search_query and kwargs.
    :param cls_model:
    :param search_query:
    :param kwargs:
    :param default_order:
    :param sort_model:
    :return:
    """
    # Add filters to query
    search_query = add_filters_to_query(
        cls_model=cls_model,
        search_query=search_query,
        **kwargs
    )

    # Add sorting to query
    search_query = sort_query(
        cls_model=cls_model,
        search_query=search_query,
        default_order=default_order,
        sort_model=sort_model,
        **kwargs

    )
    return search_query


def search_by_first_and_last_name(cls_model, search_query, search_string):
    """
    This model is used for searching users depending on search_query provided, and filter user
    first and last name combination given search_string value.
    :param cls_model:
    :param search_query:
    :param search_string:
    :return:
    """
    search_terms = ['%{}%'.format(x) for x in search_string.split(' ')]

    return search_query.filter(
        db.or_(
            *[cls_model.first_name.like(name) for name in search_terms],
            *[cls_model.last_name.like(name) for name in search_terms]
        ),
        ~cls_model.deleted
    )
