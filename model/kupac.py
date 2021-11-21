from core import db, data_types
from core.base_model import BaseModel
from utils.model_helpers import search_model


class Kupac(db.Model, BaseModel):
    __tablename__ = 'tbl_kupac'

    KUPAC_TYPES = (
        ('fizicko', 'fizicko'),
        ('pravno', 'pravno')
    )

    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    broj_telefona = db.Column(db.String(20), unique=True, nullable=False)
    jmbg = db.Column(db.String(20), unique=True, nullable=False)
    adresa = db.Column(db.Text, nullable=False)
    tip = db.Column(
        data_types.StringChoiceType(choices=KUPAC_TYPES, length=20),
        default='fizicko',
        server_default='fizicko',
        nullable=False
    )

    @classmethod
    def get_kupac_by_id(cls, kupac_id):
        return cls.query.filter(cls.id == kupac_id, ~cls.deleted).first()

    @classmethod
    def search_kupac(cls, **kwargs):
        # Get kupac for search_string combination and add filters and sorting
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
        # Get kupac count for search_string combination and add filters and sorting
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
