import pytest
from git_guardrails_test_helpers.git_test_utils import temp_repo
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


def test_creation():
    cli_opts = ValidateCLIOptions(True, None, None)
    o = ValidateOptions(cli_opts)
    assert o is not None, "Creation of Options instance is successful"


def test_verbosity_passthrough():
    cli_opts = ValidateCLIOptions(True, None, None)
    o = ValidateOptions(cli_opts)
    assert o.isVerbose() is True, "--verbose results in isVerbose() returning True"

    cli_opts2 = ValidateCLIOptions(False, None, None)
    o2 = ValidateOptions(cli_opts2)
    assert o2.isVerbose() is False, "--verbose results in isVerbose() returning False"


async def test_branch_name_passthrough():
    with temp_repo() as repo:
        cli_opts = ValidateCLIOptions(True, None, "fizz")
        o = ValidateOptions(cli_opts)
        assert await o.getCurrentBranchName(repo) == "fizz", "--current-branch supercedes git repo state"


async def test_branch_name_infer():
    with temp_repo() as repo:
        cli_opts = ValidateCLIOptions(True, None, None)
        o = ValidateOptions(cli_opts)
        assert await o.getCurrentBranchName(repo) in ["main", "master"], "absence of --current-branch results in inference"
