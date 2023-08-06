# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""
Meta Data are elements used to create Meta data (skeleton of security policies)subject_categories
* Subjects are the source of an action on an object
  (examples : users, virtual machines)
* Objects are the destination of an action
  (examples virtual machines, virtual Routers)
* Actions are what subject wants to do on an object
"""

import hug
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_utilities.auth_functions import api_key_authentication
from moon_utilities.invalided_functions import invalidate_meta_data_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration

# from moon_manager.server import handle_exception, handle_custom_exceptions

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class SubjectCategories(object):
    """
    Endpoint for subject categories requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/subject_categories", requires=api_key_authentication)
    @hug.get("/subject_categories/{category_id}", requires=api_key_authentication)
    def get(category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all subject categories or a specific one

        :param category_id: uuid of the subject category
        :param authed_user: user ID who do the request
        :return: {
            "subject_category_id": {
                "name": "name of the category",
                "description": "description of the category (optional)"
            }
        }
        :internal_api: get_subject_categories
        """
        data = driver.ModelManager.get_subject_categories(moon_user_id=authed_user,
                                                          category_id=category_id)

        return {"subject_categories": data}

    @staticmethod
    @hug.local()
    @hug.post("/subject_categories", requires=api_key_authentication)
    def post(body: validate_input("name"), authed_user: hug.directives.user = None):
        """Create or update a subject category.

        :param body: body of the request
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the category (mandatory)",
            "description": "description of the category (optional)"
        }
        :return: {
            "subject_category_id": {
                "name": "name of the category",
                "description": "description of the category (optional)"
            }
        }
        :internal_api: add_subject_category
        """
        data = driver.ModelManager.add_subject_category(moon_user_id=authed_user, value=body)


        return {"subject_categories": data}

    @staticmethod
    @hug.local()
    @hug.delete("/subject_categories/{category_id}", requires=api_key_authentication)
    def delete(category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete a subject category

        :param category_id: uuid of the subject category to delete
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_subject_category
        """

        driver.ModelManager.delete_subject_category(moon_user_id=authed_user,
                                                    category_id=category_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_meta_data_in_slaves(slaves=slaves, category_id=category_id, type='subject')

        return {"result": True}


class ObjectCategories(object):
    """
    Endpoint for object categories requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/object_categories", requires=api_key_authentication)
    @hug.get("/object_categories/{category_id}", requires=api_key_authentication)
    def get(category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all object categories or a specific one

        :param category_id: uuid of the object category
        :param authed_user: user ID who do the request
        :return: {
            "object_category_id": {
                "name": "name of the category",
                "description": "description of the category (optional)"
            }
        }
        :internal_api: get_object_categories
        """
        data = driver.ModelManager.get_object_categories(moon_user_id=authed_user,
                                                         category_id=category_id)

        return {"object_categories": data}

    @staticmethod
    @hug.local()
    @hug.post("/object_categories", requires=api_key_authentication)
    def post(body: validate_input("name"), authed_user: hug.directives.user = None):
        """Create or update a object category.

        :param body: body of the request
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the category (mandatory)",
            "description": "description of the category (optional)"
        }
        :return: {
            "object_category_id": {
                "name": "name of the category",
                "description": "description of the category (optional)"
            }
        }
        :internal_api: add_object_category
        """
        data = driver.ModelManager.add_object_category(moon_user_id=authed_user, value=body)

        return {"object_categories": data}

    @staticmethod
    @hug.local()
    @hug.delete("/object_categories/{category_id}", requires=api_key_authentication)
    def delete(category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete an object category

        :param category_id: uuid of the object category to delete
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_object_category
        """

        driver.ModelManager.delete_object_category(moon_user_id=authed_user,
                                                   category_id=category_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_meta_data_in_slaves(slaves=slaves, category_id=category_id, type='object')

        return {"result": True}


class ActionCategories(object):
    """
    Endpoint for action categories requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/action_categories", requires=api_key_authentication)
    @hug.get("/action_categories/{category_id}", requires=api_key_authentication)
    def get(category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all action categories or a specific one

        :param category_id: uuid of the action category
        :param authed_user: user ID who do the request
        :return: {
            "action_category_id": {
                "name": "name of the category",
                "description": "description of the category (optional)"
            }
        }
        :internal_api: get_action_categories
        """
        data = driver.ModelManager.get_action_categories(moon_user_id=authed_user,
                                                         category_id=category_id)
        return {"action_categories": data}

    @staticmethod
    @hug.local()
    @hug.post("/action_categories", requires=api_key_authentication)
    def post(body: validate_input("name"), authed_user: hug.directives.user = None):
        """Create or update an action category.

        :param body: body of the request
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the category (mandatory)",
            "description": "description of the category (optional)"
        }
        :return: {
            "action_category_id": {
                "name": "name of the category",
                "description": "description of the category (optional)"
            }
        }
        :internal_api: add_action_category
        """

        data = driver.ModelManager.add_action_category(moon_user_id=authed_user, value=body)

        return {"action_categories": data}

    @staticmethod
    @hug.local()
    @hug.delete("/action_categories/{category_id}", requires=api_key_authentication)
    def delete(category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete an action

        :param category_id: uuid of the action category to delete
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_action_category
        """
        driver.ModelManager.delete_action_category(moon_user_id=authed_user,
                                                   category_id=category_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_meta_data_in_slaves(slaves=slaves, category_id=category_id, type='action')

        return {"result": True}


SubjectCategoriesAPI = hug.API(name='subject_categories', doc=SubjectCategories.__doc__)


@hug.object(name='subject_categories', version='1.0.0', api=SubjectCategoriesAPI)
class SubjectCategoriesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _subject_categories_req = requests.get("{}/subject_categories".format(db_conf.get("url")),
                                               headers={"x-api-key": manager_api_key}
                                               )
        if _subject_categories_req.status_code == 200:
            if name_or_id:
                _subject_categories = None
                if name_or_id in _subject_categories_req.json().get("subject_categories"):
                    _subject_categories = _subject_categories_req.json().get("subject_categories")\
                        .get(name_or_id)
                else:
                    for _subject_categories_key in _subject_categories_req.json()\
                            .get("subject_categories"):
                        _name = _subject_categories_req.json().get("subject_categories")\
                            .get(_subject_categories_key).get("name")
                        if _name == name_or_id:
                            _subject_categories = _subject_categories_req.json()\
                                .get("subject_categories").get(_subject_categories_key)
                            name_or_id = _subject_categories_key
                            break
                if not _subject_categories:
                    raise Exception("Cannot find SubjectCategories with name or ID {}".format(
                        name_or_id))
                return {"subject_categories": {name_or_id: _subject_categories}}
            return _subject_categories_req.json()
        LOGGER.error('Cannot list SubjectCategories {}'.format(_subject_categories_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _url = "{}/subject_categories".format(db_conf.get("url"))
        _subject_categories = requests.post(
            _url,
            json={
                "name": name,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _subject_categories.status_code == 200:
            LOGGER.warning('Create {}'.format(_subject_categories.content))
            return _subject_categories.json()
        LOGGER.error('Cannot create {}'.format(name, _subject_categories.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _subject_categories = SubjectCategoriesCLI.list()
        for _perimeter_id, _perimeter_value in _subject_categories.get("subject_categories")\
                .items():
            if _perimeter_value.get("name") == name_or_id:
                _url = "{}/subject_categories/{}".format(db_conf.get("url"), _perimeter_id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find SubjectCategories with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete SubjectCategories with name {}".format(name_or_id))
        return False


ObjectCategoriesAPI = hug.API(name='object_categories', doc=ObjectCategories.__doc__)


@hug.object(name='object_categories', version='1.0.0', api=ObjectCategoriesAPI)
class ObjectCategoriesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _object_categories_req = requests.get("{}/object_categories".format(db_conf.get("url")),
                                              headers={"x-api-key": manager_api_key}
                                              )
        if _object_categories_req.status_code == 200:
            if name_or_id:
                _object_categories = None
                if name_or_id in _object_categories_req.json().get("object_categories"):
                    _object_categories = _object_categories_req.json().get("object_categories")\
                        .get(name_or_id)
                else:
                    for _object_categories_key in _object_categories_req.json()\
                            .get("object_categories"):
                        _name = _object_categories_req.json().get("object_categories")\
                            .get(_object_categories_key).get("name")
                        if _name == name_or_id:
                            _object_categories = _object_categories_req.json()\
                                .get("object_categories").get(_object_categories_key)
                            name_or_id = _object_categories_key
                            break
                if not _object_categories:
                    raise Exception("Cannot find ObjectCategories with name or ID {}".format(
                        name_or_id))
                return {"object_categories": {name_or_id: _object_categories}}
            return _object_categories_req.json()
        LOGGER.error('Cannot list ObjectCategories {}'.format(_object_categories_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _url = "{}/object_categories".format(db_conf.get("url"))
        _object_categories = requests.post(
            _url,
            json={
                "name": name,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _object_categories.status_code == 200:
            LOGGER.warning('Create {}'.format(_object_categories.content))
            return _object_categories.json()
        LOGGER.error('Cannot create {}'.format(name, _object_categories.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _object_categories = ObjectCategoriesCLI.list()
        for _perimeter_id, _perimeter_value in _object_categories.get("object_categories").items():
            if _perimeter_value.get("name") == name_or_id:
                _url = "{}/object_categories/{}".format(db_conf.get("url"), _perimeter_id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find ObjectCategories with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete ObjectCategories with name {}".format(name_or_id))
        return False


ActionCategoriesAPI = hug.API(name='action_categories', doc=ActionCategories.__doc__)


@hug.object(name='action_categories', version='1.0.0', api=ActionCategoriesAPI)
class ActionCategoriesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _action_categories_req = requests.get("{}/action_categories".format(db_conf.get("url")),
                                              headers={"x-api-key": manager_api_key}
                                              )
        if _action_categories_req.status_code == 200:
            if name_or_id:
                _action_categories = None
                if name_or_id in _action_categories_req.json().get("action_categories"):
                    _action_categories = _action_categories_req.json().get("action_categories")\
                        .get(name_or_id)
                else:
                    for _action_categories_key in _action_categories_req.json()\
                            .get("action_categories"):
                        _name = _action_categories_req.json().get("action_categories")\
                            .get(_action_categories_key).get("name")
                        if _name == name_or_id:
                            _action_categories = _action_categories_req.json()\
                                .get("action_categories").get(_action_categories_key)
                            name_or_id = _action_categories_key
                            break
                if not _action_categories:
                    raise Exception("Cannot find ActionCategories with name or ID {}".format(
                        name_or_id))
                return {"action_categories": {name_or_id: _action_categories}}
            return _action_categories_req.json()
        LOGGER.error('Cannot list ActionCategories {}'.format(_action_categories_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _url = "{}/action_categories".format(db_conf.get("url"))
        _action_categories = requests.post(
            _url,
            json={
                "name": name,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _action_categories.status_code == 200:
            LOGGER.warning('Create {}'.format(_action_categories.content))
            return _action_categories.json()
        LOGGER.error('Cannot create {}'.format(name, _action_categories.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _action_categories = ActionCategoriesCLI.list()
        for _perimeter_id, _perimeter_value in _action_categories.get("action_categories").items():
            if _perimeter_value.get("name") == name_or_id:
                _url = "{}/action_categories/{}".format(db_conf.get("url"), _perimeter_id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find ActionCategories with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete ActionCategories with name {}".format(name_or_id))
        return False
