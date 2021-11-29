import pytest
from pathlib import Path

import core
from runner import routes


TEST_DB = "test.db"
BASE_DIR = Path(__file__).resolve().parent.parent

USER_ADMIN_SESSION = "session:1:cba4ac0bfe9f84eadbcead48f49edaf592894af29fed0ad7cfee5a0587988e2b" \
                         "06040c73377930aa6930e9f03d341bd1889973f0fbd6972a2a2efbd1ba388e86"
USER_PRODAVAC_SESSION = "session:3:b2db6c41fbd01739764f5a56a58217723e00bd956426f4077076b63c4ffc8" \
                        "b72d01c26d0c9d7bc7375ec9f7059359fadc52e899a7ac564e11ee4ec34a8578e19"
USER_FINANSIJE_SESSION = "session:2:cc5c4f41476dd72b1d539ed31ee605c4868e9efc4dc958d0c915264a3260" \
                         "1a257a66e9a9c7edca8b748e655d84e885ff42a02e457465e6cfbc3c89f61500ba17"

USER_OBJ = {
    "first_name": "test",
    "last_name": "test",
    "username": "testtest",
    "role": "prodavac",
    "password": "test123"
}

KUPAC_OBJ = {
    "first_name": "test",
    "last_name": "testic",
    "email": "test.n@gmail.com",
    "broj_telefona": "2353463467453",
    "jmbg": "458568574",
    "adresa": "Tu i tamo 34",
    "tip": "fizicko"
}

STAN_OBJ = {
    "lamela": "B",
    "kvadratura": "55",
    "sprat": 3,
    "broj_soba": 2.5,
    "broj_stana": 3,
    "orjentisanost": "zapad",
    "broj_terasa": 1,
    "cena": 90000.0,
    "adresa": "Bulevar"
}

PKUPAC_OBJ = {
    "cena_za_kupca": 38000,
    "napomen": "",
    "stan_id": 5,
    "kupac_id": 1
}


@pytest.fixture
def app():
    database_mysql = "mysql+pymysql://fww:fww2020@localhost/prodaja_stanova?charset=utf8mb4&use_unicode=1"
    # database = f"sqlite:///{BASE_DIR}/tests_pytest/{TEST_DB}"
    # database_url = f"sqlite:///{BASE_DIR}/tests_pytest/{TEST_DB}"
    app = core.create_app(
        restful_routes=routes,
        test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": database_mysql
        }
    )
    app.app_context().push()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def user_session_admin():
    return USER_ADMIN_SESSION

    
@pytest.fixture
def user_session_prodavac():
    return USER_PRODAVAC_SESSION


@pytest.fixture
def user_session_finansije():
    return USER_FINANSIJE_SESSION


@pytest.fixture
def add_user_data():
    return USER_OBJ


@pytest.fixture
def add_kupac_data():
    return KUPAC_OBJ


@pytest.fixture
def add_stan_data():
    return STAN_OBJ


@pytest.fixture
def add_pkupac_data():
    return PKUPAC_OBJ
