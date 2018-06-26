#!/usr/bin/python

import json
import warnings
from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk.unity import Unity

__author__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


def create_arguments_for_ansible_module(array_of_dictionaries):  # TODO:  check it
    """
    :param array_of_dictionaries: array of dictionaries that wrap functions and special information for AnsibleModule.
    Example: {'function':do_smth, 'key':value,...}
    :return:
    """
    keys = {'required', 'default', 'type'}
    arguments = dict(login=dict(required=True, default=None, type='dict'))

    for dictionary in array_of_dictionaries:
        function_ptr = dictionary['function']
        if function_ptr is None:
            raise ValueError("dictionary don't have key 'function'")
        parameters = dict(required=False, default=None, type='dict')
        for key in keys:
            if key in dictionary:
                parameters[key] = dictionary.get(key)
        for key in dictionary.keys():
            if (key not in keys) and (key != 'function'):
                parameters.update({key: dictionary.get(key)})

        arguments.update({function_ptr.__name__: parameters})
    return arguments


def run(array_of_dictionaries):
    """
    :param array_of_dictionaries: array of dictionaries that wrap functions and special information for AnsibleModule.
    Example: {'function':do_smth, 'key':value,...}
    :return: None
    """
    warnings.warn("This function is unstable. Use function run_module", DeprecationWarning)
    arguments = create_arguments_for_ansible_module(array_of_dictionaries)
    module = AnsibleModule(argument_spec=arguments, supports_check_mode=True)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        print('%s' % json.dumps(module.params))
    else:
        queue = []
        for i in range(0, len(array_of_dictionaries)):
            queue.append(array_of_dictionaries[i]['function'])
        run_module(module, queue)


def run_module(ansible_module, queue_of_functions):
    unity = _create_unity(ansible_module)
    special_info = dict()

    for i in range(0, len(queue_of_functions)):
        function_ptr = queue_of_functions[i]
        if ansible_module.params[function_ptr.__name__]:
            ok, info = function_ptr(ansible_module.params[function_ptr.__name__], unity)
            if not ok:
                ansible_module.fail_json(changed=unity.changed, msg=info, query_results=unity.queryResults,
                                         update_results=unity.updateResults)
            else:
                if info:
                    special_info.update({function_ptr.__name__: info})
            if unity.err:
                ansible_module.fail_json(changed=unity.changed, msg=unity.err, query_results=unity.queryResults,
                                         update_results=unity.updateResults, special_info=special_info)

    ansible_module.exit_json(changed=unity.changed, query_results=unity.queryResults,
                             update_results=unity.updateResults, special_information=special_info)
    del unity


def _create_unity(ansible_module):
    if not ansible_module.params['login']:
        ansible_module.fail_json(changed=False, msg='You must input login parameter')

    login_params = ansible_module.params['login']

    host = login_params['host']
    username = login_params['username']
    password = login_params['password']
    return Unity(host, username, password)
