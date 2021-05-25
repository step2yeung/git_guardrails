

class ValidateCLIOptions:
    def __init__(self, verbose: bool, current_branch: str):
        self.verbose = verbose
        self.current_branch = current_branch

    def __str__(self):
        return 'ValidateCLIOptions'

    def to_dict(self):
        return {
            "verbose": self.verbose,
            "current_branch": self.current_branch
        }
