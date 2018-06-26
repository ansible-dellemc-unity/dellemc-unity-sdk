#!/usr/bin/python

__author__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


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
