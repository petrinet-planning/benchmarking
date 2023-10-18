
from .test_case import TestCase
from .time_measurement import TimeMeasurement


class BaseResult(object):
    test_case: TestCase
    output: dict[str, any]
    time: TimeMeasurement

    def __init__(
            self,
            test_case: TestCase,
            time: TimeMeasurement
        ) -> None:
            self.output = dict()
            self.test_case = test_case
            self.time = time

    def __repr__(self) -> str:
        return f"Result({self.time.__repr__()})"
    