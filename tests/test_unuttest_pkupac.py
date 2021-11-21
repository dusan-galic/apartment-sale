import unittest
import requests
import config


class PKupacApiTest(unittest.TestCase):
    API_URL = config.API_URL
    PKUPAC_URL = "{}/pkupac".format(API_URL)
    PKUPAC_VALIDATE_URL = "{}/pkupac/validation".format(API_URL)
    PKUPAC_STAN_URL = "{}/pkupac/stan".format(API_URL)
    USER_ADMIN_SESSION = "session:1:cba4ac0bfe9f84eadbcead48f49edaf592894af29fed0ad7cfee5a0587988e2b" \
                         "06040c73377930aa6930e9f03d341bd1889973f0fbd6972a2a2efbd1ba388e86"
    PKUPAC_OBJ = {
        "cena_za_kupca": 90000,
        "napomen": "",
        "stan_id": 7,
        "kupac_id": 6
    }

    # GET request to /pkupac/<pkupac_id> returns the details of stan for given id
    def test_get_pkupac_for_given_id(self):
        r = requests.get(
            f'{PKupacApiTest.PKUPAC_URL}/6',
            headers={
                'session_id': PKupacApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    # POST request to /pkupac to create a new pkupac
    def test_add_pkupac(self):
        r = requests.post(
            f'{PKupacApiTest.PKUPAC_URL}',
            json=PKupacApiTest.PKUPAC_OBJ,
            headers={
                'session_id': PKupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 0)

    # PATCH requests to /pkupac/<pkupac_id> to edit existing pkupac
    def test_update_existing_pkupac(self):
        edit_obj = {
            "broj_ugovora": "fasf122"
        }
        r = requests.patch(
            f'{PKupacApiTest.PKUPAC_URL}/11',
            json=edit_obj,
            headers={
                'session_id': PKupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # DELETE requests to /pkupac/<pkupac_id> to delete pkupac
    def test_delete_pkupac(self):
        r = requests.delete(
            f'{PKupacApiTest.PKUPAC_URL}/11',
            headers={
                'session_id': PKupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    # PATCH requests to /pkupac/validation/<pkupac_id> to validate price of pkupac
    def test_update_validate_pkupac(self):
        edit_obj = {
            "is_validated": True
        }
        r = requests.patch(
            f'{PKupacApiTest.PKUPAC_VALIDATE_URL}/11',
            json=edit_obj,
            headers={
                'session_id': PKupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 403)
        self.assertGreater(len(r.json()), 0)

    # GET request to /pkupac/stan/<stan_id> returns the details of stan for given id
    def test_get_pkupac_for_given_stan_id(self):
        r = requests.get(
            f'{PKupacApiTest.PKUPAC_STAN_URL}/6',
            headers={
                'session_id': PKupacApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
