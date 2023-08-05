#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37

from yutils.tools import check_object_type, prioritize_dicts
from yutils.exceptions import InputError, WrongDatatype
from yutils.base.attribute_dict import AttributeDict


class InputChecker(object):
    _INPUT_TYPES = {}
    _INPUT_OPTIONS = {}
    _INPUT_DEFAULTS = {}

    _INVALID_INPUT_OPTION_EXCEPTION_STR = 'Input {input} was {reality} but should be one of these options:\n{options}'

    def __init__(self, **inputs):
        """
        Base object for making a Python object more static-typed.
        It is useful for checking __init__ argument inputs (type and content).

        Type check is defined by _INPUT_TYPES class constant. (see yutils.tools.check_object_type for usage)
        Option check is defined by _INPUT_OPTIONS class constant.
        Default input options are defined by _INPUT_DEFAULTS class constant.

        This also:
            - creates self._inputs as the inputs dict given, with defaults, as an AttributeDict.
            - creates self._inputs_without_defaults as only the inputs dict given, without defaults, as an AttributeDict.
            - adds each input in inputs as an attribute to your object.
                (Including values of _INPUT_DEFAULTS if inputs aren't otherwise present)

        :param inputs: your __init__ inputs, can be anything you wish to check

        :raises: yutils.exceptions.WrongDatatype if any input is not of the specified type, defined by _INPUT_TYPES
                 yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS
        """
        self._create_attributes(inputs)
        self._check_inputs()

    def _create_attributes(self, inputs):
        """
        1. Creates self._inputs as the inputs dict given, as an AttributeDict.
        2. Adds each input in inputs as an attribute to your object.

        :param inputs: the inputs given as Keyword Arguments to __init__
        :type inputs: dict
        """
        self._inputs_without_defaults = AttributeDict(inputs)

        all_inputs = prioritize_dicts(inputs, self._INPUT_DEFAULTS)
        self._inputs = AttributeDict(all_inputs)

        for key, value in all_inputs.items():
            setattr(self, key, value)

    def _check_inputs(self):
        """
        Checks all inputs (types and contents).
        This also makes sure self._INPUT_TYPES and self._INPUT_OPTIONS are dicts, as expected.

        See yutils.tools.check_object_type for documentation on _INPUT_TYPES format and usage.

        :raises: yutils.exceptions.WrongDatatype if any input is not of the specified type, defined by _INPUT_TYPES
                 yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS

        """
        if not isinstance(self._INPUT_TYPES, dict):
            raise WrongDatatype('_INPUT_TYPES', dict, type(self._INPUT_TYPES))
        if not isinstance(self._INPUT_OPTIONS, dict):
            raise WrongDatatype('_INPUT_OPTIONS', dict, type(self._INPUT_OPTIONS))

        self._check_input_types()
        self._check_input_options()

    def _check_input_types(self):
        types_dict = {'type': InputChecker}
        types_dict.update(self._INPUT_TYPES)
        check_object_type(self, types_dict)

    def _check_input_options(self):
        """
        Uses self._INPUT_OPTIONS to make sure given inputs are in wanted options defined.

        :raises: yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS
        """
        for input_str, options in self._INPUT_OPTIONS.items():
            input_val = getattr(self, input_str)
            if input_val not in options:
                raise InputError(self._INVALID_INPUT_OPTION_EXCEPTION_STR.format(input=input_str,
                                                                                 reality=input_val,
                                                                                 options=repr(options)))
