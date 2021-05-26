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
    assert o.isVerbose() is True, "--verbose results in isVerbose() returning True"

    o2 = ValidateOptions(ValidateCLIOptions())
    assert o2.isVerbose() is False, "--verbose results in isVerbose() returning False"


def test_to_string():
    o = ValidateOptions(ValidateCLIOptions(verbose=True))
    assert str(o) == "ValidateOptions(cliOpts=ValidateCLIOptions(cwd=None, verbose=True, current_branch=None))"


async def test_to_dict():
    with temp_repo() as repo:
        o = ValidateOptions(ValidateCLIOptions(verbose=True, cwd="foo", current_branch="fizz"))
        d = await o.to_dict(repo)
        assert d["verbose"] == True
        assert d["cwd"] == "foo"
        assert d["current_branch"] == "fizz"


async def test_branch_name_passthrough():
    with temp_repo() as repo:
        repo.create_head("special_branch")
        repo.git.checkout("special_branch")
        o = ValidateOptions(ValidateCLIOptions(verbose=True, current_branch="fizz"))
        assert await o.getCurrentBranchName(repo) == "fizz", "--current-branch supercedes git repo state"


async def test_branch_name_infer():
    with temp_repo() as repo:
        repo.create_head("example_branch")
        repo.git.checkout("example_branch")
        o = ValidateOptions(ValidateCLIOptions())
        assert await o.getCurrentBranchName(repo) == "example_branch", "absence of --current-branch results in inference"


def test_cwd_passthrough():
    o = ValidateOptions(ValidateCLIOptions(cwd="/fizz"))
    assert o.getWorkingDirectory() == "/fizz"


def test_cwd_infer():
    o = ValidateOptions(ValidateCLIOptions())
    assert o.getWorkingDirectory() == getcwd(), "absence of --cwd results in inference"
