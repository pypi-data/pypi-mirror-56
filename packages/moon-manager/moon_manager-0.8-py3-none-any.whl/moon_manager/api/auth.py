# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Auth API"""
from falcon import HTTP_204, HTTP_400
import hug
import logging
from moon_utilities.auth_functions import basic_authentication, api_key_authentication
from moon_utilities.auth_functions import get_api_key_for_user, del_api_key_for_user

logger = logging.getLogger("moon.manager.api.status")


@hug.get("/auth/", requires=basic_authentication)
def get_api_key(authed_user: hug.directives.user = None):
    """
    Get API key
    :return: API key
    """
    return get_api_key_for_user(authed_user)


@hug.delete("/auth/", requires=api_key_authentication)
def del_api_key(response, authed_user: hug.directives.user = None):
    """
    Delete API key
    :return: None
    """
    if del_api_key_for_user(authed_user):
        response.status = HTTP_204
    else:
        response.status = HTTP_400
    return
