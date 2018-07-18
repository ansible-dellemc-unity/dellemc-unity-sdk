#!/usr/bin/python
from enum import Enum

EXECUTED_BY = "executed_by"
EXECUTED_BY_SDK = "executed_by_sdk"
ACTION_TYPE = "action_type"
PARAMETER_TYPES = "parameter_types"
REST_OBJECT = "rest_object"
ACTIONS = "actions"
ACTION_NAME = "function"
DO_ACTION = "do_action"
GET = "get"
REST_OBJECT_FOR_GET_REQUEST = "rest_object_for_get"
PARAMETER_REQUIRED = "required"
PARAMETER_OPTIONAL = "optional"
PARAMETER_DEFAULT = "default"
PARAMETER_TYPE = "type"
VALIDATOR_RESULT = "result"
VALIDATOR_MESSAGE = "message"
UNITY_IP = "unityIP"
USERNAME = "username"
PASSWORD = "password"
ERR_MISSING_REQUIRED_PARAMETERS = "Required parameters: {} was not found."
ERR_UNSUPPORTED_PARAMETERS = "Parameters: {} are not supported."
ERR_WRONG_TYPE = "{} must be {}, not {}."


class ActionType(Enum):
    UPDATE = "update"
    QUERY = "query"
