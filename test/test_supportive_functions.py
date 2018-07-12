#!/usr/bin/python
import unittest
from dellemc_unity_sdk import supportive_functions, constants


def tested_function(self):
    print("Yes")


standard_params = dict(required=False, default=None, type='dict')
expexted_minimal = dict(login=dict(required=True, default=None, type='dict'),
                        get=dict(required=False, default=None, type='dict'))


class TestRunner(unittest.TestCase):

    def test_create_arguments_for_ansible_module_only_function(self):
        arguments = supportive_functions.create_arguments_for_ansible_module([{'function': tested_function}])
        expected_args = expexted_minimal
        expected_args.update(dict(tested_function=standard_params))
        self.assertEqual(arguments, expected_args)

    def test_create_create_arguments_for_ansible_module_random_parameter(self):
        arguments = supportive_functions.create_arguments_for_ansible_module([{constants.ACTION_NAME: tested_function,
                                                                               'key1': 'str'}])
        expected_args = expexted_minimal
        params = dict(required=False, default=None, type='dict')
        params.update({'key1': 'str'})
        expected_args.update(dict(tested_function=params))
        self.assertEqual(arguments, expected_args, {'expected_args': expected_args})

    def test_create_create_arguments_for_ansible_module_change_type(self):
        arguments = supportive_functions.create_arguments_for_ansible_module([{constants.ACTION_NAME: tested_function,
                                                                               'type': 'str'}])
        expected_args = expexted_minimal
        params = standard_params
        params['type'] = 'str'
        expected_args.update(dict(tested_function=params))
        self.assertEqual(arguments, expected_args)

    def test_create_create_arguments_for_ansible_module_template(self):
        template = {
            constants.REST_OBJECT_KEY: 'fileInterface',
            constants.ACTIONS_KEY: {
                'create':
                    {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                     constants.PARAMETER_TYPES_KEY: {}},
                'modify':
                    {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                     constants.PARAMETER_TYPES_KEY: {}},
                'delete':
                    {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                     constants.PARAMETER_TYPES_KEY: {}}
            }
        }
        arguments = supportive_functions.create_arguments_for_ansible_module(template)
        expected_args = dict(login=dict(required=True, default=None, type='dict'),
                             get=dict(required=False, default=None, type='dict'))
        for action in {'create', 'modify', 'delete'}:
            expected_args.update({action: dict(required=False, default=None, type='dict')})
        self.assertEqual(arguments, expected_args, {'expected_args': expected_args})

    def test_create_arguments_for_ansible_module_define_get(self):
        template = {
            constants.REST_OBJECT_KEY: 'fileInterface',
            constants.ACTIONS_KEY: {
                'create':
                    {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                     constants.PARAMETER_TYPES_KEY: {},
                     constants.DO_ACTION: 'nnnn'},
                'modify':
                    {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                     constants.PARAMETER_TYPES_KEY: {}},
                'delete':
                    {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                     constants.PARAMETER_TYPES_KEY: {}},
                'get':{
                    constants.ACTION_TYPE_KEY: constants.ActionType.QUERY,
                    constants.PARAMETER_TYPES_KEY:{}
                }
            }
        }
        arguments = supportive_functions.create_arguments_for_ansible_module(template)
        expected_args = dict(login=dict(required=True, default=None, type='dict'),
                             get=dict(required=False, default=None, type='dict'))
        for action in {'create', 'modify', 'delete'}:
            expected_args.update({action: dict(required=False, default=None, type='dict')})
        self.assertEqual(arguments, expected_args, {'expected_args': expected_args})


if __name__ == '__main__':
    unittest.main()
