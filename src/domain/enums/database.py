from enum import Enum







# entity for subscription and enum of subscription type
class SubscriptionType(Enum):
    PREMIUM = "premium"
    PLUS = "plus"



# entity for unregistered device and device`s os type

class DeviceType(Enum):
    Ios = "ios"
    Android = "android"