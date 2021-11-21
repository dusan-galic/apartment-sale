import unittest
import requests
import config


class UserApiTest(unittest.TestCase):
    API_URL = config.API_URL
    USER_URL = "{}/user".format(API_URL)
    USERS_URL = "{}/users".format(API_URL)
    USER_ADMIN_SESSION = "session:1:cba4ac0bfe9f84eadbcead48f49edaf592894af29fed0ad7cfee5a0587988e2b" \
                         "06040c73377930aa6930e9f03d341bd1889973f0fbd6972a2a2efbd1ba388e86"
    USER_OBJ = {
        "first_name": "test",
        "last_name": "test",
        "username": "testtest",
        "role": "prodavac",
        "password": "test123"
    }

    # GET request to /user/<user_id> returns the details of user for given id
    def test_get_user_for_given_id(self):
        r = requests.get(
            f'{UserApiTest.USER_URL}/1',
            headers={
                'session_id': UserApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # POST request to /user to create a new user
    def test_add_user(self):
        r = requests.post(
            f'{UserApiTest.USER_URL}/register',
            json=UserApiTest.USER_OBJ,
            headers={
                'session_id': UserApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    # PATCH requests to /user/<user_id> to edit existing user
    def test_update_existing_user(self):
        edit_obj = {
            "first_name": "test1"
        }
        r = requests.patch(
            f'{UserApiTest.USER_URL}/6',
            json=edit_obj,
            headers={
                'session_id': UserApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # DELETE requests to /user/<user_id> to delete user
    def test_delete_user(self):
        r = requests.delete(
            f'{UserApiTest.USER_URL}/6',
            headers={
                'session_id': UserApiTest.USER_ADMIN_SESSION
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    # GET request to /users returns the details of users for given parameters
    def test_filter_and_sort_user(self):
        r = requests.get(
            f'{UserApiTest.USERS_URL}?page=1&per_page=10&sort_by=id&sort_desc=false&first_name=test',
            headers={
                'session_id': UserApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)

    # GET request to /users returns the details of users for given parameters
    def test_search_data(self):
        r = requests.get(
            f'{UserApiTest.USERS_URL}?page=1&per_page=10&sort_by=id&sort_desc=false&search_string=tes',
            headers={
                'session_id': UserApiTest.USER_ADMIN_SESSION
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 1)
