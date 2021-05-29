import asyncio
from functools import reduce
from yaspin import yaspin

from git.repo.base import Repo
from git_guardrails.cli.ux import CLIUX
from git_guardrails.cli.value_format import format_branch_name, format_cli_command, format_commit, format_integer
from git_guardrails.errors import NonApplicableSituationException, UnhandledSituationException
from git_guardrails.git_utils import git_default_branch
from git_guardrails.validate.options import ValidateOptions
from git_guardrails.coroutine import as_async


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


@as_async
def get_default_git_branch(cwd: str) -> str:
    with yaspin().white.bold as sp:
        sp.text = "determining default branch"
        default_branch = git_default_branch(cwd=cwd)
        sp.text = ''
        sp.ok(f"default_branch: {default_branch}")
        return default_branch


async def do_validate(cli: CLIUX, opts: ValidateOptions):
    try:
        cwd = opts.getWorkingDirectory()
        repo = Repo(cwd)
        remotes = repo.remotes
        num_remotes = len(remotes)
        if (num_remotes == 0):
            raise NonApplicableSituationException(
                'No git remotes found',
                "".join(
                    [
                        format_cli_command('git_guardrails validate'),
                        " is intended for ",
                        "use when pushing new code to a remote, and no remotes were found. "
                    ]
                )
            )
        active_branch = await opts.getCurrentBranchName(repo)
        cli.info(f"active_branch: {active_branch}")
        default_branch = await get_default_git_branch(cwd)
        cli.info(f"default_branch: {default_branch}")
        merge_bases = repo.merge_base(default_branch, active_branch)
        merge_bases_csv = ", ".join(map(lambda c: c.hexsha[0:8], merge_bases))
        cli.info(f"merge_bases: {merge_bases_csv}")
        num_merge_bases = len(merge_bases)
        if (num_merge_bases == 0):
            raise UnhandledSituationException('No merge-base commit found',
                                              f"""No merge-base commits between branches {
                                              format_branch_name(default_branch)
                                              } and {
                                                format_branch_name(active_branch)
                                                } could be found, so validation could not be performed.""")
        if (num_merge_bases > 1):
            description = " ".join(
                [f"Multiple ({format_integer(num_merge_bases)}) merge-base commits between branches",
                 format_branch_name(default_branch),
                 "and",
                 format_branch_name(active_branch),
                 "were found:"
                 ]
            )
            commits_description = reduce(lambda a, b: f"{a}\n- {b}", map(format_commit, merge_bases), "")
            raise UnhandledSituationException('Multiple merge-base commits found',
                                              description + commits_description)
    except NonApplicableSituationException as ex:
        cli.handle_non_applicable_situation_exception(ex)
    except UnhandledSituationException as ex:
        cli.handle_unhandled_situation_exception(ex)
