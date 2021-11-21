import unittest
import requests
import config


class StanApiTest(unittest.TestCase):
    API_URL = config.API_URL
    STAN_URL = "{}/stan".format(API_URL)
    STANOVI_URL = "{}/stanovi".format(API_URL)
    USER_ADMIN_SESSION = "session:1:cba4ac0bfe9f84eadbcead48f49edaf592894af29fed0ad7cfee5a0587988e2b" \
                         "06040c73377930aa6930e9f03d341bd1889973f0fbd6972a2a2efbd1ba388e86"
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

    # GET request to /stan/<stan_id> returns the details of stan for given id
    def test_get_stan_for_given_id(self):
        r = requests.get(
            f'{StanApiTest.STAN_URL}/4',
            headers={
                'session_id': StanApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # POST request to /stan to create a new stan
    def test_add_stan(self):
        r = requests.post(
            f'{StanApiTest.STAN_URL}',
            json=StanApiTest.STAN_OBJ,
            headers={
                'session_id': StanApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 0)

    # PATCH requests to /stan/<stan_id> to edit existing stan
    def test_update_existing_stan(self):
        edit_obj = {
            "kvadratura": "100"
        }
        r = requests.patch(
            f'{StanApiTest.STAN_URL}/7',
            json=edit_obj,
            headers={
                'session_id': StanApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # DELETE requests to /stan/<stan_id> to delete stan
    def test_delete_stan(self):
        r = requests.delete(
            f'{StanApiTest.STAN_URL}/7',
            headers={
                'session_id': StanApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    # GET request to /stanovi returns the details of users for given parameters
    def test_filter_and_sort_stan(self):
        r = requests.get(
            f'{StanApiTest.STANOVI_URL}?page=1&per_page=10&sort_by=id&sort_desc=false&kvadratura=100',
            headers={
                'session_id': StanApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)
