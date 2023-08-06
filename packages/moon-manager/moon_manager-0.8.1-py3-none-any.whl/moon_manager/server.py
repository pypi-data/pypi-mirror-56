# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import hug
import logging
from moon_manager.api import status, logs, configuration, pdp, policy, slave, auth, \
    perimeter, assignments, meta_data, meta_rules, models, \
    json_import, json_export, rules, data, attributes
from moon_manager import db_driver,orchestration_driver
from moon_utilities.auth_functions import init_db
from falcon.http_error import HTTPError
from moon_manager.api import ERROR_CODE
from moon_utilities import exceptions
LOGGER = logging.getLogger("moon.manager.server")
configuration.init_logging()


@hug.startup()
def add_data(api):
    """Adds initial data to the api on startup"""
    LOGGER.warning("Starting the server and initializing data")
    init_db(configuration.get_configuration("management").get("token_file"))
    db_driver.init()
    orchestration_driver.init()


def __get_status_code(exception):
    if isinstance(exception, HTTPError):
        return exception.status
    status_code = getattr(exception, "code", 500)
    if status_code in ERROR_CODE:
        status_code = ERROR_CODE[status_code]
    else:
        status_code = hug.HTTP_500
    return status_code


@hug.exception(exceptions.MoonError)
def handle_custom_exceptions(exception, response):
    response.status = __get_status_code(exception)
    error_message = {"result": False,
                     'message': str(exception),
                     "code": getattr(exception, "code", 500)}
    LOGGER.exception(exception)
    return error_message


@hug.exception(Exception)
def handle_exception(exception, response):
    response.status = __get_status_code(exception)
    LOGGER.exception(exception)
    return {"result": False, 'message': str(exception), "code": getattr(exception, "code", 500)}


@hug.extend_api()
def with_other_apis():
    return [status, logs, configuration, pdp, policy, slave, auth,
            perimeter, assignments, meta_data, meta_rules, models, json_import, json_export,
            rules, data, attributes]


@hug.static('/static')
def static_front():
    return (configuration.get_configuration("dashboard").get("root"), )
