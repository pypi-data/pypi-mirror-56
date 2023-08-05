# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""
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
from moon_utilities import exceptions
from moon_utilities.security_functions import validate_input
from moon_utilities.auth_functions import api_key_authentication
from moon_utilities.invalided_functions import invalidate_perimeter_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration
from moon_manager.api import policy

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Subjects(object):
    """
    Endpoint for subjects requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/subjects/", requires=api_key_authentication)
    @hug.get("/subjects/{perimeter_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/subjects/", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/subjects/{perimeter_id}", requires=api_key_authentication)
    def get(uuid: hug.types.text = None, perimeter_id: hug.types.text = None,
            authed_user: hug.directives.user = None):
        """Retrieve all subjects or a specific one if perimeter_id is
        given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param authed_user: user ID who do the request
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "a description (optional)"
            }
        }
        :internal_api: get_subjects
        """

        # data = {"policy_id": str(uuid), "perimeter_id": str(perimeter_id)}
        data = driver.PolicyManager.get_subjects(
            moon_user_id=authed_user,
            policy_id=uuid,
            perimeter_id=perimeter_id
        )
        # logger.info(db_driver.PolicyManager.get_subjects(policy_id=str(uuid)))
        return {"subjects": data}

    @staticmethod
    @hug.local()
    @hug.post("/newsubject", requires=api_key_authentication)
    @hug.post("/subjects/{perimeter_id}", requires=api_key_authentication)
    @hug.post("/policies/{uuid}/subjects/", requires=api_key_authentication)
    @hug.post("/policies/{uuid}/subjects/{perimeter_id}", requires=api_key_authentication)
    def post(body: validate_input("name"), uuid: hug.types.text = None, perimeter_id:
    hug.types.text = None, authed_user: hug.directives.user = None):
        """Create or update a subject.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the subject (mandatory)",
            "description": "description of the subject (optional)",
            "password": "password for the subject (optional)",
            "email": "email address of the subject (optional)"
        }
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject (optional)",
                    "password": "password for the subject (optional)",
                    "email": "email address of the subject (optional)"
            }
        }
        :internal_api: set_subject
        """

        if 'policy_list' in body:
            raise exceptions.PerimeterContentError("body should not contain policy_list")
        # data = {"policy_id": uuid, "perimeter_id": perimeter_id}
        data = driver.PolicyManager.add_subject(moon_user_id=authed_user,
                                                policy_id=uuid,
                                                perimeter_id=perimeter_id,
                                                value=body)

        return {"subjects": data}

    @staticmethod
    @hug.local()
    @hug.patch("/subjects/{perimeter_id}", requires=api_key_authentication)
    def patch(body, perimeter_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Create or update a subject.

        :param body: body of the request
        :param perimeter_id: must not be used here
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the subject",
            "description": "description of the subject (optional)",
            "password": "password for the subject (optional)",
            "email": "email address of the subject (optional)"
        }
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject (optional)",
                    "password": "password for the subject (optional)",
                    "email": "email address of the subject (optional)"
            }
        }
        :internal_api: set_subject
        """
        # data = {"policy_id": uuid, "perimeter_id": perimeter_id}
        data = driver.PolicyManager.update_subject(moon_user_id=authed_user,
                                                   perimeter_id=perimeter_id,
                                                   value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_perimeter_in_slaves(slaves=slaves, policy_id=None, perimeter_id=perimeter_id,
                                       type="subject", data=data[perimeter_id], is_delete=False)

        return {"subjects": data}

    @staticmethod
    @hug.local()
    @hug.delete("/subjects/", requires=api_key_authentication)
    @hug.delete("/subjects/{perimeter_id}", requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/subjects/{perimeter_id}", requires=api_key_authentication)
    def delete(uuid: hug.types.text = None, perimeter_id: hug.types.text = None,
               authed_user: hug.directives.user = None):
        """Delete a subject for a given policy

        :param uuid: uuid of the policy (mandatory if perimeter_id is not set)
        :param perimeter_id: uuid of the subject (mandatory if uuid is not set)
        :param user_id: user ID who do the request
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject (optional)",
                    "password": "password for the subject (optional)",
                    "email": "email address of the subject (optional)"
            }
        }
        :internal_api: delete_subject
        """

        # data = {"policy_id": uuid, "perimeter_id": perimeter_id}
        data = driver.PolicyManager.delete_subject(
            moon_user_id=authed_user, policy_id=uuid, perimeter_id=perimeter_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_perimeter_in_slaves(slaves=slaves, policy_id=uuid, perimeter_id=perimeter_id,
                                       type="subject" )

        return {"result": True}


class Objects(object):
    """
    Endpoint for objects requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/objects/", requires=api_key_authentication)
    @hug.get("/objects/{perimeter_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/objects/", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/objects/{perimeter_id}", requires=api_key_authentication)
    def get(uuid: hug.types.text = None, perimeter_id: hug.types.text = None,
            authed_user: hug.directives.user = None):
        """Retrieve all objects or a specific one if perimeter_id is
        given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param user_id: user ID who do the request
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: get_objects
        """

        data = driver.PolicyManager.get_objects(moon_user_id=authed_user,
                                                policy_id=uuid,
                                                perimeter_id=perimeter_id
                                                )

        return {"objects": data}

    #
    @staticmethod
    @hug.local()
    @hug.post("/newobject", requires=api_key_authentication)
    @hug.post("/objects/{perimeter_id}", requires=api_key_authentication)
    @hug.post("/policies/{uuid}/objects/", requires=api_key_authentication)
    @hug.post("/policies/{uuid}/objects/{perimeter_id}", requires=api_key_authentication)
    def post(body: validate_input("name"), uuid: hug.types.text = None, perimeter_id:
    hug.types.text = None, authed_user: hug.directives.user = None):
        """Create or update a object.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "object_name": "name of the object (mandatory)",
            "object_description": "description of the object (optional)"
        }
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: set_object
        """
        data = driver.PolicyManager.add_object(moon_user_id=authed_user,
                                               policy_id=uuid,
                                               perimeter_id=perimeter_id, value=body)

        return {"objects": data}

    @staticmethod
    @hug.local()
    @hug.patch("/objects/{perimeter_id}", requires=api_key_authentication)
    def patch(body, perimeter_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Create or update a object.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "object_name": "name of the object",
            "object_description": "description of the object (optional)"
        }
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: set_object
        """
        data = driver.PolicyManager.update_object(moon_user_id=authed_user,
                                                  perimeter_id=perimeter_id,
                                                  value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_perimeter_in_slaves(slaves=slaves, policy_id=None, perimeter_id=perimeter_id,
                                       type="object", data=data[perimeter_id], is_delete=False)

        return {"objects": data}

    @staticmethod
    @hug.local()
    @hug.delete("/objects/", requires=api_key_authentication)
    @hug.delete("/objects/{perimeter_id}", requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/objects/{perimeter_id}", requires=api_key_authentication)
    def delete(uuid: hug.types.text = None, perimeter_id: hug.types.text = None, authed_user:
    hug.directives.user = None):
        """Delete a object for a given policy

        :param uuid: uuid of the policy (mandatory if perimeter_id is not set)
        :param perimeter_id: uuid of the object (mandatory if uuid is not set)
        :param user_id: user ID who do the request
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: delete_object
        """

        data = driver.PolicyManager.delete_object(
            moon_user_id=authed_user, policy_id=uuid, perimeter_id=perimeter_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_perimeter_in_slaves(slaves=slaves, policy_id=uuid, perimeter_id=perimeter_id,
                                       type="object")

        return {"result": True}


class Actions(object):
    """
    Endpoint for actions requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/actions/", requires=api_key_authentication)
    @hug.get("/actions/{perimeter_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/actions/", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/actions/{perimeter_id}", requires=api_key_authentication)
    def get(uuid: hug.types.text = None, perimeter_id: hug.types.text = None,
            authed_user: hug.directives.user = None):
        """Retrieve all actions or a specific one if perimeter_id
        is given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param user_id: user ID who do the request
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: get_actions
        """

        data = driver.PolicyManager.get_actions(
            moon_user_id=authed_user, policy_id=uuid, perimeter_id=perimeter_id)

        return {"actions": data}

    @staticmethod
    @hug.local()
    @hug.post("/newaction", requires=api_key_authentication)
    @hug.post("/actions/{perimeter_id}", requires=api_key_authentication)
    @hug.post("/policies/{uuid}/actions/", requires=api_key_authentication)
    @hug.post("/policies/{uuid}/actions/{perimeter_id}", requires=api_key_authentication)
    def post(body: validate_input("name"), uuid: hug.types.text = None, perimeter_id:
    hug.types.text = None, authed_user: hug.directives.user = None):
        """Create or update a action.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the action (mandatory)",
            "description": "description of the action (optional)"
        }
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: set_action
        """
        data = driver.PolicyManager.add_action(
            moon_user_id=authed_user, policy_id=uuid, perimeter_id=perimeter_id, value=body)

        return {"actions": data}

    @staticmethod
    @hug.local()
    @hug.patch("/actions/{perimeter_id}", requires=api_key_authentication)
    def patch(body, perimeter_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Create or update a action.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the action",
            "description": "description of the action (optional)"
        }
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: set_action
        """
        data = driver.PolicyManager.update_action(
            moon_user_id=authed_user, perimeter_id=perimeter_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_perimeter_in_slaves(slaves=slaves, policy_id=None, perimeter_id=perimeter_id,
                                       type="action", data=data[perimeter_id], is_delete=False)

        return {"actions": data}

    @staticmethod
    @hug.local()
    @hug.delete("/actions/", requires=api_key_authentication)
    @hug.delete("/actions/{perimeter_id}", requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/actions/{perimeter_id}", requires=api_key_authentication)
    def delete(uuid: hug.types.text = None, perimeter_id: hug.types.text = None, authed_user:
    hug.directives.user = None):
        """Delete a action for a given policy

        :param uuid: uuid of the policy (mandatory if perimeter_id is not set)
        :param perimeter_id: uuid of the action (mandatory if uuid is not set)
        :param user_id: user ID who do the request
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: delete_action
        """

        data = driver.PolicyManager.delete_action(
            moon_user_id=authed_user, policy_id=uuid, perimeter_id=perimeter_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_perimeter_in_slaves(slaves=slaves, policy_id=uuid, perimeter_id=perimeter_id,
                                       type="action")

        return {"result": True}


SubjectsAPI = hug.API(name='subjects', doc=Subjects.__doc__)


def filter_dict(data, filter_args):
    for item in data:
        output = []
        for arg in filter_args:
            if arg.strip() in data.get(item):
                output.append(str(data.get(item).get(arg.strip())))
        yield output


@hug.object(name='subjects', version='1.0.0', api=SubjectsAPI)
class SubjectsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id="", filter=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _subjects_req = requests.get("{}/subjects".format(db_conf.get("url")),
                                     headers={"x-api-key": manager_api_key}
                                     )
        if _subjects_req.status_code == 200:
            if name_or_id:
                _subjects = None
                if name_or_id in _subjects_req.json().get("subjects"):
                    _subjects = _subjects_req.json().get("subjects").get(name_or_id)
                else:
                    for _subjects_key in _subjects_req.json().get("subjects"):
                        _name = _subjects_req.json().get("subjects").get(_subjects_key).get("name")
                        if _name == name_or_id:
                            _subjects = _subjects_req.json().get("subjects").get(_subjects_key)
                            name_or_id = _subjects_key
                            break
                if not _subjects:
                    raise Exception("Cannot find Subjects with name or ID {}".format(name_or_id))
                return {"subjects": [{name_or_id: _subjects}]}
            if filter:
                return "\n".join(
                    ["\t".join(_t) for _t in filter_dict(_subjects_req.json().get("subjects"),
                                                         filter.split(","))]
                )
            return _subjects_req.json()
        LOGGER.error('Cannot list Subjects {}'.format(_subjects_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description="", policy_name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _url = "{}/newsubject".format(db_conf.get("url"))
        if policy_name_or_id:
            policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
            _url = "{}/policies/{}/subjects".format(db_conf.get("url"), policy_id)
        _subjects = requests.post(
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
        if _subjects.status_code == 200:
            LOGGER.warning('Create {}'.format(_subjects.content))
            return _subjects.json()
        LOGGER.error('Cannot create {}'.format(name, _subjects.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id, policy_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _subjects = SubjectsCLI.list()
        for _perimeter_id, _perimeter_value in _subjects.get("subjects").items():
            if _perimeter_value.get("name") == name_or_id:
                _url = "{}/subjects/{}".format(db_conf.get("url"), _perimeter_id)
                if policy_name_or_id:
                    policy_id = list(
                        policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
                    _url = "{}/policies/{}/subjects/{}".format(db_conf.get("url"), policy_id,
                                                               _perimeter_id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find Subjects with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete Subjects with name {}".format(name_or_id))
        return False

    @staticmethod
    @hug.object.cli
    def update(name_or_id, description=None, extra=None, email=None, new_name=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _subjects = SubjectsCLI.list()
        for _perimeter_id, _perimeter_value in _subjects.get("subjects").items():
            if _perimeter_id == name_or_id or _perimeter_value.get("name") == name_or_id:
                updated_name = _perimeter_value.get("name")
                updated_id = _perimeter_value.get("id")
                updated_description = _perimeter_value.get("description")
                updated_extra = _perimeter_value.get("extra")
                updated_email = _perimeter_value.get("email")
                _url = "{}/subjects/{}".format(db_conf.get("url"), _perimeter_id)

                if new_name is not None:
                    updated_name = new_name
                if description is not None:
                    updated_description = description
                if extra is not None:
                    if extra == "":
                        updated_extra = {}
                    else:
                        updated_extra.update(dict((k, v) for k, v in (item.split(':') for item in extra.split(','))))
                if email is not None:
                    updated_email = email

                req = requests.patch(
                    _url,
                    json={
                        "name": updated_name,
                        "id": updated_id,
                        "description": updated_description,
                        "extra": updated_extra,
                        "email": updated_email
                    },
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find Subjects with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Updated {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot update Subjects with name {}".format(name_or_id))
        return False


ObjectsAPI = hug.API(name='objects', doc=Objects.__doc__)


@hug.object(name='objects', version='1.0.0', api=ObjectsAPI)
class ObjectsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id="", filter=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _objects_req = requests.get("{}/objects".format(db_conf.get("url")),
                                    headers={"x-api-key": manager_api_key}
                                    )
        if _objects_req.status_code == 200:
            if name_or_id:
                _objects = None
                if name_or_id in _objects_req.json().get("objects"):
                    _objects = _objects_req.json().get("objects").get(name_or_id)
                else:
                    for _objects_key in _objects_req.json().get("objects"):
                        _name = _objects_req.json().get("objects").get(_objects_key).get("name")
                        if _name == name_or_id:
                            _objects = _objects_req.json().get("objects").get(_objects_key)
                            name_or_id = _objects_key
                            break
                if not _objects:
                    raise Exception("Cannot find Objects with name or ID {}".format(name_or_id))
                return {"objects": [{name_or_id: _objects}]}
            if filter:
                return "\n".join(
                    ["\t".join(_t) for _t in filter_dict(_objects_req.json().get("objects"),
                                                         filter.split(","))]
                )
            return _objects_req.json()
        LOGGER.error('Cannot list Objects {}'.format(_objects_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description="", policy_name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _url = "{}/newobject".format(db_conf.get("url"))
        if policy_name_or_id:
            policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
            _url = "{}/policies/{}/objects".format(db_conf.get("url"), policy_id)
        _objects = requests.post(
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
        if _objects.status_code == 200:
            LOGGER.warning('Create {}'.format(_objects.content))
            return _objects.json()
        LOGGER.error('Cannot create {}'.format(name, _objects.content[:40]))

    @staticmethod
    @hug.object.cli
    def update(name_or_id, description=None, extra=None, email=None, new_name=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _objects = ObjectsCLI.list()
        for _perimeter_id, _perimeter_value in _objects.get("objects").items():
            if _perimeter_id == name_or_id or _perimeter_value.get("name") == name_or_id:
                updated_name = _perimeter_value.get("name")
                updated_id = _perimeter_value.get("id")
                updated_description = _perimeter_value.get("description")
                updated_extra = _perimeter_value.get("extra")
                updated_email = _perimeter_value.get("email")
                _url = "{}/objects/{}".format(db_conf.get("url"), _perimeter_id)

                if new_name is not None:
                    updated_name = new_name
                if description is not None:
                    updated_description = description
                if extra is not None:
                    if extra == "":
                        updated_extra = {}
                    else:
                        updated_extra.update(dict((k, v) for k, v in (item.split(':') for item in extra.split(','))))
                if email is not None:
                    updated_email = email

                req = requests.patch(
                    _url,
                    json={
                        "name": updated_name,
                        "id": updated_id,
                        "description": updated_description,
                        "extra": updated_extra,
                        "email": updated_email
                    },
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find object with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Updated {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot update object with name {}".format(name_or_id))
        return False

    @staticmethod
    @hug.object.cli
    def delete(name_or_id, policy_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _objects = ObjectsCLI.list()
        for _perimeter_id, _perimeter_value in _objects.get("objects").items():
            if _perimeter_value.get("name") == name_or_id:
                _url = "{}/objects/{}".format(db_conf.get("url"), _perimeter_id)
                if policy_name_or_id:
                    policy_id = list(
                        policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
                    _url = "{}/policies/{}/objects/{}".format(db_conf.get("url"), policy_id,
                                                               _perimeter_id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find Objects with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete Objects with name {}".format(name_or_id))
        return False


ActionsAPI = hug.API(name='actions', doc=Actions.__doc__)


@hug.object(name='actions', version='1.0.0', api=ActionsAPI)
class ActionsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id="", filter=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _actions_req = requests.get("{}/actions".format(db_conf.get("url")),
                                    headers={"x-api-key": manager_api_key}
                                    )
        if _actions_req.status_code == 200:
            if name_or_id:
                _actions = None
                if name_or_id in _actions_req.json().get("actions"):
                    _actions = _actions_req.json().get("actions").get(name_or_id)
                else:
                    for _actions_key in _actions_req.json().get("actions"):
                        _name = _actions_req.json().get("actions").get(_actions_key).get("name")
                        if _name == name_or_id:
                            _actions = _actions_req.json().get("actions").get(_actions_key)
                            name_or_id = _actions_key
                            break
                if not _actions:
                    raise Exception("Cannot find Actions with name or ID {}".format(name_or_id))
                return {"actions": [{name_or_id: _actions}]}
            if filter:
                return "\n".join(
                    ["\t".join(_t) for _t in filter_dict(_actions_req.json().get("actions"),
                                                         filter.split(","))]
                )
            return _actions_req.json()
        LOGGER.error('Cannot list Actions {}'.format(_actions_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description="", policy_name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _url = "{}/newaction".format(db_conf.get("url"))
        if policy_name_or_id:
            policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
            _url = "{}/policies/{}/actions".format(db_conf.get("url"), policy_id)
        _actions = requests.post(
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
        if _actions.status_code == 200:
            LOGGER.warning('Create {}'.format(_actions.content))
            return _actions.json()
        LOGGER.error('Cannot create {}'.format(name, _actions.content[:40]))

    @staticmethod
    @hug.object.cli
    def update(name_or_id, description=None, extra=None, email=None, new_name=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _actions = ActionsCLI.list()
        for _perimeter_id, _perimeter_value in _actions.get("actions").items():
            if _perimeter_id == name_or_id or _perimeter_value.get("name") == name_or_id:
                updated_name = _perimeter_value.get("name")
                updated_id = _perimeter_value.get("id")
                updated_description = _perimeter_value.get("description")
                updated_extra = _perimeter_value.get("extra")
                updated_email = _perimeter_value.get("email")
                _url = "{}/actions/{}".format(db_conf.get("url"), _perimeter_id)

                if new_name is not None:
                    updated_name = new_name
                if description is not None:
                    updated_description = description
                if extra is not None:
                    if extra == "":
                        updated_extra = {}
                    else:
                        updated_extra.update(dict((k, v) for k, v in (item.split(':') for item in extra.split(','))))
                if email is not None:
                    updated_email = email

                req = requests.patch(
                    _url,
                    json={
                        "name": updated_name,
                        "id": updated_id,
                        "description": updated_description,
                        "extra": updated_extra,
                        "email": updated_email
                    },
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find action with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Updated {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot update action with name {}".format(name_or_id))
        return False

    @staticmethod
    @hug.object.cli
    def delete(name_or_id, policy_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _actions = ActionsCLI.list()
        for _perimeter_id, _perimeter_value in _actions.get("actions").items():
            if _perimeter_value.get("name") == name_or_id:
                _url = "{}/actions/{}".format(db_conf.get("url"), _perimeter_id)
                if policy_name_or_id:
                    policy_id = list(
                        policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
                    _url = "{}/policies/{}/actions/{}".format(db_conf.get("url"), policy_id,
                                                               _perimeter_id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find Actions with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete Actions with name {}".format(name_or_id))
        return False
