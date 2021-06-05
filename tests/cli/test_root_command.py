import pytest
from click.testing import CliRunner
from git_guardrails.command_line import main, validate
import git_guardrails.__main__  # noqa


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


def test_root_entry():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert result.output == """Usage: main [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  validate  Examine the current Git workspace and perform some sanity-checking
"""


def test_validate_help():
    runner = CliRunner()
    result = runner.invoke(validate, ['--help'])
    assert result.exit_code == 0
    assert result.output == """Usage: validate [OPTIONS]

  Examine the current Git workspace and perform some sanity-checking

Options:
  -v, --verbose / --no-verbose    extra logging
  --cwd TEXT                      directory to examine (the git repo)
  --current-branch TEXT           name of branch to treat as 'the PR'
  --color / --no-color            terminal color support
  --tty / --no-tty                terminal TTY support
  --auto-fetch / --no-auto-fetch  automatically fetch new upstream commits
  --commit-count-soft-fail-threshold INTEGER
                                  # of new local branch commits before the user
                                  is warned  [default: 80]
  --commit-count-hard-fail-threshold INTEGER
                                  # of new local branch commits before the user
                                  is stopped  [default: 40]
  -h, --help                      Show this message and exit.
"""


def test_validate_not_enabled():
    runner = CliRunner()
    result = runner.invoke(validate, ['--no-enabled'])
    assert result.exit_code == 0
    assert result.output == """skipping validation, due to '--no-enabled' CLI arg, or GIT_GUARDRAILS_ENABLED=False env variable
"""
