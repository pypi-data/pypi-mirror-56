#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37

from yutils.exceptions import WrongDatatype, MissingInput, WrongInputDatatype, CodeMistake
from yutils.tools.list import make_list, repr_list


def check_object_type(object_to_check, types_to_validate, input_name=None):
    """
    This checks the types of an object using a certain syntax:
    Lets say we have an object_to_check and the types_to_validate.
    The object_to_check is the object

    :param object_to_check: the object you wish to check its type, and raise an exception should its type not be correct
    :type object_to_check: ....that's what we're here for....
    :param types_to_validate: defines the wanted types for the object to check:
    :type types_to_validate:
                type - checks that object_to_check is of that type
                        Example: float will make sure object_to_check is a float
                list of types - checks that object_to_check is one of the types in the list
                        Example: [int, float] will make sure object_to_check is either an int or a float
                tuple of types - checks hierarchically:
                                    checks that object_to_check is of the type of the first item,
                                    then checks that each item in object_to_check is of the type of the second item,
                                    etc.
                                 Remember, all types in the tuple except the last must support indexing.
                        Example: (list, str) will make sure object_to_check is a list of strings
                                 (tuple, [int, float]) will make sure object_to_check is a tuple of either ints or floats
                dict - checks that object_to_check is an object. It's type is defined by key 'type',
                       with other keys to be checked as the object's attributes.
                        Example: {'type': Person, 'age': int} will make sure object_to_check is a Person object,
                                 with an 'age' attribute that is an int.
                All values can have as many recursive dimensions as wanted.
    :param input_name: Do not use, this is for recursive inner use.

    More examples
    Lets say we create:

    integer = 13
    unicode_str = u'foo'
    int_list = list(range(10))
    input_object = MyObject()
    input_object.num = 3
    input_object.lis = [1, 'bar']
    input_object.3dlist = [[(1, 2, 3), (1, 1, 1)], [('a', 'b', 'c'), [7, 8, 9]]]

    We can send:
    check_object_type(integer, int)
    check_object_type(unicode_str, unicode)
    check_object_type(int_list, (list, int))
    check_object_type(input_object, {'type': MyObject,
                                     'num': int,
                                     'lis': (list, [int, str]),
                                     '3dlist': (list, list, [tuple, list], [int, str, unicode])
                                     })

    :raises:
             Because of invalid inputs:
                yutils.exceptions.CodeMistake - When no 'type' key is found (for when types_to_validate is a dict)
                yutils.exceptions.WrongDatatype - When no type type is found when isinstance-ing an object's type
             Exceptions raised by check:
                yutils.exceptions.WrongInputDatatype - When the type is not correct during validation
                yutils.exceptions.MissingInput - When an attribute is missing (for when types_to_validate is a dict)
    """
    input_name = object_to_check.__class__.__name__ if input_name is None else input_name

    if isinstance(types_to_validate, dict):
        if 'type' not in types_to_validate.keys():
            raise CodeMistake("Insert a 'type' key in the type dict for instance type check")
        _check_types_from_options(object_to_check, types_to_validate['type'], input_name)
        _check_types_from_dict(object_to_check, types_to_validate, input_name + '->')

    elif isinstance(types_to_validate, tuple):
        _check_types_from_options(object_to_check, types_to_validate[0], input_name)
        _check_types_from_tuple(object_to_check, types_to_validate[1:], input_name, 1)

    else:
        _check_types_from_options(object_to_check, types_to_validate, input_name)


def _check_types_from_dict(object_to_check, types_dict, input_name=""):
    """
    Makes sure self has inputs depending on an input dict.

    :raises: yutils.exceptions.MissingInput - When an attribute is missing (for when types_to_validate is a dict)
             For other check_object_type exceptions, see check_object_type docstring.
    """
    for attrib, types in types_dict.items():
        if attrib == 'type':
            continue
        if not hasattr(object_to_check, attrib):
            raise MissingInput(object_to_check, attrib)

        check_object_type(getattr(object_to_check, attrib), types, input_name + attrib)


def _check_types_from_tuple(object_to_check, types_tuple, input_name, level):
    """
    Recursively iterates and makes sure all iterations are of the needed type

    :raises: See check_object_type docstring
    """
    for i in range(len(object_to_check)):
        if isinstance(types_tuple[0], dict):
            _check_types_from_dict(object_to_check[i], types_tuple[0], input_name + '->dimension{}->'.format(level))
        else:
            _check_types_from_options(object_to_check[i], types_tuple[0],
                                      input_name + '->dimension{}iteration{}'.format(level, i))

        if len(types_tuple) > 1:
            _check_types_from_tuple(object_to_check[i], types_tuple[1:], input_name, level + 1)


def _check_types_from_options(object_to_check, options, input_name=""):
    """
    Checks if object is of expected type/s
    :type options: type or list of types

    :raises:
             Because of invalid inputs:
                yutils.exceptions.WrongDatatype - When no type type is found when isinstance-ing an object's type
             Exceptions raised by check:
                yutils.exceptions.WrongInputDatatype - When the type is not correct during validation
    """
    options = make_list(options)
    for option in options:
        if not isinstance(option, type):
            raise WrongDatatype(input_name + '->input_type_option', type, type(option))

    if not isinstance(object_to_check, tuple(options)):
        raise WrongInputDatatype(input_name,
                                 repr_list(option.__name__.decode() for option in options),
                                 type(object_to_check))
