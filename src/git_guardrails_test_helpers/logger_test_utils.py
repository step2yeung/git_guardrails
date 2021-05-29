from contextlib import contextmanager
from logging import DEBUG, Logger
import tempfile
from typing import Callable, IO, Iterator, List, Tuple
from git_guardrails.cli.logging import create_cli_logger


def rewind_and_print_lines(file: IO[str]) -> List[str]:
    file.seek(0) 
    return file.readlines()

@contextmanager
def fake_logger(log_level: int = DEBUG) -> Iterator[Tuple[Logger, Callable[[], List[str]]]]:
    with tempfile.TemporaryFile("r+") as temp_file:
        my_logger = create_cli_logger(log_level=log_level, outstream=temp_file)
        yield my_logger, lambda: rewind_and_print_lines(temp_file)

