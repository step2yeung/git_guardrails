from logging import INFO, WARNING
from colorama import Fore, Style

from git_guardrails_test_helpers.logger_test_utils import fake_logger


def test_cli_logger():
    with fake_logger() as logger_wrapper:
        my_logger = logger_wrapper.logger

        my_logger.debug("hello world")
        my_logger.warning("zoom")

        log_lines = logger_wrapper.get_logged_output()

        assert len(log_lines) == 2, "two lines of output"
        assert log_lines[0] == f"{Style.DIM}[DEBUG]: hello world{Fore.RESET+Style.RESET_ALL}\n"
        assert log_lines[1] == f"{Fore.YELLOW}[WARNING]: zoom{Fore.RESET+Style.RESET_ALL}\n"


def test_logger_warn_log_level():
    with fake_logger(log_level=WARNING) as logger_wrapper:
        my_logger = logger_wrapper.logger

        my_logger.debug("hello world")
        my_logger.info("hello mars")
        my_logger.warning("zoom")
        my_logger.error("boom")

        log_lines = logger_wrapper.get_logged_output()
        assert len(log_lines) == 2, "one line of output"
        assert log_lines[0] == f"{Fore.YELLOW}[WARNING]: zoom{Fore.RESET+Style.RESET_ALL}\n"
        assert log_lines[1] == f"{Fore.RED}[ERROR]: boom{Fore.RESET+Style.RESET_ALL}\n"


def test_logger_error_log_level():
    with fake_logger(log_level=WARNING) as logger_wrapper:
        my_logger = logger_wrapper.logger

        my_logger.debug("hello world")
        my_logger.info("hello mars")
        my_logger.warning("zoom")
        my_logger.error("boom")

        log_lines = logger_wrapper.get_logged_output()
        assert len(log_lines) == 2, "one line of output"
        assert log_lines[0] == f"{Fore.YELLOW}[WARNING]: zoom{Fore.RESET+Style.RESET_ALL}\n"
        assert log_lines[1] == f"{Fore.RED}[ERROR]: boom{Fore.RESET+Style.RESET_ALL}\n"


def test_logger_info_log_level():
    with fake_logger(log_level=INFO) as logger_wrapper:
        my_logger = logger_wrapper.logger

        my_logger.debug("hello world")
        my_logger.info("hello mars")
        my_logger.warning("zoom")

        log_lines = logger_wrapper.get_logged_output()

        assert len(log_lines) == 2, "two lines of output"
        assert log_lines[0] == f"hello mars{Fore.RESET+Style.RESET_ALL}\n"
        assert log_lines[1] == f"{Fore.YELLOW}[WARNING]: zoom{Fore.RESET+Style.RESET_ALL}\n"

