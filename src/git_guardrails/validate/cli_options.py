DEFAULT_COMMIT_COUNT_SOFT_FAIL_THRESHOLD = 40
DEFAULT_COMMIT_COUNT_HARD_FAIL_THRESHOLD = 80


class ValidateCLIOptions:
    def __init__(self,
                 commit_count_soft_fail_threshold: int = DEFAULT_COMMIT_COUNT_SOFT_FAIL_THRESHOLD,
                 commit_count_hard_fail_threshold: int = DEFAULT_COMMIT_COUNT_HARD_FAIL_THRESHOLD,
                 verbose: bool = False,
                 cwd: str = None,
                 current_branch: str = None,
                 auto_fetch: bool = None,
                 color: bool = None,
                 tty: bool = None):
        self.cwd = cwd
        self.verbose = verbose
        self.current_branch = current_branch
        self.color = color
        self.tty = tty
        self.auto_fetch = auto_fetch
        self.commit_count_soft_fail_threshold = commit_count_soft_fail_threshold
        self.commit_count_hard_fail_threshold = commit_count_hard_fail_threshold

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
