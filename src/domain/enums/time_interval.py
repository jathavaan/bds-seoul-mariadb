from enum import Enum


class TimeInterval(Enum):
    ZERO_TO_FORTY_NINE = "0-49"
    FIFTY_TO_NINETY_NINE = "50-99"
    HUNDRED_TO_HUNDRED_NINETY_NINE = "100-199"
    TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE = "200-499"
    FIFE_HUNDRED_PLUS = "500+"

    @classmethod
    def from_value(cls, value: str) -> "TimeInterval":
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"No TimeInterval matches value: {value}")
