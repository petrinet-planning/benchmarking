from .base_result import BaseResult
from . import TimeMeasurement, TestCase


class TranslationResult(BaseResult):
    test_case: TestCase
    time: TimeMeasurement
    output_directory: str

    def __init__(
            self,
            test_case: TestCase,
            time: TimeMeasurement,
            output_directory: str
        ) -> None:
            super().__init__(test_case, time)
            self.output_directory = output_directory
