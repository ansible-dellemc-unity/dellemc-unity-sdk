#!/usr/bin/python
import unittest
from dellemc_unity_sdk import validator
from dellemc_unity_sdk import constants


class TestValidator(unittest.TestCase):

    def test_check_parameters_normal(self):
        params = {'test1': '1', 'test2': '2', 'test3': '3'}
        params_type = {'required': {'test1', 'test2'}, 'optional': {'test3', 'test5'}}
        self.assertTrue(validator.check_parameters(params, params_type))

    def test_check_parameters_only_required(self):
        params = {'id': '1', 'test2': '2'}
        params_type = {'required': {'id', 'test2'}}
        self.assertTrue(validator.check_parameters(params, params_type))

    def test_check_template_1(self):
        template = {constants.REST_OBJECT_KEY: '1'}
        self.assertFalse(validator.check_template(template))

    def test_check_template_2(self):
        template = {constants.REST_OBJECT_KEY: '1', constants.ACTIONS_KEY: {}}
        self.assertTrue(validator.check_template(template))

    def test_check_dict_parameters(self):
        template = {'name': {'required': True, 'default': None, 'type': 'str'},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': 'str'},
                    'description': {'required': False, 'default': None, 'type': 'str'}
                    }
        params = {'name': 's123',
                  'addPoolUnitParameters': 's123',
                  'description': 'asdasd'
                  }
        self.assertTrue(validator.check_parameters(params, template))

    def test_check_dict_parameters_without_required(self):
        template = {'name': {'required': True, 'default': None, 'type': 'str'},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': 'str'},
                    'description': {'required': False, 'default': None, 'type': 'str'}
                    }
        params = {
            'addPoolUnitParameters': 's123',
            'description': 'asdasd'
        }
        self.assertFalse(validator.check_parameters(params, template))

    def test_check_dict_parameters_without_required_but_with_default(self):
        template = {'name': {'required': True, 'default': 'pool_1', 'type': 'str'},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': 'str'},
                    'description': {}
                    }
        params = {
            'addPoolUnitParameters': 's123',

        }
        self.assertTrue(validator.check_parameters(params, template))


if __name__ == '__main__':
    unittest.main()
