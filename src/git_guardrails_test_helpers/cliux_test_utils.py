
from contextlib import contextmanager
from typing import Callable, Iterator, List, Tuple

from logging import DEBUG
from git_guardrails_test_helpers.logger_test_utils import fake_logger
from git_guardrails.cli.ux import CLIUX


@contextmanager
def fake_cliux(
    supports_color: bool = False,
    supports_tty: bool = False,
    log_level: int = DEBUG
) -> Iterator[Tuple[CLIUX, Callable[[], List[str]]]]:
    with fake_logger() as (my_logger, get_lines):
        cli = CLIUX(
            supports_color=supports_color,
            supports_tty=supports_tty,
            log_level=log_level,
            logger=my_logger)
        yield cli, get_lines
