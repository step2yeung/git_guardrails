from os import getcwd
from typing import Callable, Union
from git import Repo  # type: ignore
from git_guardrails.cli.color import supports_color
from git_guardrails.cli.tty import is_tty_supported

from git_guardrails.validate.cli_options import ValidateCLIOptions


class ValidateOptions:
    def __init__(self, cliOptions: ValidateCLIOptions):
        self.cliOpts = cliOptions

    def __str__(self):
        return "".join([
            "ValidateOptions(",
            ', '.join(
                map(
                    lambda pair: f"{pair[0]}={pair[1]}",
                    [
                        ["cliOpts", str(self.cliOpts)]
                    ]
                )
            ),
            ')'
        ])

    def is_verbose(self) -> bool:
        if self.cliOpts.verbose is True:
            return True
        else:
            return False

    async def get_current_branch_name(self, repo: Repo) -> str:
        if (self.cliOpts.current_branch is not None):
            return self.cliOpts.current_branch
        else:
            return repo.active_branch.name

    def get_cwd(self) -> str:
        if (self.cliOpts.cwd is not None):
            return self.cliOpts.cwd
        else:
            return getcwd()

    def is_auto_fetch_enabled(self) -> Union[bool, None]:
        if (self.cliOpts.auto_fetch is not None):
            return self.cliOpts.auto_fetch
        else:
            return None

    def is_auto_rebase_enabled(self) -> Union[bool, None]:
        if (self.cliOpts.auto_rebase is not None):
            return self.cliOpts.auto_rebase
        else:
            return None

    def is_terminal_color_supported(self, color_support_checker: Callable[[], bool] = supports_color) -> bool:
        if (self.cliOpts.color is not None):
            return self.cliOpts.color
        else:
            return color_support_checker()

    def is_terminal_tty_supported(self, tty_support_checker: Callable[[], bool] = is_tty_supported) -> bool:
        if (self.cliOpts.tty is not None):
            return self.cliOpts.tty
        else:
            return tty_support_checker()

    async def to_dict(self, repo):
        return {
            "verbose": self.is_verbose(),
            "current_branch": await self.get_current_branch_name(repo),
            "cwd": self.get_cwd()
        }
