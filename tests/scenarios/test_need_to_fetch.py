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
from git_guardrails_test_helpers.git_test_utils import commit_all_modified_tracked_files, create_temp_clone   # type: ignore


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
        with create_temp_clone(upstream, ['review-999']) as downstream:
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


async def test_need_to_fetch_only_upstream_commits():
    with setup_need_to_fetch_scenario() as (upstream, downstream):
        assert upstream.is_dirty() == False
        downstream.heads['review-999'].checkout()
        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=downstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert "[WARNING]: New commits on origin/review-999 were detected" in strip_ansi(
                "".join(get_lines()))


async def test_need_to_fetch_upstream_and_downstream_commits():
    with setup_need_to_fetch_scenario() as (upstream, downstream):
        assert upstream.is_dirty() == False
        downstream.heads['review-999'].checkout()
        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=downstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert "[WARNING]: New commits on origin/review-999 were detected" in strip_ansi(
                "".join(get_lines()))
