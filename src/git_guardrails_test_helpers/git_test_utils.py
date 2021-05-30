from os import path
from typing import Iterator
from git import Repo  # type: ignore
import tempfile
from contextlib import contextmanager


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
            yield repo
