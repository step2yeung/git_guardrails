
from git_guardrails.validate.cli_options import ValidateCLIOptions


class ValidateOptions:
    def __init__(self, cliOptions: ValidateCLIOptions):
        self.cliOpts = cliOptions

    def __str__(self):
        return self.name

    def isVerbose(self) -> bool:
        return True

    async def getCurrentBranchName(self) -> str:
        return ''

    async def to_dict(self):
        return {
            "verbose": self.isVerbose(),
            "current_branch": await self.getCurrentBranchName()
        }
