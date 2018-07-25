#!/usr/bin/python

__author__ = "Vadim Sychev"
__collaborations__ = ["Andrew Petrov"]

from dellemc_unity_sdk import constants
from enum import Enum
from dellemc_unity_sdk.supportive_functions import _check_type
from dellemc_unity_sdk.supportive_functions import _get_type

default = {constants.PARAMETER_REQUIRED: False,
           constants.PARAMETER_DEFAULT: None,
           constants.PARAMETER_TYPE: None}

_reply = {constants.VALIDATOR_RESULT: True,
          constants.VALIDATOR_MESSAGE: ''}


def check_parameters(dictionary_of_params, param_types):
    """
    Check parameters and return reply.
    Verifies that all required parameters are inputted, and that all parameters from playbook are supported.
    :param dictionary_of_params: is a dictionary of parameters from playbook
    :param param_types: is a dictionary of supported parameters from ansible module
    Example: {'required': {'nasServer','ipPort','ipAddress'},
              'optional': {'netmask','v6PrefixLength','gateway','vlanId','isPreferred','role'}}
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
    Check that template contains constants.REST_OBJECT and constants.ACTIONS keys
    :param template: is a dictionary that should have following keys: constants.REST_OBJECT
    and constants.ACTIONS
    :return: True if template if correct
    """
    if not _check_type(template.get(constants.REST_OBJECT), str):
        return False
    if not _check_type(template.get(constants.ACTIONS), dict):
        return False
    return True


def _set_result(result):
    _reply[constants.VALIDATOR_RESULT] = result


def _set_message(message):
    _reply[constants.VALIDATOR_MESSAGE] = message


def _check_required_parameters(dictionary_of_params, required_params):
    """
    Check that all required parameters are inputted
    :param dictionary_of_params: is a dictionary of parameters from playbook
    :param required_params: is a set of required parameters
    :return: '' if all required parameters are inputted, else string that contains all missing required parameters
    """
    result = ''
    for element in required_params:
        if not dictionary_of_params.get(element):
            result += '{}, '.format(element)
    result = result[:-2]
    return result


def _check_optional_parameters(dictionary_of_params, required_parameters, optional_parameters):
    """
    Check that all parameters from playbook are supported
    :param dictionary_of_params: is a dictionary of parameters from playbook
    :param required_params: is a set of required parameters
    :param optional_parameters: is a set of optional parameters
    :return: '' if all required parameters are inputted, else string that contains all not supported parameters
    """
    result = ''
    for element in dictionary_of_params.keys():
        if not ((element in required_parameters) or (element in optional_parameters)):
            result += '{}, '.format(element)
    result = result[:-2]
    return result


def _check_dict_params(dictionary_of_params, params):
    """
    Verifies that all required parameters are inputted, that all parameters from playbook are supported,
    and that type of value is correct.
    :param params: is a dictionary of parameters from playbook 
    :param param_types: is a dictionary of supported parameters from ansible module
    :return: '' if all required parameters are inputted, else returns the error message
    """
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
            if not _check_type(dictionary_of_params.get(key), params[key][constants.PARAMETER_TYPE]):
                required_type_name = params[key][constants.PARAMETER_TYPE].__name__
                type_name = _get_type(dictionary_of_params.get(key))
                message = constants.ERR_WRONG_TYPE.format(key, required_type_name, type_name)
                return message
    return result


def _set_default(param_types):
    """
    Set default option value if parameter has missing option 
    :param param_types: is a dictionary of supported parameters from ansible module
    :return: None
    """
    for element in param_types:
        for key in default:
            if param_types[element].get(key) is None:
                param_types[element][key] = default[key]
        if param_types[element].get(constants.PARAMETER_TYPE) is object:
            param_types[element][constants.PARAMETER_TYPE] = dict


def _set_enum_value(params, params_types):
    """
    Replace params value with Enum value if parameter has Enum type from rest_supported_enums
    :param params: is a dictionary of parameters from playbook 
    :param param_types: is a dictionary of supported parameters from ansible module
    :return: None
    """
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
