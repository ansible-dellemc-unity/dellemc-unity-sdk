#!/usr/bin/python

__author__ = "Vadim Sychev"
__collaborations__ = ["Andrew Petrov"]

from dellemc_unity_sdk import constants
from enum import Enum
from dellemc_unity_sdk.supportive_functions import check_type
from dellemc_unity_sdk.supportive_functions import get_type

default = {constants.PARAMETER_REQUIRED: False,
           constants.PARAMETER_DEFAULT: None,
           constants.PARAMETER_TYPE: None}

_reply = {constants.VALIDATOR_RESULT: True,
          constants.VALIDATOR_MESSAGE: ''}


def _set_result(result):
    _reply[constants.VALIDATOR_RESULT] = result


def _set_message(message):
    _reply[constants.VALIDATOR_MESSAGE] = message


def _check_required_parameters(dictionary_of_params, required_params):
    result = ''
    for element in required_params:
        if not dictionary_of_params.get(element):
            result += '{}, '.format(element)
    result = result[:-2]
    return result


def _check_optional_parameters(dictionary_of_params, required_parameters, optional_parameters):
    result = ''
    for element in dictionary_of_params.keys():
        if not ((element in required_parameters) or (element in optional_parameters)):
            result += '{}, '.format(element)
    result = result[:-2]
    return result


def _check_dict_params(dictionary_of_params, params):
    result = ''
    for key in params:
        if key not in dictionary_of_params:
            if params[key].get(constants.PARAMETER_DEFAULT) is not None:
                dictionary_of_params[key] = params[key][constants.PARAMETER_DEFAULT]
            elif params[key][constants.PARAMETER_REQUIRED] is True:
                result += '{}, '.format(key)
    if result:
        message = constants.ERR_MISSING_REQUIRED_PARAMETERS.format(result[:-2])
        return message

    for key in dictionary_of_params:
        if key not in params:
            result += '{}, '.format(key)
    if result:
        message = constants.ERR_UNSUPPORTED_PARAMETERS.format(result[:-2])
        return message

    for key in dictionary_of_params:
        if params[key][constants.PARAMETER_TYPE] is not None:
            if not check_type(dictionary_of_params.get(key), params[key][constants.PARAMETER_TYPE]):
                required_type_name = params[key][constants.PARAMETER_TYPE].__name__
                type_name = get_type(dictionary_of_params.get(key))
                message = constants.ERR_WRONG_TYPE.format(key, required_type_name, type_name)
                return message
    return result


def _set_default(param_types):
    for element in param_types:
        for key in default:
            if param_types[element].get(key) is None:
                param_types[element][key] = default[key]


def _set_enum_value(params, params_types):
    for key in params:
        element_types = params_types.get(key)
        if element_types is not None:
            required_type = element_types.get(constants.PARAMETER_TYPE)
            if (required_type is not None) and (issubclass(required_type, Enum)):
                element = params[key]
                enum_list = list(map(int, required_type))
                if str(element).upper() in required_type.__members__.keys():
                    params[key] = params_types[key][constants.PARAMETER_TYPE][element.upper()].value
                    params_types[key][constants.PARAMETER_TYPE] = int
                elif element in enum_list:
                    params_types[key][constants.PARAMETER_TYPE] = int


def check_parameters(dictionary_of_params, param_types):
    """
    Check parameters and return reply
    :param dictionary_of_params: is a dictionary of parameters from playbook
    :param param_types: is a dictionary of supported parameters from ansible module
    :return: _reply is a dictionary with keys: constants.VALIDATOR_RESULT
    and constants.VALIDATOR_MESSAGE
    constants.VALIDATOR_RESULT is True if the parameters are correct
    constants.VALIDATOR_MESSAGE contains '' if the parameters are correct, else contains error message
    """
    _set_result(True)
    _set_message('')
    if (param_types.get(constants.PARAMETER_REQUIRED) is not None) or \
            (param_types.get(constants.PARAMETER_OPTIONAL) is not None):

        list_of_required = param_types.get(constants.PARAMETER_REQUIRED)
        if not list_of_required:
            list_of_required = {}
        result = _check_required_parameters(dictionary_of_params, list_of_required)
        if result:
            _set_result(False)
            _set_message(constants.ERR_MISSING_REQUIRED_PARAMETERS.format(result))
            return _reply

        list_of_optional = param_types.get(constants.PARAMETER_OPTIONAL)
        if not list_of_optional:
            list_of_optional = {}
        result = _check_optional_parameters(dictionary_of_params, list_of_required, list_of_optional)
        if result:
            _set_result(False)
            _set_message(constants.ERR_UNSUPPORTED_PARAMETERS.format(result))
            return _reply
        return _reply
    else:
        _set_default(param_types)
        _set_enum_value(dictionary_of_params, param_types)
        result = _check_dict_params(dictionary_of_params, param_types)
        if result:
            _set_result(False)
            _set_message(result)
        return _reply


def check_template(template):
    """
    Check template
    :param template: is a dictionary that should have following keys: constants.REST_OBJECT
    and constants.ACTIONS

    :return: True if template if correct
    """
    if not check_type(template.get(constants.REST_OBJECT), str):
        return False
    if not check_type(template.get(constants.ACTIONS), dict):
        return False
    return True
