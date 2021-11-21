import flask_restful
import flask
import model
import errors
from core import db
from utils.api_helpers import general, user_helper
from utils import session
import decorators

from passlib.hash import sha256_crypt

from schemas import (
    UserSchema,
    UserSearchSchema,
    UserRegisterSchema,
    UserLoginSchema,
    UserLogoutSchema
)


def _get_user_for_data(validated_data):
    """
    This method is used for getting user by username and password.
    If user is not found return error.
    :param validated_data:
    :return: ERR_BAD_CREDENTIALS - user does not exist for given data
    """
    user = None

    # Check if username already exists in db
    if validated_data.get('username') and validated_data.get('password'):
        user = model.User.get_by_username(
            username=validated_data.get('username')
        )

    # if user exists check password, otherwise return error
    if user:
        if sha256_crypt.verify(validated_data.get('password'), user.password):
            return user

    flask_restful.abort(400, error=errors.ERR_BAD_CREDENTIALS)


def _check_if_user_exist_for_validated_data(validated_data):
    """
    Check if user already exists in db for given username.
    :param validated_data: username
    :return:ERR_DUPLICATED_USERNAME if username already exists in db.
    """
    # Check if username already exists in db
    if validated_data.get('username') and model.User.get_by_username(username=validated_data.get('username')):
        flask_restful.abort(400, error=errors.ERR_DUPLICATED_USERNAME)


def _check_if_user_can_edit_data(current_user, user_id, role, error):
    """
    The method is used for checking if user can edit data about user
    :param current_user:
    :param user_id:
    :param role:
    :param error:
    :return:
    """
    if current_user.id != int(user_id) and current_user.role != role:
        flask_restful.abort(400, error=error)


class UserResource(flask_restful.Resource):
    """
    This class will provide api calls for managing basic user data.
    """
    path = ['/user/<user_id>']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, user_id):
        """
        Get method on this api call returns user for given id.
        Admin can see data of all users.
        Other users can only see their own data.
        :param current_user:
        :param user_id:
        :return:
        """

        # only admin and current user(own data) can edit data for user
        _check_if_user_can_edit_data(
            current_user=current_user,
            user_id=user_id,
            role='administrator',
            error=errors.ERR_FORBIDDEN_FOR_ROLE
        )

        return general.get_object_by_id(
            obj_id=user_id,
            query_model=model.User,
            error=errors.ERR_BAD_USER_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    def patch(current_user, user_id):
        """
        Patch method on this api call should be used for editing user data.
        Admin can edit data of all users.
        Other users can only edit their own data.
        :param current_user:
        :param user_id:
        :return:
        """
        # only admin and current user(own data) can edit data for user
        _check_if_user_can_edit_data(
            current_user=current_user,
            user_id=user_id,
            role='administrator',
            error=errors.ERR_FORBIDDEN_FOR_ROLE
        )

        # validate data for editing
        data = UserSchema().check_and_abort(flask.request.json or {})

        # if password is in parameters, hash it
        if data.get('password'):
            data['password'] = sha256_crypt.encrypt(data['password'])

        return user_helper.edit_user(
            data=data,
            user_id=user_id,
            query_model=model.User,
            error=errors.ERR_BAD_USER_ID
        )

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    @decorators.get_user_and_check_user_validity
    @decorators.check_user_roles(model.User.ADMINISTRATOR)
    def delete(current_user, user_id):
        """
        Delete method on this api call should be used for deleting user data for given user id.
        Admin can delete data of all users.
        :param current_user:
        :param user_id:
        :return:
        """

        return user_helper.delete_user(
            user_id=user_id,
            query_model=model.User,
            error=errors.ERR_BAD_USER_ID
        )


class UserRegistrationResource(flask_restful.Resource):
    """
    User Registration Resource is used for creating new user into db.
    In case some data is not send error will be returned.
    """
    path = ['/user/register']

    @staticmethod
    @decorators.check_user_roles(model.User.ADMINISTRATOR)
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    def post():
        # Validate schema parameters
        validated_data = UserRegisterSchema().check_and_abort(flask.request.json or {})

        # hash password
        validated_data['password'] = sha256_crypt.encrypt(validated_data.get('password'))

        # Check if user already exists in database
        _check_if_user_exist_for_validated_data(validated_data)

        # Create user object
        user = model.User.create(**validated_data)
        db.session.add(user)

        return {}


class UserLoginResource(flask_restful.Resource):
    """
    User Login Registration Resource is used for logging user with username and password.
    """
    path = ['/public/user/login']

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.to_json
    def post():
        # Validate schema parameters
        validated_data = UserLoginSchema().check_and_abort(flask.request.json or {})
        # get user from db
        user = _get_user_for_data(validated_data)

        # mark user sessions as deleted for given user id and ip_of_login
        model.UserSessions.mark_deleted_for_user_and_ip_of_login(
            user_id=user.id,
            ip_of_login=flask.request.remote_addr
        )

        # delete old session for this user
        session_id = model.UserSessions.get_session_token_for_user_id(user_id=user.id)
        if session_id:
            session.delete_user_session_from_redis(user_sessions=session_id[0])

        # generate and update user session key and add/edit user in redis
        user, session_key = session.generate_and_update_user_session_key(user=user)

        # Add user session in db
        user_session = model.UserSessions.create(**{
            'user_id': user.id,
            'ip_of_login': flask.request.remote_addr,
            'session_token': session_key,
        })
        db.session.add(user_session)
        return {'user': user, 'session_key': session_key}


class UserLogoutResource(flask_restful.Resource):
    """
    User Logout Registration Resource is used for logout user for given device id.
    """
    path = ['/user/logout']

    @staticmethod
    @decorators.flask_sqlalchemy_session_decorator
    @decorators.get_user_and_check_user_validity
    def post(current_user):
        # Validate schema parameters
        validated_data = UserLogoutSchema().check_and_abort(flask.request.json or {})

        # delete user session from db
        user_sessions = model.UserSessions.mark_deleted_for_user_and_ip_of_login(
            user_id=current_user.id,
            ip_of_login=validated_data.get('ip_of_login')
        )

        # delete session from redis
        session.delete_user_session_from_redis(user_sessions=user_sessions)

        return {}


class SearchUsersResource(flask_restful.Resource):
    """
    This resource should be used for getting all users or searching users.
    """
    path = ['/users']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    @decorators.check_user_roles(model.User.ADMINISTRATOR)
    def get(current_user):
        """
        Get method on this api call should be used for getting and searching users.
        Users can filter and sort by all fields and search by first_name and last_name field.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        kwargs = UserSearchSchema().check_and_abort(flask.request.args or {})

        users_count, users = model.User.search_user(**kwargs)

        return {'users_count': users_count, 'users': users}
