#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk.unity import Unity

__author__ = "Andrew Petrov"
__maintainer__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


def run(array):
    keys = {'required', 'default', 'type'}
    arguments = dict(login=dict(required=True, default=None, type='dict'))  # TODO: check it
    for dictionary in array:
        function_ptr = dictionary['function']
        parameters = dict(required=False, default=None, type='dict')
        for key in keys:
            if key in dictionary:
                parameters[key] = dictionary.get(key)

        arguments.update({function_ptr.__name__: parameters})
    module = AnsibleModule(argument_spec=arguments, supports_check_mode=True)
    _run_module(module, array)


def _run_module(ansible_module, array):
    if not ansible_module.params['login']:
        ansible_module.fail_json(changed=False, msg='You must input login parameter')
    login_params = ansible_module.params['login']

    host = login_params['host']
    username = login_params['username']
    password = login_params['password']

    unity = Unity(host, username, password)
    special_info = dict()
    for i in range(0, len(array)):
        function_ptr = array[i]['function']
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
