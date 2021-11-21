from sqlalchemy import func

from core import db, data_types
from core.base_model import BaseModel
from utils.model_helpers import search_model


class Stan(db.Model, BaseModel):
    __tablename__ = 'tbl_stan'

    OR_TYPES = (
        ('jug', 'jug'),
        ('zapad', 'zapad'),
        ('sever', 'sever'),
        ('istok', 'istok')
    )

    STATUS_TYPES = (
        ('dostupan', 'dostupan'),
        ('rezervisan', 'rezervisan'),
        ('prodat', 'prodat')
    )

    lamela = db.Column(db.String(10), nullable=False)  # can be a combination of characters
    kvadratura = db.Column(db.Float, nullable=False)
    sprat = db.Column(db.Integer, nullable=False)
    broj_soba = db.Column(db.Float, nullable=False)
    orjentisanost = db.Column(
        data_types.StringChoiceType(choices=OR_TYPES, length=20),
        nullable=False
    )
    broj_terasa = db.Column(db.Integer, default=0, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    adresa = db.Column(db.Text, nullable=False)
    broj_stana = db.Column(db.Integer, nullable=False)
    status = db.Column(
        data_types.StringChoiceType(choices=STATUS_TYPES, length=20),
        default='dostupan',
        server_default='dostupan',
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'), nullable=False)  # create by

    user = db.relationship('User')

    @classmethod
    def filter_stan(cls, **kwargs):
        # Get stan and add filters and sorting
        search_query = search_model.sort_query_and_add_filters(
            cls_model=cls,
            search_query=cls.query,
            **kwargs
        ) \
            .paginate(page=kwargs.get('page', 1), per_page=kwargs.get('per_page', 25), error_out=False).items
        # Get stan count and add filters and sorting
        search_query_count = search_model.sort_query_and_add_filters(
            cls_model=cls,
            search_query=db.session.query(db.func.count(cls.id)),
            **kwargs
        ).all()[0][0]

        return search_query_count, search_query

    @classmethod
    def get_num_of_apartments_per_status(cls, date_from, date_to):
        return db.session.query(cls.status, func.count(cls.id)).filter(
            cls.date_of_update > date_from,
            cls.date_of_update < date_to,
            ~cls.deleted
        ).group_by(cls.status).all()
