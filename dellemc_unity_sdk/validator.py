#!/usr/bin/python

__author__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"

from dellemc_unity_sdk import constants

default = {'required': False,
           'default': None,
           'type': 'str'}


def _check_type(param, param_type):
    return param.__class__.__name__ == param_type


def _check_required_parameters(dictionary_of_params, required_params):
    for element in required_params:
        if not dictionary_of_params.get(element):
            return False
    return True


def _check_optional_parameters(dictionary_of_params, required_parameters, optional_parameters):
    for element in dictionary_of_params.keys():
        if not ((element in required_parameters) or (element in optional_parameters)):
            return False
    return True


def _check_dict_params(dictionary_of_params, params):
    for key in dictionary_of_params:
        if key not in params:
            return False
        elif not _check_type(dictionary_of_params.get(key), params[key]['type']):
            return False

    for key in params:
        if key not in dictionary_of_params:
            if params[key]['default'] is not None:
                dictionary_of_params[key] = params[key]['default']
            elif params[key]['required'] is True:
                return False
    return True


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
        if not _check_required_parameters(dictionary_of_params, list_of_required):
            return False
        list_of_optional = param_types.get('optional')
        if not list_of_optional:
            list_of_optional = {}
        return _check_optional_parameters(dictionary_of_params, list_of_required, list_of_optional)
    else:
        _set_default(param_types)
        return _check_dict_params(dictionary_of_params, param_types)


def check_template(template):
    if not _check_type(template.get(constants.REST_OBJECT_KEY), 'str'):
        return False
    if not _check_type(template.get(constants.ACTIONS_KEY), 'dict'):
        return False
    return True
