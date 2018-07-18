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
    check_result = validator.check_parameters(params, params_types)
    if not check_result[constants.VALIDATOR_RESULT]:
        supportive_functions.raise_exception_about_parameters(check_result[constants.VALIDATOR_MESSAGE])
    reply = unity.update(action, rest_object, params)
    return reply


def do_query_request(unity, params, params_types, rest_object):
    if params == {}:
        raise ValueError("input some parameters for GET request")
    reply = unity.query(rest_object, params)
    return reply


def create_arguments_for_ansible_module(array_of_dictionaries):
    """
    Use the same function from supportive_functions
    :param array_of_dictionaries: array of dictionaries that wrap functions and special information for AnsibleModule.
    Example: {'function':do_smth, 'key':value,...}
    :return:
    """
    return supportive_functions.create_arguments_for_ansible_module(array_of_dictionaries)


def run(ansible_module, template):
    """
    Run AnsibleModule and execute functions if they exists
    :param ansible_module: AnsibleModule
    :param template: is a dictionary that should have following keys: constants.REST_OBJECT and
    constants.ACTIONS
    :return: None
    """
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if ansible_module.check_mode:
        print('%s' % json.dumps(ansible_module.params))
        return

    if not validator.check_template(template):
        raise ValueError('incorrect template')
    unity = _create_unity(ansible_module)

    rest_object = template.get(constants.REST_OBJECT)
    actions = template.get(constants.ACTIONS)
    params = ansible_module.params
    rest_object_for_get = template.get(constants.REST_OBJECT_FOR_GET_REQUEST)
    if not rest_object_for_get:
        rest_object_for_get = rest_object

    executing_module_info = dict()
    try:
        for action_name in actions.keys():
            if params.get(action_name):
                function_ptr = actions.get(action_name).get(constants.EXECUTED_BY)
                info = {}
                if function_ptr and (function_ptr != constants.EXECUTED_BY_SDK):
                    # if customer select special function to execute the action we use this function
                    if callable(function_ptr):
                        info = function_ptr(params.get(action_name), unity)
                    else:
                        raise TypeError("You try execute action by not callable object")
                else:
                    # if customer doesn't select special function to execute the action or put flag EXECUTED_BY_SDK
                    # action will be executed automatically by using following standard functions: do_update_request and
                    # do_query_request
                    action = actions.get(action_name)
                    info = _execute_request_by_sdk(action_name, action, unity, rest_object, rest_object_for_get, params)

                executing_module_info.update({action_name: info})
        if params.get(constants.GET):
            if not (constants.GET in actions.keys()):
                info = do_query_request(unity, params.get(constants.GET), {}, rest_object_for_get)
                executing_module_info.update({constants.GET: info})

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

    unity_ip = login_params[constants.UNITY_IP]
    username = login_params[constants.USERNAME]
    password = login_params[constants.PASSWORD]
    return Unity(unity_ip, username, password)


def _execute_request_by_sdk(action_name, action, unity, rest_object, rest_object_for_get, params):
    info = {}
    parameters_types = action.get(constants.PARAMETER_TYPES)
    action_type = action.get(constants.ACTION_TYPE)

    do_action = action.get(constants.DO_ACTION)
    if not do_action: do_action = action_name

    rest_object_for_request = action.get(constants.REST_OBJECT)

    if action_type == constants.ActionType.UPDATE:
        if not rest_object_for_request:
            rest_object_for_request = rest_object
        info = do_update_request(unity, params.get(action_name), parameters_types, rest_object_for_request,
                                 do_action)
    elif action_type == constants.ActionType.QUERY:
        if not rest_object_for_request:
            rest_object_for_request = rest_object_for_get

        info = do_query_request(unity, params.get(action_name), parameters_types, rest_object_for_request)
    else:
        raise ValueError(
            "you select unsupported '" + constants.ACTION_TYPE + "' use them only from "
                                                                 "constants.ActionType")
    return info
