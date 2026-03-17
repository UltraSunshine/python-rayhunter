from enum import IntEnum


class NotificationType(IntEnum):

    """
    Enum of valid notification types.
    """

    Warning = 0
    LowBattery = 1