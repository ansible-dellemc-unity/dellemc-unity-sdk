#!/usr/bin/python
from enum import Enum

EXECUTED_BY_KEY = 'executed_by'
EXECUTED_BY_SDK = 'executed by sdk'
ACTION_TYPE_KEY = 'action_type'
PARAMETERS_TYPES_KEY = 'parameters_types'
REST_OBJECT_KEY = 'rest_object'
ACTIONS_KEY = 'actions'
FUNCTION_NAME='function'


class ActionType(Enum):
    UPDATE = 'update'
    QUERY = 'query'
