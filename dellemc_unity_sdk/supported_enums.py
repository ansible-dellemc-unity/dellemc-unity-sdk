from enum import IntEnum


class HostTypeEnum(IntEnum):
    UNKNOWN = 0
    HOSTMANUAL = 1
    SUBNET = 2
    NETGROUP = 3
    RPA = 4
    HOSTAUTO = 5
    VNXSANCOPY = 255
