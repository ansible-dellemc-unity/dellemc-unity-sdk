#!/usr/bin/python
import unittest
from dellemc_unity_sdk import runner


def tested_function(self):
    print("Yes")


standard_params = dict(required=False, default=None, type='dict')
expexted_minimal = dict(login=dict(required=True, default=None, type='dict'))


class TestRunner(unittest.TestCase):

    def test_create_arguments_for_ansible_module_only_function(self):
        arguments = runner.create_arguments_for_ansible_module([{'function': tested_function}])
        expected_args = expexted_minimal
        expected_args.update(dict(tested_function=standard_params))
        self.assertEqual(arguments, expected_args)

    def test_create_arguments_for_ansible_module_function_and_type(self):
        arguments = runner.create_arguments_for_ansible_module([{'function': tested_function, 'type': 'str'}])
        expected_args = expexted_minimal
        expected_args.update(dict(tested_function=dict(required=False, default=None, type='str')))
        self.assertEqual(arguments, expected_args, {'expected_args': expected_args})

    def test_create_arguments_for_ansible_module_function_and_not_standard_keys(self):
        arguments = runner.create_arguments_for_ansible_module([{'function': tested_function, 'key1': '1'}])
        expected_args = expexted_minimal
        params = standard_params
        params.update({'key1': '1'})
        expected_args.update(dict(tested_function=params))
        self.assertEqual(arguments, expected_args, {'expected_args':expected_args})

