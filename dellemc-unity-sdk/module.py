from ansible.module_utils.basic import AnsibleModule
from .unity import Unity

__author__ = "Andrew Petrov"
__maintainer__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


def run(array_of_ansible_functions):
    arguments = dict()
    # TODO: maybe add required parameter for login
    for element in array_of_ansible_functions:
        arguments.update({element.get_name(): element.get_module_params()})
    module = AnsibleModule(argument_spec=arguments, supports_check_mode=True)
    run_module(module, array_of_ansible_functions)


def _run_module(ansible_module, array_of_ansible_functions):
    # TODO: get username, host and password from module
    host = '192.168.70.217'
    unity = Unity(host)
    special_info_from_function = dict()
    for i in range(0, len(array_of_ansible_functions)):
        element = array_of_ansible_functions[i]
        if ansible_module.params[element.get_name()]:
            ok, info = element.run(ansible_module.params[element.get_name()], unity)
            if not ok:
                ansible_module.fail_json(changed=unity.changed, msg=info, query_results=unity.queryResults,
                                         update_results=unity.updateResults)
            else:
                if info:
                    special_info_from_function.update({element.get_name(): info})
            # TODO: make output
            if unity.err:
                ansible_module.fail_json(changed=unity.changed, msg=unity.err, query_results=unity.queryResults,
                                         update_results=unity.updateResults)

    ansible_module.exit_json(changed=unity.changed, query_results=unity.queryResults,
                             update_results=unity.updateResults, special_information = special_info_from_function)
    del unity
