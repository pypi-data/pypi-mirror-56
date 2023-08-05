# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Users
"""
import hug
import logging
import getpass
from tinydb import Query
from moon_utilities.auth_functions import db, init_db, add_user, get_api_key

LOGGER = logging.getLogger("moon.manager.api." + __name__)

UsersAPI = hug.API('users')


@hug.object(name='users', version='1.0.0', api=UsersAPI)
class UsersCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod  # nosec
    @hug.object.cli
    def add(username, password: hug.types.text = ""):
        """
        Add a user to the database
        """
        return add_user(username, password)

    @staticmethod  # nosec
    @hug.object.cli
    def key(username, password: hug.types.text = ""):
        """
        Authenticate a username and password against our database
        """
        if password == "":
            password = getpass.getpass()
        return get_api_key(username, password)

    @staticmethod
    @hug.object.cli
    def list(human: bool = False):
        """
        List users from the database
        """
        global db
        if db is None:
            init_db()
        user_model = Query()
        users = db.search(user_model.username.matches('.*'))
        if human:
            result = "Users"
            if users:
                for user in users:
                    result += f"\n{user['username']} : \n"
                    result += f"\tusername : {user['username']}\n"
                    result += f"\tapi_key : {user['api_key']}"
            else:
                result += f"\nNo user"
            return result
        else:
            result = []
            if users:
                for user in users:
                    result.append({
                        'username': user['username'],
                        'api_key': user['api_key']
                    })
            return {'users': result}







