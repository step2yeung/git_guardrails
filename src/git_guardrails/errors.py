from typing import List
from colorama import Style


class ExceptionWithNextBestActions(Exception):
    """
    An exception class that's designed to surface the following things to the end user
    - What happened
    - Why
    - What are the "next best actions" the user can take?
    """

    def __init__(self, what_happened: str, reason: str, next_best_actions: List[str]):
        self.what_happened = what_happened
        self.reason = reason
        self.next_best_actions = next_best_actions

    def __str__(self):
        formatted_title = f"{Style.BRIGHT}{self.what_happened.upper()} {Style.RESET_ALL}"
        divider = "----------------------------------------"
        more_info_title = f"{Style.DIM}MORE INFORMATION{Style.RESET_ALL}"
        next_actions_title = f"""
{Style.DIM}WHAT TO DO NEXT{Style.RESET_ALL}"""
        next_actions_bullets = "\n".join(map(lambda s: f"- {s}", self.next_best_actions))
        return "\n".join([formatted_title, divider, more_info_title, self.reason, next_actions_title, next_actions_bullets])


class NonApplicableSituationException(ExceptionWithNextBestActions):
    """
    Raised in situations where the current usage is found to *not apply*.

    For example, validation logic in a pre-push git hook is not meaningful
    - if we find that there are no remotes to push to
    - if we find that the user is currently on their default branch
    - if we find that there are no new commits to push
    """

    def __init__(self, situation_title: str, situation_details: str):
        super().__init__(f"There's nothing to do because: {situation_title}", situation_details,
                         ["There is no reason to think anything is wrong, and no user action is required"])


class UnhandledSituationException(ExceptionWithNextBestActions):
    """
    Raised in situations where validation cannot proceed due to the git repo
    state being something other than what we expected it to be. The user is offered
    a warning, and an opportunity to either abort or proceed

    For example, validation logic in a pre-push git hook cannot proceed if
    - we find zero commits in the repository
    - we find the user on a branch that somehow has no merge-base with the default branch
    - the user tries to push while in a detached head state
    """

    def __init__(self, situation_title: str, situation_details: str):
        super().__init__(f"Unexpected workspace state: {situation_title}", situation_details,
                         ["You may choose to proceed at your own risk", "You may abort by pressing Ctrl + C"])
