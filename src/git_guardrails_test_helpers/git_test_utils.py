from git import Repo
from os import path
import tempfile
from contextlib import contextmanager


@contextmanager
def temp_repo() -> Repo:
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(tmpdirname)
        example_file_name = path.join(tmpdirname, "example.txt")
        with open(example_file_name, "w") as example_file:
            example_file.write("Example content")
            r = Repo.init(tmpdirname)
            r.index.add([example_file_name])
            r.index.commit("first commit")
            yield r
