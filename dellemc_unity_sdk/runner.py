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
    # if not validator.check_parameters(params,params_types):
    #    supportive_functions.raise_exception_about_parameters(params_types)
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
    :param template: is a dictionary that should have following keys: constants.REST_OBJECT_KEY and
    constants.ACTIONS_KEY
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
                    # if customer doesn't select special function to execute the action or put flag EXECUTED_BY_SDK
                    # action will be executed automatically by using following standard functions: do_update_request and
                    # do_query_request
                    action = actions.get(action_name)
                    parameters_types = action.get(constants.PARAMETER_TYPES_KEY)
                    action_type = action.get(constants.ACTION_TYPE_KEY)
                    do_action = action.get(constants.DO_ACTION)
                    if not do_action: do_action = action_name
                    if action_type == constants.ActionType.UPDATE:
                        info = do_update_request(unity, params.get(action_name), parameters_types, rest_object,
                                                 do_action)
                    elif action_type == constants.ActionType.QUERY:
                        info = do_query_request(unity, params.get(action_name), parameters_types, rest_object)
                    else:
                        raise ValueError(
                            "you select unsupported '" + constants.ACTION_TYPE_KEY + "' use them only from "
                                                                                     "constants.ActionType")
                executing_module_info.update({action_name: info})
        if params.get('get'):
            info = do_query_request(unity, params.get('get'), {}, rest_object)
            executing_module_info.update({'get': info})

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
