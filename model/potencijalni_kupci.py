import model
from core import db, data_types
from core.base_model import BaseModel


class PotencijalniKupac(db.Model, BaseModel):
    __tablename__ = 'tbl_potencijlani_kupac'

    STATUS = (
        ('potencijalni', 'potencijalni'),
        ('rezervisao', 'rezervisao'),
        ('kupio', 'kupio'),
    )

    NACIN_KUPOVINE = (
        ('kes', 'kes'),
        ('kredit', 'kredit'),
        ('ucesce_i_kredit', 'ucesce_i_kredit')
    )

    stan_id = db.Column(db.Integer, db.ForeignKey('tbl_stan.id'), nullable=False)
    kupac_id = db.Column(db.Integer, db.ForeignKey('tbl_kupac.id'), nullable=False)
    cena_za_kupca = db.Column(db.Float, nullable=False)
    napomena = db.Column(db.Text)
    broj_ugovora = db.Column(db.String(30), unique=True)
    datum_ugovora = db.Column(db.DateTime)
    status = db.Column(
        data_types.StringChoiceType(choices=STATUS, length=20),
        default='rezervisao',
        server_default='rezervisao',
        nullable=False
    )
    nacin_kupovine = db.Column(
        data_types.StringChoiceType(choices=NACIN_KUPOVINE, length=20)
    )

    kupac_stana = db.relationship('Kupac', backref='kupac_stana')
    stan = db.relationship('Stan', backref='stan')

    # finansije odobravaju ako se cena za kupca ne poklapa sa cenom stana
    is_validated = db.Column(db.Boolean, default=False, server_default=db.false())
    validated_by = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))

    @classmethod
    def get_pkupac_by_id(cls, obj_id):
        return cls.query.filter(
            cls.id == obj_id,
            ~cls.deleted
        ).options(db.joinedload(cls.kupac_stana)).all()

    @classmethod
    def get_by_stan_id(cls, stan_id):
        return cls.query.filter(
            cls.stan_id == stan_id,
            ~cls.deleted
        ).options(db.joinedload(cls.kupac_stana)).all()

    @classmethod
    def get_number_of_sold_apartments(cls, date_from, date_to):
        stan = cls.query \
            .join(model.Stan, cls.stan_id == model.Stan.id) \
            .filter(
                model.Stan.status == 'prodat',
                ~model.Stan.deleted,
                model.Stan.date_of_update >= date_from,
                model.Stan.date_of_update < date_to,
            ).options(db.joinedload(cls.stan))

        return stan.count(), stan.all()

    @classmethod
    def get_pkupac_and_stan_by_pkupac_id(cls, pkupac_id):
        stan = cls.query.filter(
            cls.kupac_id == pkupac_id,
            ~cls.deleted
        ).options(db.joinedload(cls.stan)) \
         .options(db.joinedload(cls.kupac_stana))

        return stan.count(), stan.all()

    @classmethod
    def get_pkupac_and_stan_by_pkupac_id_and_status(cls, pkupac_id, status, date_from, date_to):
        stan = cls.query.filter(
            cls.kupac_id == pkupac_id,
            cls.status == status,
            cls.date_of_update >= date_from,
            cls.date_of_update < date_to,
            ~cls.deleted
        ).options(db.joinedload(cls.stan)) \
            .options(db.joinedload(cls.kupac_stana))

        return stan.count(), stan.all()

    @classmethod
    def get_pkupac_by_stan_id_and_pkupac_id(cls, stan_id, kupac_id):
        return cls.query.filter(
            cls.stan_id == stan_id,
            cls.kupac_id == kupac_id,
            ~cls.deleted
        ).all()
