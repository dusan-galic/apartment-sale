from core import db, data_types
from core.base_model import BaseModel
from utils.model_helpers import search_model
import flask_restful


class User(db.Model, BaseModel):
    __tablename__ = 'tbl_user'

    ADMINISTRATOR = 'administrator'  # administriraju sistemom
    PRODAVAC = 'prodavac'  # osnovne operacije
    FINANSIJE = 'finansije'  # osnovne operacije + odobravanje cene, broj ugovora...

    USER_ROLES = (
        (ADMINISTRATOR, ADMINISTRATOR),
        (PRODAVAC, PRODAVAC),
        (FINANSIJE, FINANSIJE)
    )

    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100), unique=True)
    password = db.deferred(db.Column(db.Text))
    role = db.Column(
        data_types.StringChoiceType(choices=USER_ROLES, length=20),
        default='prodavac',
        server_default='prodavac',
    )

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter(cls.username == username, ~cls.deleted).first()

    @classmethod
    def search_user(cls, **kwargs):
        # Get users for search_string combination and add filters and sorting
        search_query = search_model.sort_query_and_add_filters(
            cls_model=cls,
            search_query=search_model.search_by_first_and_last_name(
                cls_model=cls,
                search_query=cls.query,
                search_string=kwargs.get('search_string', '')
            ),
            **kwargs
        ) \
            .paginate(page=kwargs.get('page', 1), per_page=kwargs.get('per_page', 25), error_out=False).items
        # Get users count for search_string combination and add filters and sorting
        search_query_count = search_model.sort_query_and_add_filters(
            cls_model=cls,
            search_query=search_model.search_by_first_and_last_name(
                cls_model=cls,
                search_query=db.session.query(db.func.count(cls.id)),
                search_string=kwargs.get('search_string', '')
            ),
            **kwargs
        ).all()[0][0]

        return search_query_count, search_query

    #################
    # CHECK METHODS #
    #################
    def check_if_user_not_deleted(self):
        """
        method is used for checking user
        :return:
        """
        # If user is deleted
        if self.deleted:
            flask_restful.abort(403, error='ERR_USER_IS_DELETED')


class UserSessions(db.Model, BaseModel):
    __tablename__ = 'tbl_user_sessions'

    user_id = db.Column(db.Integer, nullable=False)
    ip_of_login = db.Column(db.Text, nullable=False)
    session_token = db.Column(db.Text, nullable=False)

    @classmethod
    def mark_deleted_for_user_and_ip_of_login(cls, user_id, ip_of_login):
        sessions = cls.query.filter(cls.user_id == user_id, cls.ip_of_login == ip_of_login, ~cls.deleted)
        all_sessions = sessions.all()
        sessions.update({cls.deleted: True}, synchronize_session=False)
        return all_sessions

    @classmethod
    def get_session_token_for_user_id(cls, user_id):
        return db.session.query(cls.session_token).filter(cls.user_id == user_id, ~cls.deleted).first()
