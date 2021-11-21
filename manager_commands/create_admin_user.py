from flask_script import Command, Option

import model

from core import db

from passlib.hash import sha256_crypt


class CreateAdminUser(Command):
    """
    This command is used for creating new admin user into db

    Start command:
    python prodajastanova.py create_admin_user --first_name <first_name> --last_name <last_name>
    --username <username>  --password <password>
    """
    option_list = (
        Option('--first_name', dest='first_name'),
        Option('--last_name', dest='last_name'),
        Option('--username', dest='username'),
        Option('--password', dest='password'),
    )

    def run(self, first_name, last_name, username, password):
        # hash password
        password = sha256_crypt.encrypt(password)
        # get data
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password,
            'role': 'administrator'
        }
        # if some data is missing return error
        for key, value in user_data.items():
            if not value:
                return f'ERROR: {key} must be defined'

        # Create user object
        user = model.User.create(**user_data)
        db.session.add(user)
        db.session.commit()
