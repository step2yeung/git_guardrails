from git.repo.base import Repo  # type: ignore
from git_guardrails_test_helpers.git_test_utils import create_example_file_in_repo, temp_dir, temp_repo
from git_guardrails.git_utils import git_default_branch


def test_git_default_branch_detection():
    with temp_repo() as upstream:
        assert upstream is not None
        upstream.index.commit("first commit")
        assert upstream.is_dirty() == False
        assert upstream.active_branch.name in ["master", "main"]
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
                assert git_default_branch(downstream_dir) == upstream.active_branch.name
