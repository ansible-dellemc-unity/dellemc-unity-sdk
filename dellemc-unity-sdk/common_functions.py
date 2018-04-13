#!/usr/bin/python

__author__ = "Andrew Petrov"
__maintainer__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


def check_required_parameters(dictionaryOfParams, listOfRequired):
    for element in listOfRequired:
        if not dictionaryOfParams.get(element):
            return False
    return True


def check_optional_parameters(dictionaryOfParams, listOfRequired, listOfOptional):
    for element in dictionaryOfParams.keys():
        if not ((element in listOfRequired) or (element in listOfOptional)):
            return False
    return True


def check_parameters(dictionaryOfParams, listOfRequired, listOfOptional):
    if not check_required_parameters(dictionaryOfParams, listOfRequired):
        return False
    return check_optional_parameters(dictionaryOfParams, listOfRequired, listOfOptional)