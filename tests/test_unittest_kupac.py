import unittest
import requests
import config


class KupacApiTest(unittest.TestCase):
    API_URL = config.API_URL
    KUPAC_URL = "{}/kupac".format(API_URL)
    KUPCI_URL = "{}/kupci".format(API_URL)
    USER_ADMIN_SESSION = "session:1:cba4ac0bfe9f84eadbcead48f49edaf592894af29fed0ad7cfee5a0587988e2b" \
                         "06040c73377930aa6930e9f03d341bd1889973f0fbd6972a2a2efbd1ba388e86"
    KUPAC_OBJ = {
        "first_name": "test",
        "last_name": "testic",
        "email": "test.n@gmail.com",
        "broj_telefona": "2353463467453",
        "jmbg": "458568574",
        "adresa": "Tu i tamo 34",
        "tip": "fizicko"
    }

    # GET request to /kupac/<kupac_id> returns the details of kupac for given id
    def test_get_kupac_for_given_id(self):
        r = requests.get(
            f'{KupacApiTest.KUPAC_URL}/1',
            headers={
                'session_id': KupacApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # POST request to /kupac to create a new kupac
    def test_add_kupac(self):
        r = requests.post(
            f'{KupacApiTest.KUPAC_URL}',
            json=KupacApiTest.KUPAC_OBJ,
            headers={
                'session_id': KupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 0)

    # PATCH requests to /kupac/<kupac_id> to edit existing kupac
    def test_update_existing_kupac(self):
        edit_obj = {
            "first_name": "test1"
        }
        r = requests.patch(
            f'{KupacApiTest.KUPAC_URL}/8',
            json=edit_obj,
            headers={
                'session_id': KupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # DELETE requests to /kupac/<kupac_id> to delete kupac
    def test_delete_kupac(self):
        r = requests.delete(
            f'{KupacApiTest.KUPAC_URL}/8',
            headers={
                'session_id': KupacApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    # GET request to /kupci returns the details of users for given parameters
    def test_filter_and_sort_kupac(self):
        r = requests.get(
            f'{KupacApiTest.KUPCI_URL}?page=1&per_page=10&sort_by=id&sort_desc=false&first_name=test1',
            headers={
                'session_id': KupacApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # GET request to /users returns the details of users for given parameters
    def test_search_data(self):
        r = requests.get(
            f'{KupacApiTest.KUPCI_URL}?page=1&per_page=10&sort_by=id&sort_desc=false&search_string=tes',
            headers={
                'session_id': KupacApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)
