from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.dellemc_unity_sdk.unity import Unity
from ansible.module_utils.dellemc_unity_sdk.ansible_function import AnsibleFunction


def run(array_of_ansible_functions):
    arguments = dict()
    # TODO: maybe add required parameter for login
    for element in array_of_ansible_functions:
        arguments.update({element.get_name(): element.get_module_params()})
    module = AnsibleModule(argument_spec=arguments, supports_check_mode=True)
    run_module(module, array_of_ansible_functions)


def run_module(ansible_module, array_of_ansible_functions):
    # TODO: get username, host and password
    host = '192.168.0.0'
    unity = Unity(host)
    for i in range(0, len(array_of_ansible_functions)):
        element = array_of_ansible_functions[i]
        if ansible_module.params[element.get_name()]:
            element.run(ansible_module.params[element.get_name()], unity)

    # TODO: print information
