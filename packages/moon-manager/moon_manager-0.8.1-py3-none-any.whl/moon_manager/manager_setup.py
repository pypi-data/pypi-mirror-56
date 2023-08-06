# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
This file is used only once to install the manager
"""

import os
import shutil


def setup():
    """Setup the manager

    :return: nothing
    """
    if os.name == "posix":
        if not os.path.exists(os.path.join("/etc", "moon")):
            print("Installing configuration file in /etc")
            shutil.move("/usr/local/moon", os.path.join("/etc"))
        else:
            raise NotImplementedError('You should install configuration file somewhere '
                                      'on your system')