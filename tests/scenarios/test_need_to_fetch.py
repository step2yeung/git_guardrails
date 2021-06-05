from logging import INFO
from unittest.mock import patch
from git.refs.head import Head  # type: ignore
import pytest
from contextlib import contextmanager
from typing import Iterator, Tuple
from git.repo.base import Repo  # type: ignore
from git_guardrails.cli.color import strip_ansi
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux
from git_guardrails_test_helpers.git_test_utils import temp_repo, create_git_history  # type: ignore
from git_guardrails_test_helpers.git_test_utils import commit_all_modified_tracked_files, temp_repo_clone   # type: ignore


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@contextmanager
def setup_need_to_fetch_scenario() -> Iterator[Tuple[Repo, Repo]]:
    with temp_repo() as upstream:
        # Create some commit activity on origin/master
        commit_all_modified_tracked_files(upstream, "initial commit")
        # Create a review branch and check it out
        upstream_default_branch = upstream.active_branch
        upstream_review999 = upstream.create_head('review-999')
        upstream_review999.checkout()
        # Create some commit history on origin/review-999
        create_git_history(upstream, [
            ([('hello1.txt', 'hello world!')], 'second commit'),
            ([('hello2.txt', 'hello world!')], 'third commit'),
            ([('hello3.txt', 'hello world!')], 'fourth commit'),
            ([('hello4.txt', 'hello world!')], 'fifth commit'),
        ])
        # Switch back to origin/master
        upstream_default_branch.checkout()
        # Create a "downstream" clone of the repo. This would be the user's working copy
        with temp_repo_clone(upstream, ['review-999']) as downstream:
            # Make sure the downstream clone is initially on the default branch
            assert downstream.active_branch.name in ['main', 'master']
            # Make sure the downstream clone has a local copy of the review branch
            downstream_review999 = downstream.heads['review-999']
            assert downstream_review999 is not None
            # Create some new commits on origin/review-999
            upstream_review999.checkout()
            create_git_history(upstream, [
                ([('hello5.txt', 'hello world! 21')], 'purple commit'),
                ([('hello6.txt', 'hello world! 22')], 'brown commit'),
                ([('hello7.txt', 'hello world! 23')], 'yellow commit'),
                ([('hello8.txt', 'hello world! 24')], 'orange commit'),
            ])
            upstream_default_branch.checkout()
            yield (upstream, downstream)


@patch('builtins.input', return_value='Y')
async def test_need_to_fetch_only_upstream_commits(mock_input):
    with setup_need_to_fetch_scenario() as (upstream, downstream):
        assert upstream.is_dirty() == False
        downstream.heads['review-999'].checkout()
        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, auto_fetch=True, cwd=downstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert "[WARNING]: New commits on origin/review-999 were detected" in strip_ansi(
                "".join(get_lines()))


@patch('builtins.input', return_value='N')
async def test_need_to_fetch_only_upstream_commits_user_refuses(mock_input):
    with setup_need_to_fetch_scenario() as (upstream, downstream):
        assert upstream.is_dirty() == False
        downstream.heads['review-999'].checkout()
        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, auto_fetch=False, cwd=downstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert strip_ansi(
                "".join(get_lines())) == """determined that local branch review-999 tracks upstream branch review-999 on remote origin
[WARNING]: New commits on origin/review-999 were detected, which have not yet been pulled down to review-999
git_guardrails has completed without taking any action.

USER BYPASS
----------------------------------------
MORE INFORMATION
The user decided to bypass git_guardrails (user decided not to download new commits from origin/review-999)
"""


@patch('builtins.input', return_value='Y')
async def test_need_to_fetch_upstream_and_downstream_commits(mock_input):
    with setup_need_to_fetch_scenario() as (upstream, downstream):
        assert upstream.is_dirty() == False
        review_branch: Head = downstream.heads['review-999']
        review_branch.checkout()
        tracked_branch: Head = review_branch.tracking_branch()
        head_before_fetch = tracked_branch.commit
        assert head_before_fetch.hexsha == tracked_branch.commit.hexsha
        with fake_cliux(log_level=INFO) as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=False, auto_fetch=True, cwd=downstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert strip_ansi("".join(get_lines())) == """determined that local branch review-999 tracks upstream branch review-999 on remote origin
[WARNING]: New commits on origin/review-999 were detected, which have not yet been pulled down to review-999
Fetching new commits for branch origin/review-999
Fetch from origin complete
"""
            assert head_before_fetch.hexsha != tracked_branch.commit.hexsha, 'New commits have been pulled down'
