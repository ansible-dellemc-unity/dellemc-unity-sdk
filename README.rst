You need to have this SDK to execute ansible-dellemc-unity (Ansible modules for DellEMC Unity).

This SDK provides common functions for all Ansible modules and special interface to communicate with Unity.


How to write modules?

According to our experience and issue #4, you should create an instance of AnsibleModule in your module ansible module,
so for that you can use `runner.create_arguments_for_ansible_module(array_of_dictionaries)` to create special argument spec
for AnsibleModule, after that make an instance of AnsibleModule and put it with template into `runner.run(ansible_module, template)`

Your module will be automatically execute by SDK.

How to write templates for `runner.run(...)`?

template is a dictionary that should have following keys:
  1. `constants.REST_OBJECT_KEY = 'rest_object'` value of this key should be a REST object
  2. `constants.ACTIONS_KEY = 'actions'` value of this key should be a dictionary of actions,
     for example, {'create:{...}', 'delete':{...},...}

To execute actions automatically dictionary of action should have following parameters:
  1. `constants.ACTION_TYPE_KEY` value of this key should be `constants.ActionType.UPDATE` or `constants.ActionType.QUERY`
  2. `constants.PARAMETER_TYPES_KEY = 'parameter_types'` value of this key should be a dictionary that should have keys:
     'required' and 'optional' and value of each key should be iterable.

For example,
 `{
    constants.REST_OBJECT_KEY: 'pool',
    constants.ACTIONS_KEY: {
        'delete':
            {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
             constants.PARAMETER_TYPES_KEY: parameters_all.get('delete')}
    }`

How to execute custom function?

If your request can't be made by functions `runner.do_update_request(...)` or `runner.do_query_request(...)` you can
execute your own function by using key `constants.EXECUTED_BY_KEY = 'executed_by'`, for example,
`{constants.REST_OBJECT_KEY: 'pool',
  constants.ACTIONS_KEY: {'create': {constants.EXECUTED_BY_KEY: function}}
  }`
function should have 2 parameters (parameters, unity). parameters = parameters from yml file, unity = instance of class Unity and
also function must have return statement, that will be add to output in parameter `'output'`

