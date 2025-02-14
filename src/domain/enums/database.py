from enum import Enum



# entity for subscription and enum of subscription type
class SubscriptionType(Enum):
    PREMIUM = "premium"
    PLUS = "plus"


class DeviceType(Enum):
    Ios = "ios"
    Android = "android"


class CurencyType(Enum):
    EUR = "EUR"
    USD = "USD"
    UAH = "UAH"

class PeriodTypeEnum(Enum):
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class TransactionsStatusEnum(Enum):
    IN_PROCESS = "IN_PROCESS"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    TEST = "TEST"