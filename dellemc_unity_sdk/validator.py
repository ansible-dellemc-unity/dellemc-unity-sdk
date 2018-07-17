#!/usr/bin/python

__author__ = "Vadim Sychev"
__collaborations__ = ["Andrew Petrov"]

from dellemc_unity_sdk import constants

default = {'required': False,
           'default': None,
           'type': None}

reply = {constants.VALIDATOR_RESULT: True,
         constants.VALIDATOR_MESSAGE: ''}


def _create_reply(result, message=''):
    reply[constants.VALIDATOR_RESULT] = result
    reply[constants.VALIDATOR_MESSAGE] = message
    return reply


def _get_type(param):
    return param.__class__.__name__


def _check_type(param, param_type):
    return _get_type(param) == param_type


def _check_required_parameters(dictionary_of_params, required_params):
    for element in required_params:
        if not dictionary_of_params.get(element):
            return element
    return None


def _check_optional_parameters(dictionary_of_params, required_parameters, optional_parameters):
    for element in dictionary_of_params.keys():
        if not ((element in required_parameters) or (element in optional_parameters)):
            return element
    return None


def _check_dict_params(dictionary_of_params, params):
    for key in dictionary_of_params:
        if key not in params:
            return _create_reply(False, constants.ERR_UNSUPPORTED_PARAMETER.format(key))
        elif params[key]['type'] is not None:
            if not _check_type(dictionary_of_params.get(key), params[key]['type']):
                message = constants.ERR_WRONG_TYPE.format(key, params[key]['type'],
                                                          _get_type(dictionary_of_params.get(key)))
                return _create_reply(False, message)

    for key in params:
        if key not in dictionary_of_params:
            if params[key]['default'] is not None:
                dictionary_of_params[key] = params[key]['default']
            elif params[key]['required'] is True:
                return _create_reply(False, constants.ERR_MISSING_REQUIRED_PARAMETER.format(key))
    return _create_reply(True, '')


def _set_default(param_types):
    for element in param_types:
        for key in default:
            if param_types[element].get(key) is None:
                param_types[element][key] = default[key]


def check_parameters(dictionary_of_params, param_types):
    if (param_types.get('required') is not None) or (param_types.get('optional') is not None):

        list_of_required = param_types.get('required')
        if not list_of_required:
            list_of_required = {}
        result = _check_required_parameters(dictionary_of_params, list_of_required)
        if result is not None:
            return _create_reply(False, constants.ERR_MISSING_REQUIRED_PARAMETER.format(result))

        list_of_optional = param_types.get('optional')
        if not list_of_optional:
            list_of_optional = {}
        result = _check_optional_parameters(dictionary_of_params, list_of_required, list_of_optional)
        if result is not None:
            return _create_reply(False, constants.ERR_UNSUPPORTED_PARAMETER.format(result))
        return _create_reply(True, '')
    else:
        _set_default(param_types)
        _check_dict_params(dictionary_of_params, param_types)
        return reply


def check_template(template):
    if not _check_type(template.get(constants.REST_OBJECT_KEY), 'str'):
        return False
    if not _check_type(template.get(constants.ACTIONS_KEY), 'dict'):
        return False
    return True
