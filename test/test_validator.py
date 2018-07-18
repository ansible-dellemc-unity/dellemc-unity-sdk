#!/usr/bin/python
import unittest
from dellemc_unity_sdk import validator
from dellemc_unity_sdk import constants
from dellemc_unity_sdk import rest_supported_enums


class TestValidator(unittest.TestCase):

    def test_check_parameters_normal(self):
        params = {'test1': '1', 'test2': '2', 'test3': '3'}
        params_type = {'required': {'test1', 'test2'}, 'optional': {'test3', 'test5'}}
        result = validator.check_parameters(params, params_type)
        self.assertTrue(result[constants.VALIDATOR_RESULT])

    def test_check_parameters_only_required(self):
        params = {'id': '1', 'test2': '2'}
        params_type = {'required': {'id', 'test2'}}
        result = validator.check_parameters(params, params_type)
        self.assertTrue(result['result'])

    def test_check_template_1(self):
        template = {constants.REST_OBJECT: '1'}
        self.assertFalse(validator.check_template(template))

    def test_check_template_2(self):
        template = {constants.REST_OBJECT: '1', constants.ACTIONS: {}}
        self.assertTrue(validator.check_template(template))

    def test_check_dict_parameters(self):
        template = {'name': {'required': True, 'default': None, 'type': str},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                    'description': {'required': False, 'default': None, 'type': str}
                    }
        params = {'name': 's123',
                  'addPoolUnitParameters': 's123',
                  'description': 'asdasd'
                  }
        self.assertTrue(validator.check_parameters(params, template)['result'])

    def test_check_with_two_unsupported_params(self):
        template = {'name': {'required': True, 'default': None, 'type': str},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                    'description': {'required': False, 'default': None, 'type': str}
                    }
        params = {'name': 's123',
                  'addPoolUnitParameters': 's123',
                  'description': 'asdasd',
                  'vadim': 1,
                  'sychev': 2
                  }
        res = validator.check_parameters(params, template)
        self.assertFalse(res['result'])

    def test_check_dict_parameters_without_required(self):
        template = {'name': {'required': True, 'default': None, 'type': str},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                    'description': {'required': False, 'default': None, 'type': str}
                    }
        params = {
            'addPoolUnitParameters': 's123',
            'description': 'asdasd'
        }
        res = validator.check_parameters(params, template)
        self.assertFalse(res['result'])

    def test_check_dict_parameters_wrong_type(self):
        template = {'name': {'required': True, 'default': None, 'type': str},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                    'description': {'required': False, 'default': None, 'type': str}
                    }
        params = {
            'name': 1,
            'addPoolUnitParameters': 's123',
            'description': 'asdasd'
        }
        reply = validator.check_parameters(params, template)
        self.assertEqual('name must be str, not int.', reply['message'])

    def test_check_dict_parameters_without_two_required(self):
        template = {'name': {'required': True, 'default': None, 'type': str},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                    'description': {'required': False, 'default': None, 'type': str}
                    }
        params = {
            'description': 'asdasd'
        }
        reply = validator.check_parameters(params, template)
        self.assertEqual('Required parameters: name, addPoolUnitParameters was not found.', reply['message'])

    def test_check_dict_parameters_without_required_but_with_default(self):
        template = {'name': {'required': True, 'default': 'pool_1', 'type': str},
                    'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                    'description': {}
                    }
        params = {
            'addPoolUnitParameters': 's123',

        }
        res = validator.check_parameters(params, template)
        self.assertTrue(res['result'])

    def test_params_without_required(self):
        params = {'test2': '2', 'test3': '3'}
        params_type = {'required': {'test1', 'test2'}, 'optional': {'test3', 'test5'}}
        result = validator.check_parameters(params, params_type)
        self.assertFalse(result['result'])

    def test_params_not_supported_param(self):
        params = {'test1': '1', 'test2': '2', 'test3': '3', 'vadim': 3}
        params_type = {'required': {'test1', 'test2'}, 'optional': {'test3', 'test5'}}
        result = validator.check_parameters(params, params_type)
        self.assertFalse(result['result'])

    def test_err_not_supported_param(self):
        params = {'test1': '1', 'test2': '2', 'test3': '3', 'vadim': 3}
        params_type = {'required': {'test1', 'test2'}, 'optional': {'test3', 'test5'}}
        result = validator.check_parameters(params, params_type)
        self.assertEqual('Parameters: vadim are not supported.', result['message'])

    def test_enum_check(self):
        params_type = {'name': {'required': True, 'default': 'pool_1', 'type': str},
                       'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                       'description': {},
                       'type': {'required': False, 'default': None, 'type': rest_supported_enums.HostTypeEnum}
                       }

        params = {
            'name': 'kek',
            'addPoolUnitParameters': 's123',
            'description': 'test description',
            'type': 'RPa'
        }

        result = validator.check_parameters(params, params_type)
        self.assertEqual(params['type'], 4)

    def test_key_not_in_enum(self):
        params_type = {'name': {'required': True, 'default': 'pool_1', 'type': str},
                       'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                       'description': {},
                       'type': {'required': False, 'default': None, 'type': rest_supported_enums.HostTypeEnum}
                       }

        params = {
            'name': 'kek',
            'addPoolUnitParameters': 's123',
            'description': 'asdasd',
            'type': 'RPAS'
        }

        result = validator.check_parameters(params, params_type)
        self.assertFalse(result['result'])

    def test_value_in_enum(self):
        params_type = {'name': {'required': True, 'default': 'pool_1', 'type': str},
                       'addPoolUnitParameters': {'required': True, 'default': None, 'type': str},
                       'description': {},
                       'type': {'required': False, 'default': None, 'type': rest_supported_enums.HostTypeEnum}
                       }

        params = {
            'name': 'kek',
            'addPoolUnitParameters': 's123',
            'description': 'asdasd',
            'type': 1
        }

        result = validator.check_parameters(params, params_type)
        self.assertTrue(result['result'])


if __name__ == '__main__':
    unittest.main()
