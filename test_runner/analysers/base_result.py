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

    def parse_files(self, result_file_path: str, time_file_path: str, print_unfound_keys: bool = False) -> Optional["BaseResult"]:
        if not os.path.exists(result_file_path):
            return None
        if not os.path.exists(time_file_path):
            return None

        with open(result_file_path, "r") as result_file:
            with open(time_file_path, "r") as time_file:
                self.parse_result("".join(result_file.readlines()))
                self.parse_time("".join(time_file.readlines()))
        return self

    def parse_result(self, file_content: str, print_unfound_keys: bool = False) -> None:
        pass

    def parse_time(self, file_content: str) -> None:
        real = time_regexes["real"].search(file_content)
        user = time_regexes["user"].search(file_content)
        sys = time_regexes["sys"].search(file_content)

        self.time = TimeMeasurement(
            float(real[1]) * 60 + float(real[2]),
            float(user[1]) * 60 + float(user[2]),
            float(sys[1]) * 60 + float(sys[2])
        )
