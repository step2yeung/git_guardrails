import pytest
from unittest.mock import patch
from git_guardrails.cli.color import strip_ansi
from git_guardrails.validate import do_validate
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux
from git_guardrails.validate.options import ValidateOptions
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails_test_helpers.git_test_utils import create_example_file_in_repo, temp_dir, temp_repo
from git_guardrails.git_utils import git_default_branch
from git.repo.base import Repo


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@patch('builtins.input', return_value="continue")
async def test_do_validate(mock_input):
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
            new_branch = downstream.create_head("feature/123")
            assert len(downstream.index.unmerged_blobs()) == 0
            new_branch.checkout()
            with create_example_file_in_repo(repo=downstream, file_path="hello.txt", content="12345") as _:
                downstream.index.commit("second commit")
                assert len(downstream.remotes) == 1
                assert "feature/123" in map(lambda h: h.name, downstream.heads)
                assert downstream.is_dirty() == False
                assert downstream.active_branch.name == "feature/123"
                downstream_default_branch = git_default_branch(downstream_dir)
                assert downstream_default_branch == upstream.active_branch.name
                with fake_cliux() as (cli, get_lines):
                    opts = ValidateOptions(ValidateCLIOptions(verbose=True, cwd=downstream_dir))
                    await do_validate(cli=cli, opts=opts)
                    assert strip_ansi("".join(get_lines())) == f"""[INFO]: active_branch: feature/123
[INFO]: default_branch: {downstream_default_branch}
[INFO]: merge_bases: {merge_base.hexsha[0:8]}
"""
