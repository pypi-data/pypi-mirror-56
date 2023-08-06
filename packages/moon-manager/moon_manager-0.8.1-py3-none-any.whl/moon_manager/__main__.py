# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
import sys
import os
import subprocess  # nosec
from moon_utilities import auth_functions
from moon_manager.api import configuration
from moon_utilities.auth_functions import init_db
from moon_manager import daemon
import hug.interface

LOGGER = logging.getLogger("moon.manager")
configuration.init_logging()

_conf = configuration.get_configuration()
_conf["logging"]["loggers"]["moon"]["level"] = "WARNING"
configuration.set_configuration(_conf)


@hug.cli("start_manager")
def start_manager():
    """ start the manager """
    pid_filename = _conf["management"]["pid_file"]
    _command = ["gunicorn", "moon_manager.server:__hug_wsgi__", "--threads", "5",
                "--bind", "0.0.0.0:8000", "-D", "-p", pid_filename]
    subprocess.Popen(_command, stdout=subprocess.PIPE, close_fds=True)  # nosec


@hug.cli("stop_manager")
def stop_manager():
    """ stop the manager """
    pid_filename = _conf["management"]["pid_file"]
    with open(pid_filename, 'r') as pid_file:
        try:
            pid = int(pid_file.read())
        except ValueError:
            LOGGER.error("The pid found in {} is not valid".format(pid_filename))
            return

    os.kill(pid, 15)


@hug.cli("start_all")
def start_all():
    """ start the manager and the auto-update service """
    start_manager()
    daemon.run()


@hug.cli("stop_all")
def stop_all():
    """ stop the manager and the auto-update service """
    stop_manager()
    daemon.stop()


def run(command=None):
    if len(sys.argv) > 1:
        if not command:
            command = sys.argv[1]
        # Note: delete the command argument because Hug CLI system read it
        sys.argv.pop(1)
        init_db(configuration.get_configuration("management").get("token_file"))

        if command == "conf":
            configuration.get_configuration.interface.cli()
        elif command == "db":
            configuration.init_database.interface.cli()
        elif command == "start_manager":
            start_manager.interface.cli()
        elif command == "stop_manager":
            stop_manager.interface.cli()
        elif command == "start_daemon":
            daemon.run.interface.cli()
        elif command == "stop_daemon":
            daemon.stop.interface.cli()
        elif command == "start_all":
            start_all.interface.cli()
        elif command == "stop_all":
            stop_all.interface.cli()
        elif command == "users":
            from moon_manager.api import users
            users.UsersAPI.cli()
        elif command == "import":
            configuration.import_json.interface.cli()
        elif command == "slaves":
            from moon_manager.api import slave
            slave.SlavesAPI.cli()
        elif command == "status":
            from moon_manager.api import status
            status.status.interface.cli()
        elif command == "models":
            from moon_manager.api import models
            models.ModelsAPI.cli()
        elif command == "pdp":
            from moon_manager.api import pdp
            pdp.PDPAPI.cli()
        elif command == "policies":
            from moon_manager.api import policy
            policy.PoliciesAPI.cli()
        elif command == "subjects":
            from moon_manager.api import perimeter
            perimeter.SubjectsAPI.cli()
        elif command == "objects":
            from moon_manager.api import perimeter
            perimeter.ObjectsAPI.cli()
        elif command == "actions":
            from moon_manager.api import perimeter
            perimeter.ActionsAPI.cli()
        elif command == "subject_categories":
            from moon_manager.api import meta_data
            meta_data.SubjectCategoriesAPI.cli()
        elif command == "object_categories":
            from moon_manager.api import meta_data
            meta_data.ObjectCategoriesAPI.cli()
        elif command == "action_categories":
            from moon_manager.api import meta_data
            meta_data.ActionCategoriesAPI.cli()
        elif command == "subject_data":
            from moon_manager.api import data
            data.SubjectDataAPI.cli()
        elif command == "object_data":
            from moon_manager.api import data
            data.ObjectDataAPI.cli()
        elif command == "action_data":
            from moon_manager.api import data
            data.ActionDataAPI.cli()
        elif command == "subject_assignments":
            from moon_manager.api import assignments
            assignments.SubjectAssignmentsAPI.cli()
        elif command == "object_assignments":
            from moon_manager.api import assignments
            assignments.ObjectAssignmentsAPI.cli()
        elif command == "action_assignments":
            from moon_manager.api import assignments
            assignments.ActionAssignmentsAPI.cli()
        elif command == "meta_rules":
            from moon_manager.api import meta_rules
            meta_rules.MetaRulesAPI.cli()
        elif command == "rules":
            from moon_manager.api import rules
            rules.RulesAPI.cli()
        elif command == "tests":
            from moon_manager.api import checks
            checks.ChecksAPI.cli()
        elif command == "attrs":
            from moon_manager.api import attributes
            attributes.AttrsAPI.cli()
        else:
            LOGGER.critical("Unknown command {}".format(command))
    else:
        # TODO: update the command management by using argparse
        print("""Possible commands are:
        - conf
        - db
        - start
        - stop
        - start_daemon
        - stop_daemon
        - start_all
        - stop_all
        - users
        - import
        - slaves
        - models
        - pdp
        - policies
        - subject_data
        - object_data
        - action_data
        - subjects
        - objects
        - actions
        - subject_categories
        - object_categories
        - action_categories
        - meta_rules
        - tests
        - attrs
        """)


if __name__ == "__main__":
    run()
