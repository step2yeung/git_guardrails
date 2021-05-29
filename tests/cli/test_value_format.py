from git_guardrails.cli.color import strip_ansi
from git_guardrails.cli.value_format import TOTAL_RESET, format_branch_name
from git_guardrails.cli.value_format import format_cli_command, format_commit, format_integer, format_sha
from colorama import Fore, Back
from git_guardrails_test_helpers import git_test_utils


def test_format_branch_name():
    assert format_branch_name("foo") == f"{Fore.YELLOW}foo{TOTAL_RESET}"


def test_format_sha():
    assert format_sha("foo") == f"{Fore.MAGENTA}foo{TOTAL_RESET}"


def test_format_cli_command():
    assert format_cli_command("ls") == f"{Back.BLACK + Fore.GREEN}ls{TOTAL_RESET}"


def test_format_integer():
    assert format_integer(61) == f"{Fore.LIGHTGREEN_EX}61{TOTAL_RESET}"


def test_format_commit():
    with git_test_utils.temp_repo() as repo:
        repo.index.commit("first commit")
        commit = repo.active_branch.commit
        assert strip_ansi(format_commit(commit)) == f"{commit.hexsha[0:8]} <{commit.author.email}> - first commit"
