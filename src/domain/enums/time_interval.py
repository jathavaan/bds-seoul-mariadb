from enum import Enum


class TimeInterval(Enum):
    ZERO_TO_FORTY_NINE = 0
    FIFTY_TO_NINETY_NINE = 1
    HUNDRED_TO_HUNDRED_NINETY_NINE = 2
    TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE = 3
    FIVE_HUNDRED_PLUS = 4

    @classmethod
    def from_value(cls, value: str) -> "TimeInterval":
        match value:
            case "0-49":
                return cls.ZERO_TO_FORTY_NINE
            case "50-99":
                return cls.FIFTY_TO_NINETY_NINE
            case "100-199":
                return cls.HUNDRED_TO_HUNDRED_NINETY_NINE
            case "200-499":
                return cls.TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE
            case "500+":
                return cls.FIVE_HUNDRED_PLUS
            case _:
                raise ValueError(f"No TimeInterval matches value: {value}")
