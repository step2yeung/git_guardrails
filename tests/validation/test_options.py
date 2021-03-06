import pytest
from git_guardrails_test_helpers.git_test_utils import temp_repo
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions
from os import getcwd


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


def test_creation():
    o = ValidateOptions(ValidateCLIOptions())
    assert o is not None, "Creation of Options instance is successful"


def test_verbosity_passthrough():
    o = ValidateOptions(ValidateCLIOptions(verbose=True))
    assert o.is_verbose() is True, "--verbose results in isVerbose() returning True"

    o2 = ValidateOptions(ValidateCLIOptions())
    assert o2.is_verbose() is False, "--verbose results in isVerbose() returning False"


def test_to_string():
    o = ValidateOptions(ValidateCLIOptions(verbose=True))
    assert str(o) == "ValidateOptions(cliOpts=ValidateCLIOptions(cwd=None, verbose=True, current_branch=None))"


async def test_to_dict():
    with temp_repo() as repo:
        repo.index.commit("first commit")
        o = ValidateOptions(ValidateCLIOptions(verbose=True, cwd="foo", current_branch="fizz"))
        d = await o.to_dict(repo)
        assert d["verbose"] == True
        assert d["cwd"] == "foo"
        assert d["current_branch"] == "fizz"


async def test_branch_name_passthrough():
    with temp_repo() as repo:
        repo.index.commit("first commit")
        repo.create_head("special_branch")
        repo.git.checkout("special_branch")
        o = ValidateOptions(ValidateCLIOptions(verbose=True, current_branch="fizz"))
        assert await o.get_current_branch_name(repo) == "fizz", "--current-branch supercedes git repo state"


async def test_branch_name_infer():
    with temp_repo() as repo:
        repo.index.commit("first commit")
        repo.create_head("example_branch")
        repo.git.checkout("example_branch")
        o = ValidateOptions(ValidateCLIOptions())
        assert await o.get_current_branch_name(repo) == "example_branch", "absence of --current-branch results in inference"


def test_color_arg_passthrough():
    o1 = ValidateOptions(ValidateCLIOptions(color=True))
    assert o1.is_terminal_color_supported() == True, "--color passes through correctly in ValidateOptions (True)"
    o2 = ValidateOptions(ValidateCLIOptions(color=False))
    assert o2.is_terminal_color_supported() == False, "--color passes through correctly in ValidateOptions (False)"


def test_color_arg_infer():
    """
    absence of --color argument results in inference
    """
    o = ValidateOptions(ValidateCLIOptions())

    callback_invocation_count = 0

    def fake_color_detector() -> bool:
        nonlocal callback_invocation_count
        callback_invocation_count += 1
        return True

    def fake_no_color_detector() -> bool:
        nonlocal callback_invocation_count
        callback_invocation_count += 1
        return False

    assert callback_invocation_count == 0
    assert o.is_terminal_color_supported(fake_color_detector) == True
    assert callback_invocation_count == 1
    assert o.is_terminal_color_supported(fake_no_color_detector) == False
    assert callback_invocation_count == 2


def test_tty_arg_passthrough():
    o1 = ValidateOptions(ValidateCLIOptions(tty=True))
    assert o1.is_terminal_tty_supported() == True, "--tty passes through correctly in ValidateOptions (True)"
    o2 = ValidateOptions(ValidateCLIOptions(tty=False))
    assert o2.is_terminal_tty_supported() == False, "--tty passes through correctly in ValidateOptions (False)"


def test_tty_arg_infer():
    """
    absence of --tty argument results in inference
    """
    o = ValidateOptions(ValidateCLIOptions())

    callback_invocation_count = 0

    def fake_tty_detector() -> bool:
        nonlocal callback_invocation_count
        callback_invocation_count += 1
        return True

    def fake_no_tty_detector() -> bool:
        nonlocal callback_invocation_count
        callback_invocation_count += 1
        return False

    assert callback_invocation_count == 0
    assert o.is_terminal_tty_supported(fake_tty_detector) == True
    assert callback_invocation_count == 1
    assert o.is_terminal_tty_supported(fake_no_tty_detector) == False
    assert callback_invocation_count == 2


def test_cwd_passthrough():
    o = ValidateOptions(ValidateCLIOptions(cwd="/fizz"))
    assert o.get_cwd() == "/fizz"


def test_cwd_infer():
    o = ValidateOptions(ValidateCLIOptions())
    assert o.get_cwd() == getcwd(), "absence of --cwd results in inference"
