from unittest.mock import patch
from git_guardrails.cli.color import strip_ansi
from git_guardrails.errors import NonApplicableSituationException
from git_guardrails.errors import UnhandledSituationException
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux


def test_non_applicable_situation_exception():
    with fake_cliux() as (cli, get_lines):
        try:
            raise NonApplicableSituationException(
                situation_title="Example title",
                situation_details="Some example details")
        except NonApplicableSituationException as ex:
            cli.handle_non_applicable_situation_exception(ex)
            log_lines = "".join(get_lines())
            assert strip_ansi(log_lines) == """git_guardrails has completed without taking any action.

THERE'S NOTHING TO DO BECAUSE: EXAMPLE TITLE
----------------------------------------
MORE INFORMATION
Some example details

WHAT TO DO NEXT
- There is no reason to think anything is wrong, and no user action is required
"""


@patch('builtins.input', return_value="continue")
def test_unhandled_situation_exception_user_continue(_mock_input):
    with fake_cliux() as (cli, get_lines):
        try:
            raise UnhandledSituationException(
                situation_title="Example title",
                situation_details="Some example details")
        except UnhandledSituationException as ex:
            cli.handle_unhandled_situation_exception(ex, retry_prompt=False)
            log_lines = "".join(get_lines())
            assert strip_ansi(log_lines) == """[WARNING]: git_guardrails found your workspace in an unexpected state

UNEXPECTED WORKSPACE STATE: EXAMPLE TITLE
----------------------------------------
MORE INFORMATION
Some example details

WHAT TO DO NEXT
- You may choose to proceed at your own risk
- You may abort by pressing Ctrl + C
[WARNING]: Proceeding at user's request
"""


@patch('builtins.input', return_value="retry, I am not sure")
def test_unhandled_situation_exception_user_invalid_response(_mock_input):
    with fake_cliux() as (cli, get_lines):
        try:
            raise UnhandledSituationException(
                situation_title="Example title",
                situation_details="Some example details")
        except UnhandledSituationException as ex:
            cli.handle_unhandled_situation_exception(ex, retry_prompt=False)
            log_lines = "".join(get_lines())
            assert strip_ansi(log_lines) == """[WARNING]: git_guardrails found your workspace in an unexpected state

UNEXPECTED WORKSPACE STATE: EXAMPLE TITLE
----------------------------------------
MORE INFORMATION
Some example details

WHAT TO DO NEXT
- You may choose to proceed at your own risk
- You may abort by pressing Ctrl + C
[ERROR]: invalid user response. Please either abort by pressing Ctrl+C or proceed by typing CONTINUE
"""
