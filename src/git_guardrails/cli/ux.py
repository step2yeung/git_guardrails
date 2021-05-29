from colorama import init as initColorama, Style, Fore
from git_guardrails.cli.logging import create_cli_logger
from git_guardrails.errors import NonApplicableSituationException, UnhandledSituationException

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

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def handle_non_applicable_situation_exception(self, ex: NonApplicableSituationException):
        self.info(f"""git_guardrails has completed without taking any action.

{str(ex)}""")

    def handle_unhandled_situation_exception(self, ex: UnhandledSituationException):
        while(True):
            user_response = ''
            self.warning(f"""git_guardrails found your workspace in an unexpected state

{str(ex)}""")
            user_response = input(f"""
{Fore.CYAN}Please type CONTINUE to proceed, or hit Ctrl+C to abort{Fore.RESET}
{Style.BRIGHT}>{Style.RESET_ALL} """)
            if (user_response.lower() == "continue"):
                self.warning("Proceeding at user's request")
                return
            else:
                self.error("invalid user response. Please either abort by pressing Ctrl+C or proceed by typing CONTINUE")
