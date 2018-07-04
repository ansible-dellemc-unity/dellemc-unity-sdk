#!/usr/bin/python

__author__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"
from dellemc_unity_sdk import constants


def _check_type(param, param_type):
    if param_type is None:
        return True
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


def check_parameters(dictionary_of_params, param_types):
    list_of_required = param_types.get('required')
    if not list_of_required:
        list_of_required = {}
    if not _check_required_parameters(dictionary_of_params, list_of_required):
        return False
    list_of_optional = param_types.get('optional')
    if not list_of_optional:
        list_of_optional = {}
    return _check_optional_parameters(dictionary_of_params, list_of_required, list_of_optional)


def check_template(template):
    if not _check_type(template[constants.REST_OBJECT_KEY], 'str'):
        return False
    if not _check_type(template[constants.ACTIONS_KEY], 'dict'):
        return False
    return True
