from dataclasses import dataclass


@dataclass
class TimeResponse:

    """
    Expose system time information.

    Attributes:
        adjusted_time (str): The adjusted time (system time + offset).
        offset_seconds (int): The current offset in seconds.
        system_time (str): The raw system time (without clock offset).
    """

    adjusted_time: str
    offset_seconds: int
    system_time: str

    @staticmethod
    def from_dict(time_response: dict):
        return TimeResponse(**time_response)
