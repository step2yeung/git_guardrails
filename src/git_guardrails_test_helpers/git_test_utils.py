import json
from os import path
from typing import Iterator, List, Tuple
from git import Repo  # type: ignore
import tempfile
from contextlib import contextmanager
from git.refs.log import RefLog, RefLogEntry   # type: ignore
from git.remote import Remote  # type: ignore


@contextmanager
def temp_dir() -> Iterator[str]:
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def temp_repo_in_dir(dir: str) -> Repo:
    return Repo.init(dir)


@contextmanager
def create_example_file_in_repo(repo: Repo, file_path: str, content: str) -> Iterator[str]:
    full_file_path = path.join(repo.working_dir, file_path)
    with open(full_file_path, "w+") as f:
        f.write(content)
        repo.index.add([full_file_path])
        yield full_file_path


@contextmanager
def temp_repo() -> Iterator[Repo]:
    with temp_dir() as tmpdirname:
        repo = temp_repo_in_dir(tmpdirname)
        with create_example_file_in_repo(
            repo=repo,
            file_path="example.txt",
            content="Example content"
        ) as _:
            commit_all_modified_tracked_files(repo, 'initial commit')
            assert repo is not None
            assert repo.is_dirty() == False
            assert repo.active_branch.name in ["master", "main"]
            yield repo


def commit_all_modified_tracked_files(repo: Repo, message: str):
    if (repo.is_dirty() == True):
        repo.index.add([])
        repo.index.commit(message)


def create_single_file_git_commit(repo: Repo, requested_commit: Tuple[Tuple[str, str], str]):
    try:
        repo_dir = repo.working_dir

        commit_message = requested_commit[1]
        file_and_content = requested_commit[0]

        file_path = file_and_content[0]
        file_content = file_and_content[1]

        f = open(path.join(repo_dir, file_path), 'w+')
        f.write(file_content)
        repo.index.add([])
        repo.index.commit(commit_message)
    except IndexError:
        raise Exception(f"Invalid commit tuple: {json.dumps(requested_commit)}")


@contextmanager
def temp_repo_clone(original: Repo, branches_to_checkout: List[str] = []) -> Iterator[Repo]:
    original_default_branch = original.active_branch
    with temp_dir() as dir:
        new_clone = original.clone(dir)
        upstream_remote: Remote = new_clone.remotes['origin']
        for branch_to_checkout in branches_to_checkout:
            upstream_ref = upstream_remote.refs[branch_to_checkout]
            new_head = new_clone.create_head(branch_to_checkout)
            new_head.set_tracking_branch(upstream_ref)

        original_default_branch.checkout()
        assert new_clone is not None
        assert new_clone.is_dirty() == False
        assert len(new_clone.remotes) == 1
        yield new_clone


def reflog_to_str(log: RefLog) -> str:
    def reflog_entry_to_str(entry: RefLogEntry):
        return f"{entry.message}"
    data = list(map(reflog_entry_to_str, log))
    return "\n".join(data)


def create_git_history(repo: Repo, requested_commits: List[Tuple[Tuple[str, str], str]]):
    assert repo.is_dirty() == False, "create_git_history may only be invoked on a 'clean' repo"
    for c in requested_commits:
        create_single_file_git_commit(repo, c)


def sorted_repo_branch_names(repo: Repo) -> List[str]:
    return sorted(list(map(lambda h: h.name, repo.heads)))
