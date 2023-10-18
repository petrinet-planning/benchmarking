
class TimeMeasurement(object):
    seconds_real: float
    seconds_user: float
    seconds_system: float

    def __init__(
            self,
            seconds_real: float,
            seconds_user: float,
            seconds_system: float
        ) -> None:
            self.seconds_real = seconds_real
            self.seconds_user = seconds_user
            self.seconds_system = seconds_system

