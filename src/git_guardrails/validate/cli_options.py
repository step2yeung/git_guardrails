
class ValidateCLIOptions:
    def __init__(self,
                 verbose: bool = False,
                 cwd: str = None,
                 current_branch: str = None,
                 color: bool = None,
                 tty: bool = None):
        self.cwd = cwd
        self.verbose = verbose
        self.current_branch = current_branch
        self.color = color
        self.tty = tty

    def __str__(self):
        return "".join([
            "ValidateCLIOptions(",
            ', '.join(
                map(
                    lambda pair: f"{pair[0]}={pair[1]}",
                    [
                        ["cwd", self.cwd],
                        ["verbose", self.verbose],
                        ["current_branch", self.current_branch]
                    ]
                )
            ),
            ')'
        ])

    def to_dict(self):
        return {
            "cwd": self.cwd,
            "verbose": self.verbose,
            "current_branch": self.current_branch
        }
