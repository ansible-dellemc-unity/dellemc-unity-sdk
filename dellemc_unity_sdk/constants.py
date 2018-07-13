#!/usr/bin/python
from enum import Enum

EXECUTED_BY = "executed_by"
EXECUTED_BY_KEY = EXECUTED_BY  # TODO: remove later
EXECUTED_BY_SDK = "executed_by_sdk"
ACTION_TYPE_KEY = "action_type"
PARAMETER_TYPES = "parameter_types"
PARAMETER_TYPES_KEY = PARAMETER_TYPES
REST_OBJECT = "rest_object"
REST_OBJECT_KEY = REST_OBJECT  # TODO: remove later
ACTIONS = "actions"
ACTIONS_KEY = ACTIONS  # TODO: remove later
ACTION_NAME = "function"
DO_ACTION = "do_action"
GET = "get"
REST_OBJECT_FOR_GET_REQUEST = "rest_object_for_get"
VALIDATOR_RESULT = "result"
VALIDATOR_MESSAGE = "message"
ERR_MISSING_REQUIRED_PARAMETER = "Required parameter {} was not found."
ERR_UNSUPPORTED_PARAMETER = "{} is unsupported parameter"
ERR_WRONG_TYPE = "{} must be {}, not {}"

class ActionType(Enum):
    UPDATE = "update"
    QUERY = "query"
