import pytest
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux
from git_guardrails_test_helpers.git_test_utils import temp_dir
from git_guardrails.cli.color import strip_ansi

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_in_non_git_directory():
    with temp_dir() as dir:
        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, auto_fetch=True, cwd=dir))
            await do_validate(cli=cli, opts=opts)
            assert strip_ansi("".join(get_lines())) == f"""[ERROR]: git_guardrails is only intended for use within a git repository directory
{dir} does not seem to be a git repository
"""
