#!/usr/bin/python

__author__ = "Andrew Petrov"
__maintainer__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


def check_required_parameters(dictionary_of_params, list_of_required):
    for element in list_of_required:
        if not dictionary_of_params.get(element):
            return False
    return True


def check_optional_parameters(dictionary_of_params, list_of_required, list_of_optional):
    for element in dictionary_of_params.keys():
        if not ((element in list_of_required) or (element in list_of_optional)):
            return False
    return True


def check_parameters(dictionaryOfParams, list_of_required, list_of_optional):
    if not check_required_parameters(dictionaryOfParams, list_of_required):
        return False
    return check_optional_parameters(dictionaryOfParams, list_of_required, list_of_optional)
