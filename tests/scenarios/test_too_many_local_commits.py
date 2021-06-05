from logging import INFO
import pytest
from git_guardrails.errors import LikelyUserErrorException
from git_guardrails.cli.color import strip_ansi
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions
from git_guardrails_test_helpers.git_test_utils import create_git_history, temp_repo, temp_repo_clone
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_review_branch_commit_count_soft_fail():
    with temp_repo() as upstream:
        upstream_default_branch = upstream.active_branch
        upstream.create_head('mnorth-review-111')
        create_git_history(upstream, [
            (("demo_0.txt", "content for demo_0"), "demo 0 commit"),
            (("demo_1.txt", "content for demo_1"), "demo 1 commit"),
            (("demo_2.txt", "content for demo_2"), "demo 2 commit"),
            (("demo_3.txt", "content for demo_3"), "demo 3 commit"),
        ])
        upstream_default_branch.checkout()
        with temp_repo_clone(upstream, ['mnorth-review-111']) as downstream:
            # downstream_default_branch = downstream.active_branch
            downstream_review_branch = downstream.heads['mnorth-review-111']
            assert downstream_review_branch is not None
            downstream_review_branch.checkout()
            create_git_history(downstream, [
                (("demo_4.txt", "content for demo_4"), "demo 4 commit"),
                (("demo_5.txt", "content for demo_5"), "demo 5 commit"),
                (("demo_6.txt", "content for demo_6"), "demo 6 commit"),
                (("demo_7.txt", "content for demo_7"), "demo 7 commit"),
                (("demo_8.txt", "content for demo_8"), "demo 8 commit"),
                (("demo_9.txt", "content for demo_9"), "demo 9 commit"),
                (("demo_10.txt", "content for demo_10"), "demo 10 commit"),
                (("demo_11.txt", "content for demo_11"), "demo 11 commit"),
                (("demo_12.txt", "content for demo_12"), "demo 12 commit"),
                (("demo_13.txt", "content for demo_13"), "demo 13 commit"),
                (("demo_14.txt", "content for demo_14"), "demo 14 commit"),
                (("demo_15.txt", "content for demo_15"), "demo 15 commit"),
            ])
            with fake_cliux(log_level=INFO) as (cli, get_lines):
                opts = ValidateOptions(ValidateCLIOptions(
                    verbose=True,
                    commit_count_soft_fail_threshold=10,
                    commit_count_auto_bypass_soft_fail=True,
                    cwd=downstream.working_dir))
                await do_validate(cli=cli, opts=opts)
                assert strip_ansi("".join(get_lines())) == """determined that local branch mnorth-review-111 tracks upstream branch mnorth-review-111 on remote origin
Comparing mnorth-review-111 against origin/mnorth-review-111
[WARNING]: WARNING: LARGE NUMBER OF REVIEW BRANCH COMMITS
----------------------------------------
MORE INFORMATION
An unusually large 16 number of commits were detected on review branch mnorth-review-111, which were not found on tracked branch origin/mnorth-review-111.

This may be an indication of an improper rebase!

This warning is presented whenever more than 10 new commits, that have not yet been pushed, are found on a review branch.

Please take a close look at your review branch, and ensure you don't see any duplicate commits that are already on master

WHAT TO DO NEXT
- You may choose to continue
- You may choose to abort by pressing Ctrl + C
[WARNING]: Proceeding at user's request
"""


async def test_review_branch_commit_count_hard_fail():
    try:
        with temp_repo() as upstream:
            upstream_default_branch = upstream.active_branch
            upstream.create_head('mnorth-review-111')
            create_git_history(upstream, [
                (("demo_0.txt", "content for demo_0"), "demo 0 commit"),
                (("demo_1.txt", "content for demo_1"), "demo 1 commit"),
                (("demo_2.txt", "content for demo_2"), "demo 2 commit"),
                (("demo_3.txt", "content for demo_3"), "demo 3 commit"),
            ])
            upstream_default_branch.checkout()
            with temp_repo_clone(upstream, ['mnorth-review-111']) as downstream:
                # downstream_default_branch = downstream.active_branch
                downstream_review_branch = downstream.heads['mnorth-review-111']
                assert downstream_review_branch is not None
                downstream_review_branch.checkout()
                create_git_history(downstream, [
                    (("demo_4.txt", "content for demo_4"), "demo 4 commit"),
                    (("demo_5.txt", "content for demo_5"), "demo 5 commit"),
                    (("demo_6.txt", "content for demo_6"), "demo 6 commit"),
                    (("demo_7.txt", "content for demo_7"), "demo 7 commit"),
                    (("demo_8.txt", "content for demo_8"), "demo 8 commit"),
                    (("demo_9.txt", "content for demo_9"), "demo 9 commit"),
                    (("demo_10.txt", "content for demo_10"), "demo 10 commit"),
                    (("demo_11.txt", "content for demo_11"), "demo 11 commit"),
                    (("demo_12.txt", "content for demo_12"), "demo 12 commit"),
                    (("demo_13.txt", "content for demo_13"), "demo 13 commit"),
                    (("demo_14.txt", "content for demo_14"), "demo 14 commit"),
                    (("demo_15.txt", "content for demo_15"), "demo 15 commit"),
                ])
                with fake_cliux(log_level=INFO) as (cli, get_lines):
                    opts = ValidateOptions(ValidateCLIOptions(
                        verbose=True,
                        commit_count_soft_fail_threshold=5,
                        commit_count_hard_fail_threshold=10,
                        cwd=downstream.working_dir))
                    await do_validate(cli=cli, opts=opts)
                    assert False, 'Error should have already been thrown by this point'
    except LikelyUserErrorException as ex:
        assert ex is not None
        assert strip_ansi(str(ex)) == """DANGER: VERY LARGE NUMBER OF REVIEW BRANCH COMMITS
----------------------------------------
MORE INFORMATION
An very large 16 number of commits were detected on review branch mnorth-review-111, which were not found on tracked branch origin/mnorth-review-111.

This may be an indication of an improper rebase!

This warning is presented whenever more than 10 new commits that have not yet been pushed are found on a review branch.

Please take a close look at your review branch, and ensure you don't see any duplicate commits that are already on master

WHAT TO DO NEXT
- It's quite possible that you've made a mistake in your review branch, that you need to address
- If you're doing something exotic deliberately, you can suppress this failure by trying this command again, while skipping all git hooks"""
