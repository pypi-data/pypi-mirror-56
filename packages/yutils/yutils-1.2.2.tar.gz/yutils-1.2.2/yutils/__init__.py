#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37

import os

ARABIC_NLS_LANG = 'AMERICAN_AMERICA.AL32UTF8'


def match_arabic_nls_lang():
    os.environ['NLS_LANG'] = ARABIC_NLS_LANG


from yutils import base, conn, exceptions, ml, queries, tools

# All important utilities are here for easy access
from yutils.base import dict_to_generic_object, UpdatingDict, ListContainer, InputChecker
from yutils.queries import DBConnection
