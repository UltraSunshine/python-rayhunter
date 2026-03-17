from enum import IntEnum


class Device(IntEnum):

    """
    An enumeration of the internal names of currently implemented devices.
    """

    orbic = 0
    tplink = 1
    tmobile = 2
    wingtech = 3
    pinephone = 4
    us801 = 5
