#!/usr/bin/python
import unittest
from dellemc_unity_sdk import validator


class TestValidator(unittest.TestCase):

    def test_check_parameters_normal(self):
        params = {'test1': '1', 'test2': '2', 'test3': '3'}
        params_type = {'required':{'test1','test2'}, 'optional': {'test3', 'test5'}}
        self.assertTrue(validator.check_parameters(params, params_type))

    def test_check_parameters_only_required(self):
        params = {'id': '1', 'test2': '2'}
        params_type = {'required':{'id','test2'}}
        self.assertTrue(validator.check_parameters(params, params_type))


if __name__ == '__main__':
    unittest.main()
