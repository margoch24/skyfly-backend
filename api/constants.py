from enum import Enum

from api.helpers.request_validator import (
    BodyRequestValidator,
    QueryRequestValidator,
    RequestValidatorTypes,
)

DEFAULT_LIMIT = 50

REQUEST_VALIDATOR_CLASSES = {
    RequestValidatorTypes.Body: BodyRequestValidator,
    RequestValidatorTypes.Query: QueryRequestValidator,
}


class CabinClass:
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"


class Scheduled:
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class SeatType:
    AISLE = "aisle"
    WINDOW = "window"


class Environment:
    TEST = "test"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


SEATS_DATA = [
    {
        "row": 1,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 1,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 1,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 1,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 2,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 2,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 2,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 2,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 3,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 3,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 3,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 3,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 4,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 4,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 4,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 4,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 5,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 5,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 5,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 5,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.FIRST,
    },
    {
        "row": 6,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 6,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 6,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 6,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 7,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 7,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 7,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 7,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 8,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 8,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 8,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 8,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 9,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 9,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 9,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 9,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 10,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 10,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 10,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 10,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 11,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 11,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 11,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 11,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 12,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 12,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 12,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 12,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 13,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 13,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 13,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 13,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 14,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 14,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 14,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 14,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 15,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 15,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 15,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 15,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.BUSINESS,
    },
    {
        "row": 16,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 16,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 16,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 16,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 17,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 17,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 17,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 17,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 18,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 18,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 18,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 18,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 19,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 19,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 19,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 19,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 20,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 20,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 20,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 20,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 21,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 21,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 21,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 21,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 22,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 22,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 22,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 22,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 23,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 23,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 23,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 23,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 24,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 24,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 24,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 24,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 25,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 25,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 25,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 25,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 26,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 26,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 26,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 26,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 27,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 27,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 27,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 27,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 28,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 28,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 28,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 28,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 29,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 29,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 29,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 29,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 30,
        "column": "A",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 30,
        "column": "B",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 30,
        "column": "C",
        "type": SeatType.AISLE,
        "cabin_class": CabinClass.ECONOMY,
    },
    {
        "row": 30,
        "column": "D",
        "type": SeatType.WINDOW,
        "cabin_class": CabinClass.ECONOMY,
    },
]
