import click
from functools import reduce
from git.refs.head import Head  # type: ignore
from git.remote import Remote  # type: ignore
from yaspin import yaspin  # type: ignore

from git.repo.base import Repo  # type: ignore
from git_guardrails.cli.ux import CLIUX
from git_guardrails.cli.value_format import format_branch_name, format_cli_command, format_commit
from git_guardrails.cli.value_format import format_integer, format_remote_name
from git_guardrails.errors import NonApplicableSituationException, UnhandledSituationException, UserBypassException
from git_guardrails.git_utils import git_default_branch, git_does_commit_exist_locally, git_ls_remote
from git_guardrails.validate.options import ValidateOptions
from git_guardrails.coroutine import as_async


@as_async
def get_default_git_branch(repo: Repo) -> str:
    with yaspin().white.bold as sp:
        sp.text = "determining default branch"
        default_branch = git_default_branch(repo)
        sp.text = ''
        sp.stop()
        return default_branch


def validate_remotes(repo: Repo):
    remotes = repo.remotes   # remotes
    num_remotes = len(remotes)
    if (num_remotes == 0):
        raise NonApplicableSituationException(
            'No git remotes found',
            "".join(
                [
                    format_cli_command('git_guardrails validate'),
                    " is intended for ",
                    "use when pushing new code to a remote, and no remotes were found."
                ]
            )
        )


def validate_merge_bases_with_default_branch(cli: CLIUX, repo: Repo, active_branch_name: str, default_branch_name: str):
    merge_bases = repo.merge_base(default_branch_name, active_branch_name)
    merge_bases_csv = ", ".join(map(lambda c: c.hexsha[0:8], merge_bases))
    cli.debug(f"merge_bases: {merge_bases_csv}")
    num_merge_bases = len(merge_bases)
    if (num_merge_bases == 0):
        raise UnhandledSituationException(
            'No merge-base commit found',
            f"""No merge-base commits between branches {format_branch_name(default_branch_name) } and {
            format_branch_name(active_branch_name) } could be found, so validation could not be performed.""")
    if (num_merge_bases > 1):
        description = " ".join(
            [
                f"Multiple ({format_integer(num_merge_bases)}) merge-base commits between branches",
                format_branch_name(default_branch_name),
                "and",
                format_branch_name(active_branch_name),
                "were found:"
            ]
        )
        commits_description = reduce(lambda a, b: f"{a}\n- {b}", map(format_commit, merge_bases), "")
        raise UnhandledSituationException(
            'Multiple merge-base commits found',
            description + commits_description)


def get_branch_information(repo: Repo, branch_name: str) -> Head:
    branch_head: Head = repo.heads[branch_name]
    if (branch_head is None):
        raise UnhandledSituationException(
            f"Could not find branch {branch_name}",
            f"A branch called '{branch_name}' could not be found in repo {repo.working_dir()}"
        )
    return branch_head


async def do_validate(cli: CLIUX, opts: ValidateOptions):
    try:
        cwd = opts.get_cwd()  # working directory
        repo = Repo(cwd)  # git repo

        validate_remotes(repo=repo)

        active_branch = get_branch_information(repo, await opts.get_current_branch_name(repo))  # current_branch
        cli.debug(f"active branch: {active_branch.name} @ {active_branch.commit.hexsha}")
        default_branch = get_branch_information(repo, await get_default_git_branch(repo))  # default branch
        cli.debug(f"default branch: {default_branch.name} @ {default_branch.commit.hexsha}")

        if active_branch == default_branch:
            raise NonApplicableSituationException(
                f"You are on the default branch ({default_branch.name})",
                """git_guardrails is intended to catch potential problems when pushing
review branches, and will not take any action when on a git repo's default branch""")

        cli.debug('validating merge base between review branch and default branch')
        validate_merge_bases_with_default_branch(
            cli=cli,
            repo=repo,
            active_branch_name=active_branch,
            default_branch_name=default_branch
        )
        cli.debug('merge base validation complete')

        active_branch_tracked_ref = active_branch.tracking_branch()
        if (active_branch_tracked_ref is None):
            raise NonApplicableSituationException(
                f"Branch {active_branch.name} does not track a remote branch",
                "The currently active branch does not track a remote branch yet, perhaps you have not pushed it yet?")

        cli.info(f"""determined that local branch {format_branch_name(active_branch.name)} tracks upstream branch {
            format_branch_name(active_branch_tracked_ref.remote_head)
            } on remote {format_remote_name(active_branch_tracked_ref.remote_name)}""")

        with yaspin().white.bold as sp:
            sp.text = f"searching for new upstream commits on {active_branch_tracked_ref.name}"
            sp.start()
            latest_remote_sha = git_ls_remote(repo=repo,
                                              ref=active_branch_tracked_ref,
                                              ref_types=["heads"])
            latest_local_sha = active_branch_tracked_ref.commit.hexsha
            sp.stop()
            cli.debug(f"latest commit for local ref {active_branch_tracked_ref.name}: {latest_local_sha}")
            cli.debug(f"""latest commit for tracked branch {active_branch_tracked_ref.remote_head
                      } on remote {active_branch_tracked_ref.remote_name}: {latest_remote_sha}""")

            has_latest_commits_from_upstream = git_does_commit_exist_locally(repo=repo, sha=latest_remote_sha)
            if (has_latest_commits_from_upstream == False):
                cli.warning(f"""New commits on {active_branch_tracked_ref
                            } were detected, which have not yet been pulled down to {active_branch.name}""")
                user_response = click.confirm("Would you like to download these new commits?")
                if user_response == False:
                    cli.debug(f"When asked whether we can download new commits, user response was {user_response}")
                    raise UserBypassException(f"""user decided not to download new commits from {
                        active_branch_tracked_ref.name}""")
                origin: Remote = repo.remotes['origin']
                refspec = f"{active_branch.name}:{active_branch_tracked_ref.name}"
                cli.info(f"Fetching new commits for branch {active_branch_tracked_ref.name}")
                cli.debug(f"running 'git fetch' from remote '{origin.name}' with refspec '{refspec}'")
                origin.fetch()
                cli.info(f"Fetch from {origin.name} complete")
    except UserBypassException as ex:
        cli.handle_user_bypass_exception(ex)
    except NonApplicableSituationException as ex:
        cli.handle_non_applicable_situation_exception(ex)
    except UnhandledSituationException as ex:
        cli.handle_unhandled_situation_exception(ex)
