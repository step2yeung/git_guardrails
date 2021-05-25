from git import Repo


class GitRepo:
    def __init__(self, cwd: str):
        self.r = Repo(cwd)
