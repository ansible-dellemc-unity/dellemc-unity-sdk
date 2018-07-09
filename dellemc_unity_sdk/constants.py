#!/usr/bin/python
from enum import Enum

EXECUTED_BY_KEY = "executed_by"
EXECUTED_BY_SDK = "executed_by_sdk"
ACTION_TYPE_KEY = "action_type"
PARAMETER_TYPES_KEY = "parameter_types"
REST_OBJECT_KEY = "rest_object"
ACTIONS_KEY = "actions"
ACTION_NAME = "function"
DO_ACTION = "do_action"


class ActionType(Enum):
    UPDATE = "update"
    QUERY = "query"
