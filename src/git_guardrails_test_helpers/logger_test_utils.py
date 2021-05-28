from contextlib import contextmanager
from logging import DEBUG, Logger
import tempfile
from typing import IO, Iterator
from git_guardrails.cli.logging import create_cli_logger


class FakeLoggerWrapper:
    def __init__(self, logger: Logger, tmp_file: IO[str]):
        self.logger = logger
        self.__tmp_file = tmp_file

    def get_logged_output(self) -> list[str]:
        self.__tmp_file.seek(0)
        return self.__tmp_file.readlines()


@contextmanager
def fake_logger(log_level: int = DEBUG) -> Iterator[FakeLoggerWrapper]:
    with tempfile.TemporaryFile("r+") as temp_file:
        my_logger = create_cli_logger(log_level=log_level, outstream=temp_file)
        fake_logger_wrapper = FakeLoggerWrapper(logger=my_logger, tmp_file=temp_file)
        yield fake_logger_wrapper
