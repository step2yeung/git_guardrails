from os import getcwd
from git import Repo

from git_guardrails.validate.cli_options import ValidateCLIOptions


class ValidateOptions:
    def __init__(self, cliOptions: ValidateCLIOptions):
        self.cliOpts = cliOptions

    def __str__(self):
        return self.name

    def isVerbose(self) -> bool:
        if self.cliOpts.verbose is True:
            return True
        else:
            return False

    async def getCurrentBranchName(self, repo: Repo) -> str:
        if (self.cliOpts.current_branch is not None):
            return self.cliOpts.current_branch
        else:
            return repo.active_branch.name

    def getWorkingDirectory(self) -> str:
        if (self.cliOpts.cwd is not None):
            return self.cliOpts.cwd
        else:
            return getcwd()

    async def to_dict(self, repo):
        return {
            "verbose": self.isVerbose(),
            "current_branch": await self.getCurrentBranchName(repo),
            "cwd": self.getWorkingDirectory()
        }
