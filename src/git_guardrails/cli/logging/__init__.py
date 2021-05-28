import logging
import sys
from typing import TextIO

from git_guardrails.cli.logging.colored_formatter import ColoredFormatter


def create_cli_logger(log_level: int, outstream: TextIO = sys.stdout) -> logging.Logger:
    logger = logging.Logger("git_guardrails", level=log_level)
    console_handler = logging.StreamHandler(outstream)
    console_handler.setLevel(log_level)
    console_formatter = ColoredFormatter(
        supports_color=True,
        verbose=(log_level == logging.DEBUG),
        format_string="%(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    return logger
