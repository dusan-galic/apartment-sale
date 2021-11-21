import marshmallow
from utils.marshmallow_helpers import SuperSchema


class PageAndSizeSchema(SuperSchema):
    page = marshmallow.fields.Int(required=True, default=1)
    per_page = marshmallow.fields.Int(required=True, default=25)


class SortSchema(SuperSchema):
    sort_by = marshmallow.fields.Str(required=True, default='id')
    sort_desc = marshmallow.fields.Str(required=True, default='false')


class BasicUserSchema(SuperSchema):
    first_name = marshmallow.fields.Str()
    last_name = marshmallow.fields.Str()
    username = marshmallow.fields.Str()


class UserSchema(BasicUserSchema):
    password = marshmallow.fields.Str()


class UserSearchSchema(BasicUserSchema, SortSchema, PageAndSizeSchema):
    search_string = marshmallow.fields.Str()
    role = marshmallow.fields.Str()


class UserRegisterSchema(SuperSchema):
    first_name = marshmallow.fields.Str(required=True)
    last_name = marshmallow.fields.Str(required=True)
    username = marshmallow.fields.Str(required=True)
    role = marshmallow.fields.Str(required=True)
    password = marshmallow.fields.Str(required=True)


class UserLoginSchema(SuperSchema):
    username = marshmallow.fields.Str()
    password = marshmallow.fields.Str()


class UserLogoutSchema(SuperSchema):
    ip_of_login = marshmallow.fields.Str(required=True)


class StanSchema(SuperSchema):
    lamela = marshmallow.fields.Str()
    kvadratura = marshmallow.fields.Float()
    sprat = marshmallow.fields.Int()
    broj_soba = marshmallow.fields.Float()
    broj_stana = marshmallow.fields.Int()
    orjentisanost = marshmallow.fields.Str()
    broj_terasa = marshmallow.fields.Str()
    cena = marshmallow.fields.Float()
    status = marshmallow.fields.Str()
    adresa = marshmallow.fields.Str()


class StanCreateSchema(SuperSchema):
    lamela = marshmallow.fields.Str(required=True)
    kvadratura = marshmallow.fields.Float(required=True)
    sprat = marshmallow.fields.Int(required=True)
    broj_soba = marshmallow.fields.Float(required=True)
    broj_stana = marshmallow.fields.Int(required=True)
    orjentisanost = marshmallow.fields.Str(required=True)
    broj_terasa = marshmallow.fields.Int(required=True)
    cena = marshmallow.fields.Float(required=True)
    status = marshmallow.fields.Str()
    adresa = marshmallow.fields.Str(required=True)


class StanSearchSchema(StanSchema, SortSchema, PageAndSizeSchema):
    search_string = marshmallow.fields.Str()


class PKupacEditSchema(SuperSchema):
    cena_za_kupca = marshmallow.fields.Float()
    napomena = marshmallow.fields.Str()
    broj_ugovora = marshmallow.fields.Str()
    datum_ugovora = marshmallow.fields.Str()
    status = marshmallow.fields.Str()
    is_validated = marshmallow.fields.Boolean()
    nacin_kupovine = marshmallow.fields.Str()


class PKupacCreateSchema(SuperSchema):
    cena_za_kupca = marshmallow.fields.Float(required=True)
    napomena = marshmallow.fields.Str()
    status = marshmallow.fields.Str()
    stan_id = marshmallow.fields.Int(required=True)
    kupac_id = marshmallow.fields.Int(required=True)
    nacin_kupovine = marshmallow.fields.Str()


class PKupacValidationSchema(SuperSchema):
    is_validated = marshmallow.fields.Boolean(required=True)


class KupacEditSchema(SuperSchema):
    first_name = marshmallow.fields.Str()
    last_name = marshmallow.fields.Str()
    email = marshmallow.fields.Str()
    broj_telefona = marshmallow.fields.Str()
    jmbg = marshmallow.fields.Str()
    adresa = marshmallow.fields.Str()
    tip = marshmallow.fields.Str()


class KupacCreateSchema(SuperSchema):
    first_name = marshmallow.fields.Str(required=True)
    last_name = marshmallow.fields.Str(required=True)
    email = marshmallow.fields.Str(required=True)
    broj_telefona = marshmallow.fields.Str(required=True)
    jmbg = marshmallow.fields.Str(required=True)
    adresa = marshmallow.fields.Str(required=True)
    tip = marshmallow.fields.Str()


class KupacSearchSchema(KupacEditSchema, PageAndSizeSchema, SortSchema):
    search_string = marshmallow.fields.Str()


###########
# REPORTS #
###########
class IntervalDate(SuperSchema):
    date_from = marshmallow.fields.Date(required=True)
    date_to = marshmallow.fields.Date(required=True)

