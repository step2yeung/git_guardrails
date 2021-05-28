from colorama import Fore, Style
import logging

LEVEL_NAMES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LEVEL_COLORS = {
    "DEBUG": Style.DIM,
    "INFO": '',
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED
}
LEVEL_SHOW_LABEL = {
    "DEBUG": False,
    "INFO": False,
    "WARNING": True,
    "ERROR": True,
    "CRITICAL": True
}
RESET_SEQ = Fore.RESET + Style.RESET_ALL


class ColoredFormatter(logging.Formatter):
    def __init__(self, supports_color: bool, format_string: str, verbose: bool):
        self.is_verbose = verbose
        # logging.Formatter.__init__(self, "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logging.Formatter.__init__(self, format_string)
        self.use_color = supports_color

    def format(self, record: logging.LogRecord):
        levelname = record.levelname
        if self.use_color and levelname in LEVEL_COLORS:
            formatted_level_name = f"[{levelname}]: " if LEVEL_SHOW_LABEL[levelname] or self.is_verbose else ""
            colorized_level_name = f"{LEVEL_COLORS[levelname]}{formatted_level_name}"
            record.levelname = colorized_level_name
            record.msg = f"{colorized_level_name}{record.msg}{RESET_SEQ}"
        return logging.Formatter.format(self, record)
