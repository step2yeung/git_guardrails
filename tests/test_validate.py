from logging import INFO
from git.remote import Remote  # type: ignore
import pytest
from unittest.mock import patch
from git_guardrails.errors import GitRemoteConnectivityException
from git_guardrails.cli.color import strip_ansi
from git_guardrails.validate import do_validate
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux
from git_guardrails.validate.options import ValidateOptions
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails_test_helpers.git_test_utils import create_git_history, sorted_repo_branch_names
from git_guardrails_test_helpers.git_test_utils import temp_repo, temp_repo_clone
from git_guardrails.git_utils import git_default_branch


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@patch('builtins.input', return_value="continue")
async def test_review_branch_not_yet_pushed(mock_input):
    """
    Test case for a new review branch that does not yet track any remote branch
    (presumably, it hasn't yet been pushed)
    """
    with temp_repo() as upstream:
        merge_base = upstream.active_branch.commit
        assert merge_base is not None
        with temp_repo_clone(upstream) as downstream:
            new_branch = downstream.create_head("feature-123")
            new_branch.checkout()
            assert downstream.active_branch.name == "feature-123"
            create_git_history(downstream, [
                ([('my-file.txt', 'sample content')], 'second commit')
            ])
            assert downstream.heads['feature-123'] is not None
            downstream_default_branch = git_default_branch(downstream)
            assert downstream_default_branch == upstream.active_branch.name
            with fake_cliux(log_level=INFO) as (cli, get_lines):
                opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=downstream.working_dir))
                await do_validate(cli=cli, opts=opts)
                assert strip_ansi("".join(get_lines())) == """git_guardrails has completed without taking any action.

THERE'S NOTHING TO DO BECAUSE: BRANCH FEATURE-123 DOES NOT TRACK A REMOTE BRANCH
----------------------------------------
MORE INFORMATION
The currently active branch does not track a remote branch yet, perhaps you have not pushed it yet?

WHAT TO DO NEXT
- There is no reason to think anything is wrong, and no user action is required
"""


@patch('builtins.input', return_value="continue")
@patch('click.confirm', return_value="Y")
async def test_new_upstream_commits_to_pull_down(mock_input_a, mock_input_b):
    """
    Test case for "origin/review-branch has new commits that I must pull down"
    (no new local commits that origin doesn't have yet)
    """
    with temp_repo() as upstream:
        upstream_default_branch = upstream.active_branch
        upstream_feature_branch = upstream.create_head("feature-123")
        # upstream_feature_branch.checkout()
        with temp_repo_clone(upstream, ['feature-123']) as downstream:
            assert ", ".join(sorted_repo_branch_names(downstream)) == f"feature-123, {upstream_default_branch.name}"
            upstream_feature_branch.checkout()
            create_git_history(upstream, [
                ([('file_0.txt', 'content for file 0')], 'second commit'),
                ([('file_1.txt', 'content for file 1')], 'third commit'),
                ([('file_2.txt', 'content for file 2')], 'fourth commit'),
            ])
            upstream_default_branch.checkout()
            assert upstream.active_branch.name in ['main', 'master']
            downstream.heads['feature-123'].checkout()
            opts = ValidateOptions(ValidateCLIOptions(verbose=False, cwd=downstream.working_dir))
            assert opts.is_verbose() == False
            with fake_cliux(log_level=INFO) as (cli, get_lines):
                assert cli.log_level == INFO
                await do_validate(cli=cli, opts=opts)
                assert strip_ansi("".join(get_lines())) == """determined that local branch feature-123 tracks upstream branch feature-123 on remote origin
[WARNING]: New commits on origin/feature-123 were detected, which have not yet been pulled down to feature-123
Fetching new commits for branch origin/feature-123
Fetch from origin complete
"""


@patch('builtins.input', return_value="continue")
async def test_do_validate_no_remote(mock_input):
    """
    Test case for repo w/o any git remotes
    """
    with temp_repo() as upstream:
        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=upstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert strip_ansi("".join(get_lines())) == """git_guardrails has completed without taking any action.

THERE'S NOTHING TO DO BECAUSE: NO GIT REMOTES FOUND
----------------------------------------
MORE INFORMATION
git_guardrails validate is intended for use when pushing new code to a remote, and no remotes were found.

WHAT TO DO NEXT
- There is no reason to think anything is wrong, and no user action is required
"""


@patch('builtins.input', return_value="continue")
async def test_no_connect_to_remote(mock_input):
    """
    Test case for "can't connect to git remote"
    """
    with pytest.raises(GitRemoteConnectivityException):
        with temp_repo() as upstream:
            with temp_repo_clone(upstream) as downstream:
                downstream_origin: Remote = downstream.remotes['origin']
                assert downstream_origin is not None
                downstream_origin.set_url(new_url='https://example.com')
                with fake_cliux(log_level=INFO) as (cli, get_lines):
                    opts = ValidateOptions(ValidateCLIOptions(verbose=False, cwd=downstream.working_dir))
                    await do_validate(cli=cli, opts=opts)
                    assert strip_ansi("".join(get_lines())) == ""


@patch('builtins.input', return_value="continue")
async def test_push_from_default_branch(mock_input):
    """
    Test case for "push while on the default branch instead of a review branch"
    """
    with temp_repo() as upstream:
        with temp_repo_clone(upstream) as downstream:
            with fake_cliux(log_level=INFO) as (cli, get_lines):
                opts = ValidateOptions(ValidateCLIOptions(verbose=False, cwd=downstream.working_dir))
                await do_validate(cli=cli, opts=opts)
                assert strip_ansi("".join(get_lines())) == """git_guardrails has completed without taking any action.

THERE'S NOTHING TO DO BECAUSE: YOU ARE ON THE DEFAULT BRANCH (MASTER)
----------------------------------------
MORE INFORMATION
git_guardrails is intended to catch potential problems when pushing
review branches, and will not take any action when on a git repo's default branch

WHAT TO DO NEXT
- There is no reason to think anything is wrong, and no user action is required
"""
