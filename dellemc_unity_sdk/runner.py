#!/usr/bin/python

import json
import warnings
from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import validator
from dellemc_unity_sdk import supportive_functions
from dellemc_unity_sdk import constants

__author__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


def do_update_request(unity, params, params_types, rest_object, action):
    if not validator.check_parameters(params, params_types):
        supportive_functions.raise_exception_about_parameters(params_types)
    reply = unity.update(action, rest_object, params)
    return reply


def do_query_request(unity, params, params_types, rest_object):
    return {'do_query_request is unsupported yet'}


def create_arguments_for_ansible_module(array_of_dictionaries):  # TODO:  check it
    """
    :param array_of_dictionaries: array of dictionaries that wrap functions and special information for AnsibleModule.
    Example: {'function':do_smth, 'key':value,...}
    :return:
    """
    keys = {'required', 'default', 'type'}
    arguments = dict(login=dict(required=True, default=None, type='dict'))

    for dictionary in array_of_dictionaries:
        function_ptr = dictionary[constants.FUNCTION_NAME]
        if function_ptr is None:
            raise ValueError("dictionary don't have key '" + constants.FUNCTION_NAME + "'")
        parameters = dict(required=False, default=None, type='dict')
        for key in keys:
            if key in dictionary:
                parameters[key] = dictionary.get(key)
        for key in dictionary.keys():
            if (key not in keys) and (key != constants.FUNCTION_NAME):
                parameters.update({key: dictionary.get(key)})

        if callable(function_ptr):
            arguments.update({function_ptr.__name__: parameters})
        else:
            arguments.update({function_ptr: parameters})
    return arguments


def run_module(ansible_module, queue_of_functions):
    """
    run AnsibleModule and execute functions if they exists
    :param ansible_module: AnsibleModule
    :param queue_of_functions: sequence of functions execution
    :return: None
    """
    if ansible_module.check_mode:
        print('%s' % json.dumps(ansible_module.params))
        return
    unity = _create_unity(ansible_module)
    executing_module_info = dict()

    for i in range(0, len(queue_of_functions)):
        function_ptr = queue_of_functions[i]
        if ansible_module.params.get(function_ptr.__name__):
            try:
                info = function_ptr(ansible_module.params[function_ptr.__name__], unity)
                executing_module_info.update({function_ptr.__name__: info})
            except Exception as err:
                ansible_module.fail_json(changed=unity.changed, msg=err.__str__(),
                                         query_results=unity.queryResults,
                                         update_results=unity.updateResults,
                                         output=executing_module_info)
                del unity
                return

            if unity.err:
                ansible_module.fail_json(changed=unity.changed, msg=unity.err,
                                         query_results=unity.queryResults,
                                         update_results=unity.updateResults,
                                         output=executing_module_info)

    ansible_module.exit_json(changed=unity.changed, query_results=unity.queryResults,
                             update_results=unity.updateResults, output=executing_module_info)
    del unity


def run(ansible_module, template):
    """

    :param ansible_module:
    :param template:
    :return:
    """
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if ansible_module.check_mode:
        print('%s' % json.dumps(ansible_module.params))
        return
    if not validator.check_template(template):
        raise ValueError('incorrect template')  # TODO: check it
    unity = _create_unity(ansible_module)

    rest_object = template.get(constants.REST_OBJECT_KEY)
    actions = template.get(constants.ACTIONS_KEY)
    params = ansible_module.params

    executing_module_info = dict()
    try:
        for action_name in actions.keys():
            if params.get(action_name):
                function_ptr = actions.get(action_name).get(constants.EXECUTED_BY_KEY)
                info = {}
                if function_ptr and (function_ptr != constants.EXECUTED_BY_SDK):
                    # if customer select special function to execute the action we use this function
                    if callable(function_ptr):
                        info = function_ptr(params.get(action_name), unity)
                    else:
                        raise TypeError("You try execute action by not callable object")
                else:
                    # if customer don't select special function to execute the action or put flag EXECUTED_BY_SDK
                    # action will be executed automatically by using following standard functions: do_update_request and
                    # do_query_request
                    action = actions.get(action_name)
                    parameters_types = action.get(constants.PARAMETERS_TYPES_KEY)
                    action_type = action.get(constants.ACTION_TYPE_KEY)

                    if action_type == constants.ActionType.UPDATE:
                        info = do_update_request(unity, params.get(action_name), parameters_types, rest_object,
                                                 action_name)
                    elif action_type == constants.ActionType.QUERY:
                        info = do_query_request(unity, params.get(action_name), parameters_types, rest_object)
                    else:
                        raise ValueError(
                            "you select unsupported '" + constants.ACTION_TYPE_KEY + "' use them only from "
                                                                                     "constants.ActionType")
                executing_module_info.update({action_name: info})

    except Exception as err:
        ansible_module.fail_json(changed=unity.changed, msg=err.__str__(),
                                 query_results=unity.queryResults,
                                 update_results=unity.updateResults,
                                 output=executing_module_info)
        del unity
        return

    if unity.err:
        ansible_module.fail_json(changed=unity.changed, msg=unity.err,
                                 query_results=unity.queryResults,
                                 update_results=unity.updateResults,
                                 output=executing_module_info)

    ansible_module.exit_json(changed=unity.changed, query_results=unity.queryResults,
                             update_results=unity.updateResults, output=executing_module_info)
    del unity


def _create_unity(ansible_module):
    if not ansible_module.params['login']:
        ansible_module.fail_json(changed=False, msg='You must input login parameter')

    login_params = ansible_module.params['login']

    host = login_params['host']
    username = login_params['username']
    password = login_params['password']
    return Unity(host, username, password)
