from re import split
from colorama import Fore, Style, Back
from git.objects.commit import Commit

TOTAL_RESET = Style.RESET_ALL + Fore.RESET + Back.RESET


def __format_string(val: str, color: str, return_to_color) -> str:
    return f"{color}{val}{return_to_color}"


def format_branch_name(name: str, return_to_color=TOTAL_RESET) -> str:
    return __format_string(name, Fore.YELLOW, return_to_color)


def format_cli_command(cmd: str, return_to_color=TOTAL_RESET) -> str:
    return __format_string(cmd, Back.BLACK + Fore.GREEN, return_to_color)


def format_integer(num: int, return_to_color=TOTAL_RESET) -> str:
    return __format_string(f"{num}", Fore.LIGHTGREEN_EX, return_to_color)


def format_sha(sha: str, return_to_color=TOTAL_RESET) -> str:
    return __format_string(f"{sha[0:8]}", Fore.MAGENTA, return_to_color)


def format_commit(c: Commit, return_to_color=TOTAL_RESET) -> str:
    lines = split("\n", c.message)
    return f"""{format_sha(c.hexsha)} {Fore.LIGHTBLUE_EX} < {c.author.email} > {Fore.WHITE} - {
        Style.DIM}{lines[0][0:30]}{return_to_color}"""
