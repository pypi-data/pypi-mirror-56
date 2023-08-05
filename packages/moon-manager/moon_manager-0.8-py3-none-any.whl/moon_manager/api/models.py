# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Models aggregate multiple meta rules
"""

import hug
import json
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_utilities.auth_functions import api_key_authentication
from moon_utilities.invalided_functions import invalidate_model_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration


LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Models(object):
    """
    Endpoint for model requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/models", requires=api_key_authentication)
    @hug.get("/models/{model_id}", requires=api_key_authentication)
    def get(model_id: hug.types.text = None, moon_user_id=None):
        """Retrieve all models

        :param model_id: uuid of the model
        :param moon_user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "...",
                "description": "... (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: get_models
        """
        data = driver.ModelManager.get_models(moon_user_id=moon_user_id, model_id=model_id)
        return {"models": data}

    @staticmethod
    @hug.local()
    @hug.post("/models", requires=api_key_authentication)
    def post(body: validate_input("name"), moon_user_id=None):
        """Create model.

        :param body: body of the request
        :param moon_user_id: user ID who do the request
        :request body: {
            "name": "name of the model (mandatory)",
            "description": "description of the model (optional)",
            "meta_rules": ["meta_rule_id1", ]
        }
        :return: {
            "model_id1": {
                "name": "name of the model",
                "description": "description of the model (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: add_model
        """
        data = driver.ModelManager.add_model(
            moon_user_id=moon_user_id, value=body)

        return {"models": data}

    @staticmethod
    @hug.local()
    @hug.delete("/models/{model_id}", requires=api_key_authentication)
    def delete(model_id: hug.types.text, moon_user_id=None):
        """Delete a model

        :param model_id: uuid of the model to delete
        :param moon_user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_model
        """

        driver.ModelManager.delete_model(moon_user_id=moon_user_id, model_id=model_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_model_in_slaves(slaves=slaves, model_id=model_id)

        return {"result": True}

    @staticmethod
    @hug.local()
    @hug.patch("/models/{model_id}", requires=api_key_authentication)
    def patch(body: validate_input("name"), model_id: hug.types.text, moon_user_id=None):
        """Update a model

        :param body: body of the request
        :param model_id: uuid of the model to update
        :param moon_user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "name of the model",
                "description": "... (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: update_model
        """
        data = driver.ModelManager.update_model(
            moon_user_id=moon_user_id, model_id=model_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_model_in_slaves(slaves=slaves, model_id=model_id, is_delete=False,
                                   data=data[model_id])

        return {"models": data}


ModelsAPI = hug.API(name='models', doc=Models.__doc__)


@hug.object(name='models', version='1.0.0', api=ModelsAPI)
class ModelsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _models = requests.get("{}/models".format(db_conf.get("url")),
                               headers={"x-api-key": manager_api_key}
                               )
        if name_or_id:
            if name_or_id in _models.json().get("models"):
                return {"models": [{name_or_id: _models.json().get("models").get(name_or_id)}]}
            else:
                for _model_id in _models.json().get("models"):
                    if _models.json().get("models").get(_model_id).get("name") == name_or_id:
                        return {"models": [
                            {_model_id: _models.json().get("models").get(_model_id)}]}
            raise Exception("Cannot find model with name or ID {}".format(name_or_id))
        if _models.status_code == 200:
            return _models.json()

    @staticmethod
    @hug.object.cli
    def add(name='default', address="local", description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _models = requests.post(
            "{}/models".format(db_conf.get("url")),
            json={
                "name": name,
                "address": address,
                "description": description
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _models.status_code == 200:
            LOGGER.warning('Create {}'.format(_models.content))
            return _models.json()
        LOGGER.error('Cannot create {}'.format(name, _models.content))

    @staticmethod
    @hug.object.cli
    def delete(name='default'):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _models = ModelsCLI.list()
        for _slave_id, _slave_value in _models.get("models").items():
            if _slave_value.get("name") == name:
                req = requests.delete(
                    "{}/models/{}".format(db_conf.get("url"), _slave_id),
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find model with name {}".format(name))
            return
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name))
            return True
        LOGGER.error("Cannot delete model with name {}".format(name))
