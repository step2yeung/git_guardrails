from colorama import init as initColorama, Style, Fore
from git_guardrails.cli.logging import create_cli_logger

initColorama()


def generate_welcome_banner():
    return ''.join(
        [
            Style.DIM, "|===|===|===|==", Style.RESET_ALL,
            Fore.LIGHTCYAN_EX, " Git Guardrails ", Fore.RESET,
            Style.DIM, "==|===|===|===|", Style.RESET_ALL
        ]
    )


class CLIUX:
    def __init__(self, supports_color: bool, supports_tty: bool, log_level: int):
        self.log_level = log_level
        self.supports_color = supports_color
        self.supports_tty = supports_tty
        self.logger = create_cli_logger(log_level=log_level)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
