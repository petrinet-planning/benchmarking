import os.path
import re
from typing import Optional

from ..time_measurement import TimeMeasurement

time_regexes: dict[str, re.Pattern] = {
    "real": re.compile(r"^real\t(\d+)m(\d+\.\d+)s", re.MULTILINE),
    "user": re.compile(r"^user\t(\d+)m(\d+\.\d+)s", re.MULTILINE),
    "sys": re.compile(r"^sys\t(\d+)m(\d+\.\d+)s", re.MULTILINE),
}


class BaseResult(object):
    time: TimeMeasurement

    def parse(self, result_file_path: str, test_case: "TestCase", print_unfound_keys: bool = False) -> Optional["BaseResult"]:
        with open(result_file_path, "r") as result_file:
            filecontent = "".join(result_file.readlines())
            self.parse_result(filecontent, test_case)
            self.parse_time(filecontent)
        return self

    def parse_result(self, file_content: str, test_case: "TestCase", print_unfound_keys: bool = False) -> None:
        pass

    def parse_time(self, file_content: str) -> None:
        real = time_regexes["real"].search(file_content)
        user = time_regexes["user"].search(file_content)
        sys = time_regexes["sys"].search(file_content)

        self.time = TimeMeasurement(
            (float(real[1]) * 60 + float(real[2])) if real is not None else float("inf"),
            (float(user[1]) * 60 + float(user[2])) if user is not None else float("inf"),
            (float(sys[1]) * 60 + float(sys[2]))   if sys is not None else float("inf")
        )
