from git.refs.head import Head  # type: ignore
from git.remote import Remote  # type: ignore
import pytest
from unittest.mock import patch
from git_guardrails.cli.color import strip_ansi
from git_guardrails.validate import do_validate
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux
from git_guardrails.validate.options import ValidateOptions
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails_test_helpers.git_test_utils import create_example_file_in_repo, temp_dir, temp_repo
from git_guardrails.git_utils import git_default_branch
from git.repo.base import Repo  # type: ignore


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@patch('builtins.input', return_value="continue")
async def test_do_validate_with_remote(mock_input):
    with temp_repo() as upstream:
        assert upstream is not None
        upstream.index.commit("first commit")
        assert upstream.is_dirty() == False
        assert upstream.active_branch.name in ["master", "main"]
        merge_base = upstream.active_branch.commit
        assert merge_base is not None
        with temp_dir() as downstream_dir:
            downstream = Repo.clone_from(upstream.working_dir, downstream_dir)
            assert downstream is not None
            assert downstream.is_dirty() == False
            new_branch = downstream.create_head("feature-123")
            assert len(downstream.index.unmerged_blobs()) == 0
            new_branch.checkout()
            with create_example_file_in_repo(repo=downstream, file_path="hello.txt", content="12345") as _:
                downstream.index.commit("second commit")
                assert len(downstream.remotes) == 1
                assert "feature-123" in map(lambda h: h.name, downstream.heads)
                assert downstream.is_dirty() == False
                assert downstream.active_branch.name == "feature-123"
                downstream_default_branch = git_default_branch(downstream)
                assert downstream_default_branch == upstream.active_branch.name
                with fake_cliux() as (cli, get_lines):
                    opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=downstream_dir))
                    await do_validate(cli=cli, opts=opts)
                    assert strip_ansi("".join(get_lines())) == f"""[DEBUG]: active branch: feature-123 @ {downstream.active_branch.commit.hexsha}
[DEBUG]: default branch: {downstream_default_branch} @ {downstream.heads[downstream_default_branch].commit.hexsha}
[DEBUG]: merge_bases: {merge_base.hexsha[0:8]}
[INFO]: git_guardrails has completed without taking any action.

THERE'S NOTHING TO DO BECAUSE: BRANCH FEATURE-123 DOES NOT TRACK A REMOTE BRANCH
----------------------------------------
MORE INFORMATION
The currently active branch does not track a remote branch yet, perhaps you have not pushed it yet?

WHAT TO DO NEXT
- There is no reason to think anything is wrong, and no user action is required
"""


@patch('builtins.input', return_value="continue")
async def test_do_validate_with_remote_that_has_upstream_commits(mock_input):
    with temp_repo() as upstream:
        assert upstream is not None
        upstream.index.commit("first commit")
        assert upstream.is_dirty() == False
        assert upstream.active_branch.name in ["master", "main"]
        upstream_default_branch = upstream.active_branch
        upstream_feature_branch = upstream.create_head("feature-123")
        upstream_feature_branch.checkout()
        with create_example_file_in_repo(repo=upstream, file_path="sample.txt", content="aaaa") as _:
            upstream.index.commit('first feature commit')
            upstream_default_branch.checkout()
            assert upstream.refs[upstream_default_branch.name] is not None
            merge_base = upstream_default_branch.commit
            with temp_dir() as downstream_dir:
                downstream = Repo.clone_from(upstream.working_dir, downstream_dir)
                downstream_upstream_remote: Remote = downstream.remotes['origin']
                downstream_default_branch = downstream.active_branch
                assert downstream_default_branch is not None
                upstream_default_branch_ref = upstream.refs[upstream_default_branch.name]
                upstream_feature_branch_ref = upstream.refs[upstream_feature_branch.name]

                assert upstream_default_branch_ref is not None
                downstream_feature_branch: Head = downstream.create_head(
                    upstream_feature_branch_ref.name,
                    commit=upstream_feature_branch_ref.commit
                )
                assert downstream_feature_branch is not None
                assert ', '.join(map(lambda r: r.name, downstream_upstream_remote.refs)) == ', '.join([
                    'origin/HEAD', 'origin/feature-123', 'origin/master'
                ])
                assert upstream_feature_branch.name == "feature-123"
                assert downstream_upstream_remote.refs['master'] is not None
                assert downstream_upstream_remote.refs['feature-123'] is not None
                downstream_feature_branch.set_tracking_branch(downstream_upstream_remote.refs['feature-123'])
                downstream_feature_branch.checkout()
                assert downstream.heads['feature-123'] is not None
                assert downstream is not None
                assert downstream.is_dirty() == False
                downstream_feature_branch = downstream.heads["feature-123"]
                downstream_feature_branch.checkout()
                upstream_feature_branch.checkout()
                with create_example_file_in_repo(repo=upstream, file_path="hello.txt", content="12345") as _:
                    upstream.index.commit("second feature commit")
                    upstream_default_branch.checkout()
                    # downstream_default_branch_tracked = downstream_default_branch.tracking_branch()
                    # assert downstream_default_branch.name == upstream.active_branch.name
                    with fake_cliux() as (cli, get_lines):
                        opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=downstream_dir))
                        await do_validate(cli=cli, opts=opts)
                        assert strip_ansi("".join(get_lines())) == f"""[DEBUG]: active branch: feature-123 @ {
                            downstream_feature_branch.commit.hexsha
}
[DEBUG]: default branch: {downstream_default_branch.name} @ {downstream_default_branch.commit.hexsha}
[DEBUG]: merge_bases: {merge_base.hexsha[0:8]}
[INFO]: determined that local branch feature-123 tracks upstream branch feature-123 on remote origin
[DEBUG]: latest commit for local ref origin/feature-123: {downstream_feature_branch.commit.hexsha}
[DEBUG]: latest commit for tracked branch feature-123 on remote origin: {upstream_feature_branch.commit.hexsha}
[WARNING]: New commits on origin/feature-123 were detected, which have not yet been pulled down to feature-123
"""


@patch('builtins.input', return_value="continue")
async def test_do_validate_no_remote(mock_input):
    with temp_repo() as upstream:
        assert upstream is not None
        upstream.index.commit("first commit")
        assert upstream.is_dirty() == False
        assert upstream.active_branch.name in ["master", "main"]

        with fake_cliux() as (cli, get_lines):
            opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=upstream.working_dir))
            await do_validate(cli=cli, opts=opts)
            assert strip_ansi("".join(get_lines())) == """[INFO]: git_guardrails has completed without taking any action.

THERE'S NOTHING TO DO BECAUSE: NO GIT REMOTES FOUND
----------------------------------------
MORE INFORMATION
git_guardrails validate is intended for use when pushing new code to a remote, and no remotes were found.

WHAT TO DO NEXT
- There is no reason to think anything is wrong, and no user action is required
"""
