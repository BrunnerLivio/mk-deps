"""
Module for ExitStatus which get returned
by the program usign sys.exit()
"""
from enum import IntEnum


class ExitStatus(IntEnum):
    """
    Enumerator for possible ExitStatus of mk-deps
    """
    SUCCESS = 0
    UNABLE_TO_INSTALL = 1
    NOT_FOUND = 2
