# Readme

A python module to execute [ansible-dellemc-unity](https://github.com/ansible-dellemc-unity/ansible-dellemc-unity) (Ansible modules for DellEMC Unity).

This SDK provides common functions for all Ansible modules and special interface to communicate with Unity.

## How to install this SDK

You have several ways to install this SDK

##### Install from pip repo
``pip install dellemc-unity-sdk``

##### Install from source

    git clone https://github.com/ansible-dellemc-unity/dellemc-unity-sdk.git
    cd dellemc-unity-sdk
    python setup.py sdist
    sudo pip install dist/dellemc_unity_sdk.xxxx.tar.gz

## How to write modules

According to our experience and [issue #4](https://github.com/ansible-dellemc-unity/dellemc-unity-sdk/issues/4) , 
you should create an instance of AnsibleModule in your module. So to create you should argument_spec use:

``supportive_functions.create_arguments_for_ansible_module(array_of_dictionaries)`` or 
``supportive_functions.create_arguments_for_ansible_module(template)``

After that make an instance of AnsibleModule and put it next to template into

``runner.run(ansible_module, template)``

Your module will be automatically executed by SDK.

## How to write templates for runner.run(...)

template is a dictionary that should have following keys:

1. ``constants.REST_OBJECT = 'rest_object'`` value of this key should be a REST object
2. ``constants.ACTIONS = 'actions'`` value of this key should be a dictionary of actions,
for example, {'create:{...}', 'delete':{...},...}

To execute actions automatically dictionary of action should have following parameters:

1. ``constants.ACTION_TYPE`` value of this key should be ``constants.ActionType.UPDATE`` or ``constants.ActionType.QUERY``
2. ``constants.PARAMETER_TYPES = 'parameter_types'`` value of this key should be a dictionary that should have keys:
'required' and 'optional' and value of each key should be iterable.

For example:

    {
        constants.REST_OBJECT: 'pool',
        constants.ACTIONS: {
            'delete':
                {constants.ACTION_TYPE: constants.ActionType.UPDATE,
                 constants.PARAMETER_TYPES: parameters_all.get('delete')}
        }
    }

### Optional parameters (keys) for template

1. ``constants.REST_OBJECT_FOR_GET_REQUEST`` use this key for making GET request to REST
 object that is different from ``constants.REST_OBJECT``

### Optional parameters (keys) for dictionary of actions

1. ``constants.DO_ACTION = 'do action'`` use this constant if you want the parameter name in the playbook to 
be different from the one in the REST model. For example,
 
       {
           constants.REST_OBJECT: 'lun',
           constants.ACTIONS: {
               'create':
                   {
                      constants.ACTION_TYPE: constants.ActionType.UPDATE,
                      constants.PARAMETER_TYPES: parameters_all.get('create'),
                      constants.DO_ACTION: "
                   }
           }
       }    

### How to write type of parameters for validator

It should be a dictionary that can be writen in two ways

#### Variant with type of arguments

    {
        "required_argument_var1" : dict(required=True, type=<type of this object>, default=<default_value>),
        "required_argument_var2" : dict(required=True),
        "optional_argument": dict(required=False),
        "optional_argument_var_2": dict()... 
    }
    
you can skip some keys in dictionary of argument, by default it will be 
``dict(required=False, type=None, default=None)``

**supported types of arguments**:

* _None_ - validator doesn't check type of this argument
* _dict_ - validator expect type dictionary
* _object_ - same as dict
* _bool_
* _int_
* _str_
* _list_
* any others python's object
* supported enums from dellemc_unity_sdk.rest_supported_enums

#### Variant with keys (easy way)

Dictionary should have keys: "required" and "optional". For example: 

    {
        'required': {'type', 'name'},
        'optional': {'description','osType','tenant'},
    }

## How to execute custom functions

If your request can't be made by functions ``runner.do_update_request(...)`` or ``runner.do_query_request(...)`` you can
execute your own function by using key ``constants.EXECUTED_BY = 'executed_by'``

For example:

    {
        constants.REST_OBJECT: 'pool',
        constants.ACTIONS: {'create': {constants.EXECUTED_BY: function}}
    }

Your function should have 2 parameters (parameters, unity). parameters = parameters from *.yml file, 
unity = instance of class Unity and also function must have return statement, 
that will be add to output in parameter ``'output'``

## Additional information

All REST objects have action _"get"_ (``constants.GET``), that sends GET requests, you are allowed to redefine this action 


