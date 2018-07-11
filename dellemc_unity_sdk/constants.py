#!/usr/bin/python
from enum import Enum

EXECUTED_BY_KEY = "executed_by"  # TODO: remove later
EXECUTED_BY = "executed_by"
EXECUTED_BY_SDK = "executed_by_sdk"
ACTION_TYPE_KEY = "action_type"
PARAMETER_TYPES_KEY = "parameter_types"
REST_OBJECT_KEY = "rest_object"  # TODO: remove later
REST_OBJECT = "rest_object"
ACTIONS_KEY = "actions"  # TODO: remove later
ACTIONS = "actions"
ACTION_NAME = "function"
DO_ACTION = "do_action"
GET = "get"
REST_OBJECT_FOR_GET_REQUEST = "rest_object_for_get"


class ActionType(Enum):
    UPDATE = "update"
    QUERY = "query"
