#!/usr/bin/python

from dellemc_unity_sdk import constants


def raise_exception_about_result(check_results, supported_parameters):
    raise ValueError(check_results['message'] + ',\
     supported parameters = ' + supported_parameters.__str__())


def raise_exception_about_parameters(supported_parameters):
    """
    custom function, use it to handle parameter exception
    :param supported_parameters: dictionary of supported parameters types.
     Example: {'required':{...}, 'optional':{...}}
    :return: False, special string about exception
    """
    raise ValueError('You did not input required parameters or inputted unsupported parameter, ' \
                     'supported parameters = ' + supported_parameters.__str__())


def create_arguments_for_ansible_module(arguments):
    """
    Create special arguments_spec for AnsibleModule, some arguments expected in runner.run(...)
    :param arguments: either template or array_of_dictionaries

    1. array of dictionaries that wrap functions and special information for AnsibleModule.
    Example: {'function':do_smth, 'key':value,...}
    2. template that you create for runner.run(...)
    :return: argument_spec for AnsibleModule
    """
    if arguments.__class__.__name__ == 'dict':
        return _create_arguments_for_ansible_module_from_template(arguments)
    return _create_arguments_for_ansible_module_from_array(arguments)


def _create_arguments_for_ansible_module_from_template(template):
    arguments = dict(login=dict(required=True, default=None, type='dict'),
                     get=dict(required=False, default=None, type='dict'))

    parameters = dict(required=False, default=None, type='dict')
    actions = template.get(constants.ACTIONS_KEY)
    for action_name in actions.keys():
        arguments.update({action_name: parameters})
    return arguments


def _create_arguments_for_ansible_module_from_array(array_of_dictionaries):
    """
    Create special arguments_spec for AnsibleModule, some arguments expected in runner.run(...)
    :param array_of_dictionaries: array of dictionaries that wrap functions and special information for AnsibleModule.
    Example: {'function':do_smth, 'key':value,...}
    :return: argument_spec for AnsibleModule
    """
    keys = {'required', 'default', 'type'}
    arguments = dict(login=dict(required=True, default=None, type='dict'),
                     get=dict(required=False, default=None, type='dict'))

    for dictionary in array_of_dictionaries:
        function_ptr = dictionary.get(constants.ACTION_NAME)
        if function_ptr is None:
            raise ValueError("dictionary don't have key '" + constants.ACTION_NAME + "'")
        parameters = dict(required=False, default=None, type='dict')
        for key in keys:
            if key in dictionary:
                parameters[key] = dictionary.get(key)
        for key in dictionary.keys():
            if (key not in keys) and (key != constants.ACTION_NAME):
                parameters.update({key: dictionary.get(key)})

        if callable(function_ptr):
            arguments.update({function_ptr.__name__: parameters})
        else:
            arguments.update({function_ptr: parameters})
    return arguments
