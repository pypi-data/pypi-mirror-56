import os
from enum import Enum

PROGRAM_NAME = 'conapp'


DEFAULT_STRIP_COMPONENTS = '--strip-components=1'


USER_HOME_DIR = os.path.expanduser('~')


class Hosts(Enum):
    BITBUCKET = 'B'
    GITHUB = 'G'
