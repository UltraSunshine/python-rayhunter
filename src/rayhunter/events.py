from enum import IntEnum


class EventType(IntEnum):

    """
    The severity level of an event.
    """

    Informational = 0
    Low = 1
    Medium = 2
    High = 3
