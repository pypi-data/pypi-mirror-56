# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Rules
"""

import hug
import json
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_utilities.invalided_functions import invalidate_rules_in_slaves
from moon_manager.api import configuration
from moon_utilities.auth_functions import init_db, api_key_authentication
from moon_manager.api import slave as slave_class
from moon_manager.api import policy, meta_rules, data

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Rules(object):
    """
    Endpoint for rules requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/rules", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/rules/{rule_id}", requires=api_key_authentication)
    def get(uuid: hug.types.text, rule_id: hug.types.text = None, moon_user_id=None):
        """Retrieve all rules or a specific one

        :param uuid: policy ID
        :param rule_id: rule ID
        :param moon_user_id: user ID who do the request
        :return: {
            "rules": [
                "policy_id": "policy_id1",
                "meta_rule_id": "meta_rule_id1",
                "rule_id1":
                    ["subject_data_id1", "subject_data_id2", "object_data_id1", "action_data_id1"],
                "rule_id2":
                    ["subject_data_id3", "subject_data_id4", "object_data_id2", "action_data_id2"],
            ]
        }
        :internal_api: get_rules
        """

        data = driver.PolicyManager.get_rules(moon_user_id=moon_user_id, policy_id=uuid,
                                              rule_id=rule_id)

        return {"rules": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/rules", requires=api_key_authentication)
    def post(body: validate_input("meta_rule_id", "rule", "instructions"),
             uuid: hug.types.text,
             moon_user_id=None):
        """Add a rule to a meta rule

        :param uuid: policy ID
        :param body: body of the request
        :param moon_user_id: user ID who do the request
        :request body: post = {
            "meta_rule_id": "meta_rule_id1",  # mandatory
            "rule": ["subject_data_id2", "object_data_id2", "action_data_id2"],  # mandatory
            "instructions": [  # mandatory
                {"decision": "grant"},
            ]
            "enabled": True
        }
        :return: {
            "rules": [
                "meta_rule_id": "meta_rule_id1",
                "rule_id1": {
                    "rule": ["subject_data_id1",
                             "object_data_id1",
                             "action_data_id1"],
                    "instructions": [
                        {"decision": "grant"},
                        # "grant" to immediately exit,
                        # "continue" to wait for the result of next policy
                        # "deny" to deny the request
                    ]
                }
                "rule_id2": {
                    "rule": ["subject_data_id2",
                             "object_data_id2",
                             "action_data_id2"],
                    "instructions": [
                        {
                            "update": {
                                "operation": "add",
                                    # operations may be "add" or "delete"
                                "target": "rbac:role:admin"
                                    # add the role admin to the current user
                            }
                        },
                        {"chain": {"name": "rbac"}}
                            # chain with the policy named rbac
                    ]
                }
            ]
        }
        :internal_api: add_rule
        """
        data = driver.PolicyManager.add_rule(moon_user_id=moon_user_id, policy_id=uuid,
                                             meta_rule_id=body['meta_rule_id'], value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_rules_in_slaves(slaves=slaves, policy_id=uuid, rule_id=None)

        return {"rules": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/rules/{rule_id}", requires=api_key_authentication)
    def delete(uuid: hug.types.text, rule_id: hug.types.text, moon_user_id=None):
        """Delete one rule linked to a specific sub meta rule

        :param uuid: policy ID
        :param rule_id: rule ID
        :param moon_user_id: user ID who do the request
        :return: { "result": true }
        :internal_api: delete_rule
        """

        driver.PolicyManager.delete_rule(
            moon_user_id=moon_user_id, policy_id=uuid, rule_id=rule_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_rules_in_slaves(slaves=slaves, policy_id=uuid, rule_id=rule_id)

        return {"result": True}


RulesAPI = hug.API(name='rules', doc=Rules.__doc__)
db_conf = configuration.get_configuration(key='management')
init_db(db_conf.get("token_file"))


@hug.object(name='rules', version='1.0.0', api=RulesAPI)
class RulesCLI(object):
    """An example of command like calls via an Object"""

    __global_data = None

    @staticmethod
    def get_data_name(rule_data, policy_id):
        if not RulesCLI.__global_data:
            RulesCLI.__global_data = data.SubjectDataCLI.list(policy_id).get("subject_data") + \
                                     data.ObjectDataCLI.list(policy_id).get("object_data") + \
                                     data.ActionDataCLI.list(policy_id).get("action_data")
        _rule_names = list()
        for rule_id in rule_data:
            for _data in RulesCLI.__global_data:
                if rule_id in _data.get("data"):
                    _rule_names.append(_data.get("data")[rule_id].get("name"))
                    break
            else:
                _rule_names.append(rule_id)
        return _rule_names

    @staticmethod
    def get_data_id(rule_data, policy_id):
        _global_data = data.SubjectDataCLI.list(policy_id).get("subject_data") + \
                       data.ObjectDataCLI.list(policy_id).get("object_data") + \
                       data.ActionDataCLI.list(policy_id).get("action_data")
        _rule_ids = list()
        for rule_id_or_name in rule_data:
            _id = None
            for _data in _global_data:
                if rule_id_or_name in _data.get("data"):
                    _id = _data.get("data")[rule_id_or_name].get("name")
                    break
                else:
                    for _data_key in _data.get("data"):
                        if _data.get("data")[_data_key]['name'] == rule_id_or_name:
                            _id = _data_key
                            break
                if _id:
                    _rule_ids.append(_id)
                    break
            else:
                raise Exception("Cannot find data for {}".format(rule_id_or_name))
        return _rule_ids

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, human: bool = False, instructions: bool = False):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _rules = requests.get("{}/policies/{}/rules".format(db_conf.get("url"), policy_id),
                              headers={"x-api-key": manager_api_key}
                              )
        if _rules.status_code == 200:
            if human:
                for value in _rules.json().get("rules", {}).get("rules"):
                    if value.get("enabled"):
                        _rule_names = RulesCLI.get_data_name(value.get("rule"), policy_id)
                        output = value.get("id") + " | "
                        output += "{:30}".format(" ".join(_rule_names))
                        if instructions:
                            output += " " + json.dumps(value.get("instructions"))
                        print(output)
            else:
                return _rules.json()
        else:
            raise Exception("Got a {} response ({})".format(_rules.status_code, _rules.text))

    @staticmethod
    @hug.object.cli
    def add(policy_name_or_id, meta_rule_id_or_name, rule_items, instructions=None, enabled: bool = True):
        if not instructions:
            instructions = [{'decision': 'grant'}]
        rules_list = []
        for item in rule_items.split(","):
            rules_list.append(item.strip())
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        meta_rule_id = list(meta_rules.MetaRulesCLI.list(meta_rule_id_or_name).
                            get("meta_rules").keys())[0]

        _rules = requests.post("{}/policies/{}/rules".format(db_conf.get("url"), policy_id),
                               headers={"x-api-key": manager_api_key},
                               json={
                                    "meta_rule_id": meta_rule_id,
                                    "rule": RulesCLI.get_data_id(rules_list, policy_id),
                                    "instructions": instructions,
                                    "enabled": enabled
                               })
        if _rules.status_code == 200:
            return _rules.json()
        else:
            raise Exception("Got a {} response ({})".format(_rules.status_code, _rules.text))

    @staticmethod
    @hug.object.cli
    def delete(policy_name_or_id, rule_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]

        _rules = requests.delete("{}/policies/{}/rules/{}".format(
            db_conf.get("url"), policy_id, rule_id),
                               headers={"x-api-key": manager_api_key})
        if _rules.status_code == 200:
            return _rules.json()
        else:
            raise Exception("Got a {} response ({})".format(_rules.status_code, _rules.text))
