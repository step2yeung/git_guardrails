

class ValidateCLIOptions:
    def __init__(self, verbose: bool, cwd: str, current_branch: str):
        assert verbose is not None, "ValidateCLIOptions#verbose must be either True or False"
        self.cwd = cwd
        self.verbose = verbose
        self.current_branch = current_branch

    def __str__(self):
        return 'ValidateCLIOptions'

    def to_dict(self):
        return {
            "cwd": self.cwd,
            "verbose": self.verbose,
            "current_branch": self.current_branch
        }
